# Simple Payment System using Strategy Pattern
# Super common interview question!

from abc import ABC, abstractmethod

# 1. Strategy Interface - defines how to pay
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        pass

# 2. Concrete Strategies - different ways to pay

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str, expiry: str):
        self.card_number = card_number
        self.cvv = cvv
        self.expiry = expiry
    
    def validate(self) -> bool:
        # Simple validation
        return (len(self.card_number) == 16 and 
                len(self.cvv) == 3 and 
                len(self.expiry) == 5)
    
    def pay(self, amount: float) -> str:
        if not self.validate():
            return "❌ Invalid credit card details"
        
        masked_card = "**** **** **** " + self.card_number[-4:]
        return f"💳 Paid ${amount:.2f} using Credit Card {masked_card}"

class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
    
    def validate(self) -> bool:
        return "@" in self.email and len(self.password) >= 6
    
    def pay(self, amount: float) -> str:
        if not self.validate():
            return "❌ Invalid PayPal credentials"
        
        return f"🅿️ Paid ${amount:.2f} using PayPal ({self.email})"

class ApplePayPayment(PaymentStrategy):
    def __init__(self, touch_id: bool = True):
        self.touch_id_enabled = touch_id
        self.authenticated = False
    
    def validate(self) -> bool:
        if self.touch_id_enabled:
            # Simulate biometric authentication
            print("👆 Touch ID authentication...")
            self.authenticated = True
            return True
        return False
    
    def pay(self, amount: float) -> str:
        if not self.validate():
            return "❌ Apple Pay authentication failed"
        
        return f"🍎 Paid ${amount:.2f} using Apple Pay"

class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet_address: str, private_key: str):
        self.wallet_address = wallet_address
        self.private_key = private_key
    
    def validate(self) -> bool:
        return (len(self.wallet_address) == 42 and 
                self.wallet_address.startswith("0x") and
                len(self.private_key) == 64)
    
    def pay(self, amount: float) -> str:
        if not self.validate():
            return "❌ Invalid crypto wallet details"
        
        masked_wallet = self.wallet_address[:6] + "..." + self.wallet_address[-4:]
        return f"₿ Paid ${amount:.2f} using Crypto from wallet {masked_wallet}"

# 3. Context - Shopping Cart that uses different payment strategies
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.payment_strategy: PaymentStrategy = None
    
    def add_item(self, item: str, price: float):
        self.items.append({"item": item, "price": price})
        print(f"➕ Added {item} - ${price:.2f}")
    
    def get_total(self) -> float:
        return sum(item["price"] for item in self.items)
    
    def set_payment_method(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy
        print(f"💰 Payment method set: {strategy.__class__.__name__}")
    
    def checkout(self) -> str:
        if not self.payment_strategy:
            return "❌ No payment method selected!"
        
        if not self.items:
            return "❌ Cart is empty!"
        
        total = self.get_total()
        print(f"\n🧾 Cart total: ${total:.2f}")
        print("Items:")
        for item in self.items:
            print(f"  - {item['item']}: ${item['price']:.2f}")
        
        # Process payment using the selected strategy
        result = self.payment_strategy.pay(total)
        
        if "❌" not in result:
            self.items.clear()  # Clear cart after successful payment
            return result + " ✅ Order confirmed!"
        
        return result

# Demo usage
if __name__ == "__main__":
    print("=== Simple Payment System Demo ===\n")
    
    # Create shopping cart
    cart = ShoppingCart()
    
    # Add some items
    cart.add_item("Laptop", 999.99)
    cart.add_item("Mouse", 29.99)
    cart.add_item("Keyboard", 79.99)
    
    print(f"\n💰 Total: ${cart.get_total():.2f}")
    
    # Try different payment methods
    
    # 1. Credit Card Payment
    print(f"\n" + "="*50)
    print("💳 Trying Credit Card Payment...")
    credit_card = CreditCardPayment("1234567890123456", "123", "12/25")
    cart.set_payment_method(credit_card)
    result = cart.checkout()
    print(result)
    
    # Add items again for next demo
    cart.add_item("Headphones", 199.99)
    cart.add_item("Cable", 19.99)
    
    # 2. PayPal Payment
    print(f"\n" + "="*50)
    print("🅿️ Trying PayPal Payment...")
    paypal = PayPalPayment("user@example.com", "mypassword123")
    cart.set_payment_method(paypal)
    result = cart.checkout()
    print(result)
    
    # Add items again
    cart.add_item("Phone Case", 24.99)
    
    # 3. Apple Pay
    print(f"\n" + "="*50)
    print("🍎 Trying Apple Pay...")
    apple_pay = ApplePayPayment(touch_id=True)
    cart.set_payment_method(apple_pay)
    result = cart.checkout()
    print(result)
    
    # Add items again
    cart.add_item("Crypto Course", 99.99)
    
    # 4. Crypto Payment
    print(f"\n" + "="*50)
    print("₿ Trying Crypto Payment...")
    crypto = CryptoPayment("0x1234567890abcdef1234567890abcdef12345678", "a" * 64)
    cart.set_payment_method(crypto)
    result = cart.checkout()
    print(result)
    
    # 5. Failed payment example
    print(f"\n" + "="*50)
    print("❌ Trying Invalid Credit Card...")
    cart.add_item("Book", 15.99)
    invalid_card = CreditCardPayment("123", "12", "1/1")  # Invalid details
    cart.set_payment_method(invalid_card)
    result = cart.checkout()
    print(result)
    
    print(f"\n=== Strategy Pattern Benefits ===")
    print("✅ Easy to switch payment methods at runtime")
    print("✅ Adding new payment methods doesn't change existing code")
    print("✅ Each payment method handles its own logic")
    print("✅ Clean separation of concerns")
    print("✅ Easy to test each payment method independently")

# Bonus: Even simpler version using just functions
print(f"\n" + "="*60)
print("🐍 BONUS: Function-based Strategy Pattern")

def credit_card_pay(amount, card_number):
    return f"💳 Paid ${amount:.2f} with card ending {card_number[-4:]}"

def paypal_pay(amount, email):
    return f"🅿️ Paid ${amount:.2f} via PayPal ({email})"

def apple_pay_pay(amount):
    return f"🍎 Paid ${amount:.2f} with Apple Pay"

class SimpleCart:
    def __init__(self):
        self.total = 0
        self.payment_function = None
    
    def set_payment(self, pay_func, *args):
        self.payment_function = lambda amount: pay_func(amount, *args)
    
    def pay(self, amount):
        if self.payment_function:
            return self.payment_function(amount)
        return "No payment method set"

# Usage
simple_cart = SimpleCart()
simple_cart.set_payment(credit_card_pay, "1234567890123456")
print(simple_cart.pay(50.00))

simple_cart.set_payment(paypal_pay, "user@email.com")
print(simple_cart.pay(75.50))