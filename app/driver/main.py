# example_usage.py
from receipt_template import ReceiptTemplate
from tspl_init import TSPLTemplate  # наш класс из предыдущего ответа

def print_order_receipt(order_data):
    """Печать чека заказа"""
    
    # Создаем шаблон
    receipt = ReceiptTemplate(width_mm=60)
    
    # Заполняем данными
    (receipt
        .add_header("ПИЦЦЕРИЯ 'МАРГАРИТА'", "пр. Мира, 15")
        .add_order_info(
            order_id=order_data['id'],
            table=order_data.get('table'),
            waiter=order_data.get('waiter')
        )
        .add_items_list(order_data['items'])
        .add_total(
            subtotal=order_data['subtotal'],
            discount=order_data.get('discount', 0),
            delivery=order_data.get('delivery', 0)
        )
        .add_payment_info(
            payment_type=order_data['payment_type'],
            amount=order_data['paid'],
            change=order_data.get('change', 0)
        )
        .add_footer(
            thank_you="ЖДЕМ ВАС СНОВА!",
            promo="Instagram: @pizzamargarita"
        )
        .copies(1)  # 1 копия
    )
    
    # Получаем команды TSPL
    commands = receipt.render()
    print("Сгенерированные команды:")
    print(commands)
    
    # Отправляем на печать
    printer = TSPLTemplate()  # для Windows
    # printer = TSPLPrinter()  # для Linux (автоматически найдет /dev/usb/lp*)
    
    printer.print_to_printer()
    
    # Для отладки можно сохранить в файл
    receipt.save_to_file(f"order_{order_data['id']}.tspl")

# Пример данных заказа
order = {
    'id': 1234,
    'table': 5,
    'waiter': 'Анна',
    'items': [
        {'name': 'Пицца Маргарита', 'qty': 1, 'price': 450},
        {'name': 'Латте', 'qty': 2, 'price': 180},
        {'name': 'Тирамису', 'qty': 1, 'price': 320, 'special': 'без сахара'}
    ],
    'subtotal': 450 + 360 + 320,  # 1130
    'discount': 50,
    'delivery': 0,
    'payment_type': 'card',
    'paid': 1130,
    'change': 0
}

print_order_receipt(order)