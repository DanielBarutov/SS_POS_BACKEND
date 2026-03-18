import csv
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker
from .base import Base
from .product import Category, Product

# Подключение (используем твои данные из первого скриншота)
DATABASE_URL = "postgresql+psycopg2://admin:555@san_db:5432/san"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def migrate():
    session = SessionLocal()
    try:
        # 1. ЗАГРУЗКА КАТЕГОРИЙ
        with open('./app/models/categories2fix.csv', mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            category_cache = {} # {name: id}
            
            for row in reader:
                name = row['name'].strip()
                parent_name = row.get('parent_name', '').strip()
                
                # Получаем id родителя из кэша, если он есть
                parent_id = category_cache.get(parent_name) if parent_name else None
                
                # Проверяем, нет ли уже такой категории в базе
                db_cat = session.execute(select(Category).where(Category.name == name)).scalar_one_or_none()
                
                if not db_cat:
                    db_cat = Category(name=name, parent_id=parent_id)
                    session.add(db_cat)
                    session.flush() # Получаем ID без фиксации всей транзакции
                
                category_cache[name] = db_cat.id

        print(f"Категории обработаны. Всего: {len(category_cache)}")

        # 2. ЗАГРУЗКА ТОВАРОВ
        with open('./app/models/products2fix.csv', mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            product_count = 0
            
            for row in reader:
                name = row['name'].strip()
                price = float(row['price'].replace(',', '.')) # На случай если в CSV запятые
                section_name = row['section'].strip()
                
                cat_id = category_cache.get(section_name)
                
                if cat_id:
                    new_product = Product(
                        name=name,
                        price_retail=price,
                        price_purchase=0.0, # Укажи закупочную, если она есть
                        category_id=cat_id,
                        kit=False
                    )
                    session.add(new_product)
                    product_count += 1
                else:
                    print(f"Предупреждение: Категория '{section_name}' не найдена для товара {name}")

        session.commit()
        print(f"Миграция завершена! Добавлено товаров: {product_count}")

        session.execute(text("ALTER TABLE orders ALTER COLUMN address_id DROP NOT NULL"))
        session.commit()
        print("Адрес в заказах сделан nullable")

    except Exception as e:
        session.rollback()
        print(f"Произошла ошибка: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    migrate()