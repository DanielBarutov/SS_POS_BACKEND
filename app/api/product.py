
from sqlalchemy import select
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload
from app.core.db import get_db
from app.models.product import Product, Category
from pydantic import BaseModel

# !CHAR
router = APIRouter()

# !PYDANTIC


class CategoryCreate(BaseModel):
    name: str
    parent_id: int | None = None


class CategoryGet(BaseModel):
    id: int
    name: str
    parent_id: int | None = None
    children: list["CategoryGet"] = []

class CategoryGetOnce(BaseModel):
    id: int
    name: str
    parent_id: int | None = None
    

class ProductCreate(BaseModel):
    name: str
    category_id: int
    kit: bool = False
    price_retail: float
    price_purchase: float


class ProductGet(BaseModel):
    id: int
    name: str
    category_id: int | None
    category: CategoryGet | None
    kit: bool
    price_retail: float
    price_purchase: float


# !ROUTES


@router.get("/products", tags=["Product"], response_model=list[ProductGet])
def get_products(db: Session = Depends(get_db)):
    products = db.execute(select(Product).options(
        selectinload(Product.category))).scalars().all()
    if not products:
        raise HTTPException(404, "Products not found")

    return products


@router.get("/product/{product_id}", tags=["Product"], response_model=ProductGet)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.execute(select(Product).where(
        Product.id == product_id)).scalar()
    if not product:
        raise HTTPException(404, "Product not found")
    return product

@router.get("/product/category/{category_id}", tags=["Product"], response_model=list[ProductGet])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    products = db.execute(select(Product).where(
        Product.category_id == category_id)).scalars().all()
    if not products:
        raise HTTPException(404, "Products not found")
    return products


@router.get("/product", tags=["Product"], response_model=ProductGet)
def get_product_by_name(name: str, db: Session = Depends(get_db)):
    product = db.execute(select(Product).where(
        Product.name.ilike(f"%{name}%"))).scalar()
    if not product:
        raise HTTPException(404, "Product not found")
    return product


@router.post("/product", tags=["Product"], response_model=ProductCreate)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    category = db.execute(select(Category).where(
        Category.id == product.category_id)).scalar()
    if not category:
        raise HTTPException(404, "Category not found")

    new_product = Product(
        name=product.name,
        category_id=product.category_id,
        kit=product.kit,
        price_retail=product.price_retail,
        price_purchase=product.price_purchase
    )
    db.add(new_product)
    try:
        db.commit()
        db.refresh(new_product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Product with this name already exists")

    return new_product


@router.patch("/product/{product_id}", tags=["Product"])
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    existing_product = db.get(Product, product_id)
    if not existing_product:
        raise HTTPException(404, "Product not found")

    category = db.execute(select(Category).where(
        Category.id == product.category_id)).scalar()
    if not category:
        raise HTTPException(404, "Category not found")

    existing_product.name = product.name
    existing_product.category_id = product.category_id
    existing_product.kit = product.kit
    existing_product.price_retail = product.price_retail
    existing_product.price_purchase = product.price_purchase

    try:
        db.commit()
        db.refresh(existing_product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Product with this name already exists")

    return existing_product


@router.delete("/product/{product_id}", tags=["Product"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    db.delete(product)
    db.commit()


@router.get("/category", tags=["Category"], response_model=list[CategoryGet])
def get_categories(db: Session = Depends(get_db)):
    categories = db.execute(select(Category)).scalars().all()
    if not categories:
        raise HTTPException(404, "Categories not found")

    return categories

@router.get("/category/{category_id}", tags=["Category"], response_model=list[CategoryGetOnce])
def get_categories_by_id(category_id: int, db: Session = Depends(get_db)):
    categories = db.execute(select(Category).where(Category.parent_id == category_id).options(
        selectinload(Category.children))).scalars().all()
    if not categories:
        raise HTTPException(404, "Categories not found")

    return categories




@router.post("/category", tags=["Category"], response_model=CategoryCreate)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    if category.parent_id:
        parent_category = db.execute(select(Category).where(
            Category.id == category.parent_id)).scalar()
        if not parent_category:
            raise HTTPException(404, "Parent category not found")

    new_category = Category(
        name=category.name,
        parent_id=category.parent_id if category.parent_id != 0 else None
    )
    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Category with this name already exists")


@router.delete("/category/{category_id}", tags=["Category"])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(404, "Category not found")
    if category.children:
        raise HTTPException(400, "Cannot delete category with subcategories")
    db.delete(category)
    db.commit()

# !FUNCTIONS
