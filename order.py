from abc import ABC, abstractmethod

# Product 클래스
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# 결제 수단을 위한 추상 클래스
class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

# 카드 결제 클래스
class CardPayment(Payment):
    def pay(self, amount):
        print(f"카드로 {amount}원을 결제했습니다.")

# 계좌 이체 클래스
class BankTransferPayment(Payment):
    def pay(self, amount):
        print(f"계좌 이체로 {amount}원을 결제했습니다.")

# 결제 수단을 생성하는 팩토리 클래스(Factory)
class PaymentFactory:
    @staticmethod
    def create_payment(payment_type):
        if payment_type == "card":
            return CardPayment()
        elif payment_type == "bank_transfer":
            return BankTransferPayment()
        else:
            raise ValueError("Unsupported payment type")

# 주문 클래스
class Order:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def calculate_total_price(self):
        return self.product.price * self.quantity

# 결제 서비스 클래스(Singleton)
class OrderPaymentService:
    def process_order(self, order, payment):
        total_amount = order.product.price * order.quantity
        payment.pay(total_amount)

# 추가 기능을 부여하는 데코레이터 클래스(Decoraotr)
class PaymentDecorator(Payment):
    def __init__(self, payment):
        self._payment = payment

    def pay(self, amount):
        self._payment.pay(amount)

# 보안 기능을 추가한 카드 결제 데코레이터 클래스(Decorator)
class SecureCardPaymentDecorator(PaymentDecorator):
    def pay(self, amount):
        print("보안 기능을 추가합니다.")
        self._payment.pay(amount)

# 로깅 기능을 추가한 계좌 이체 데코레이터 클래스(Decorator)
class LoggingBankTransferPaymentDecorator(PaymentDecorator):
    def pay(self, amount):
        print("결제 내역을 로그에 남깁니다.")
        self._payment.pay(amount)

# 메인 코드
if __name__ == "__main__":
    # 메뉴 보여주기
    print("메뉴:")
    menu = [
        Product("Keyboard", 50),
        Product("Mouse", 30),
        Product("Monitor", 200),
        Product("Headphones", 100)
    ]
    for i, product in enumerate(menu, start=1):
        print(f"{i}. {product.name} - ${product.price}")

    # 상품 선택
    selected_item = int(input("상품 번호를 선택하세요: "))
    selected_product = menu[selected_item - 1]

    # 주문 수량 입력
    quantity = int(input("주문 수량을 입력하세요: "))

    # 주문 생성
    order = Order(selected_product, quantity)

    # 결제 방법 선택
    payment_type = input("결제 방법을 선택하세요 (card 또는 bank_transfer): ")

    # 선택한 결제 수단 생성(Factory)
    payment_factory = PaymentFactory()
    payment_method = payment_factory.create_payment(payment_type)

    # 보안 기능이 추가된 결제 수단 생성(Decorator)
    if payment_type == "card":
        payment_method = SecureCardPaymentDecorator(payment_method)

    # 로깅 기능이 추가된 결제 수단 생성(Decorator)
    if payment_type == "bank_transfer":
        payment_method = LoggingBankTransferPaymentDecorator(payment_method)

    # 결제 서비스 생성(Singleton)
    order_payment_service = OrderPaymentService()

    # 주문 처리 및 결제
    order_payment_service.process_order(order, payment_method)
