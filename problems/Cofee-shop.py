from abc import ABC, abstractmethod

# 1. Component: Abstract Coffee interface
#  Decorater
class Coffee(ABC):
    """Abstract base class for all coffee types"""
    
    def __init__(self):
        self.description = "Unknown Coffee"
    
    def get_description(self):
        """Get the description of the coffee"""
        return self.description
    
    @abstractmethod
    def get_cost(self):
        """Get the cost of the coffee"""
        pass
    
    def get_ingredients(self):
        """Get the ingredients list"""
        return self.get_description()

# 2. Concrete Components: Different types of coffee
class Espresso(Coffee):
    """Espresso coffee - rich and strong"""
    
    def __init__(self):
        super().__init__()
        self.description = "Espresso"
    
    def get_cost(self):
        return 1.99

class HouseBlend(Coffee):
    """House blend coffee - smooth and balanced"""
    
    def __init__(self):
        super().__init__()
        self.description = "House Blend Coffee"
    
    def get_cost(self):
        return 0.89

class DarkRoast(Coffee):
    """Dark roast coffee - bold and intense"""
    
    def __init__(self):
        super().__init__()
        self.description = "Dark Roast Coffee"
    
    def get_cost(self):
        return 0.99

class Decaf(Coffee):
    """Decaffeinated coffee - all the taste, no caffeine"""
    
    def __init__(self):
        super().__init__()
        self.description = "Decaf Coffee"
    
    def get_cost(self):
        return 1.05

# 3. Decorator: Abstract condiment decorator
class CondimentDecorator(Coffee):
    """Abstract decorator for condiments"""
    
    def __init__(self, coffee):
        super().__init__()
        self.coffee = coffee
    
    @abstractmethod
    def get_description(self):
        """Must be implemented by concrete decorators"""
        pass
    
    def get_ingredients(self):
        """Get ingredients including the wrapped coffee"""
        return self.get_description()

# 4. Concrete Decorators: Various condiments
class Milk(CondimentDecorator):
    """Milk condiment decorator"""
    
    def __init__(self, coffee):
        super().__init__(coffee)
    
    def get_description(self):
        return self.coffee.get_description() + ", Milk"
    
    def get_cost(self):
        return self.coffee.get_cost() + 0.10

class Mocha(CondimentDecorator):
    """Mocha condiment decorator"""
    
    def __init__(self, coffee):
        super().__init__(coffee)
    
    def get_description(self):
        return self.coffee.get_description() + ", Mocha"
    
    def get_cost(self):
        return self.coffee.get_cost() + 0.20

class Soy(CondimentDecorator):
    """Soy milk condiment decorator"""
    
    def __init__(self, coffee):
        super().__init__(coffee)
    
    def get_description(self):
        return self.coffee.get_description() + ", Soy"
    
    def get_cost(self):
        return self.coffee.get_cost() + 0.15

class Whip(CondimentDecorator):
    """Whipped cream condiment decorator"""
    
    def __init__(self, coffee):
        super().__init__(coffee)
    
    def get_description(self):
        return self.coffee.get_description() + ", Whip"
    
    def get_cost(self):
        return self.coffee.get_cost() + 0.10

class Sugar(CondimentDecorator):
    """Sugar condiment decorator"""
    
    def __init__(self, coffee):
        super().__init__(coffee)
    
    def get_description(self):
        return self.coffee.get_description() + ", Sugar"
    
    def get_cost(self):
        # Sugar is usually free, but let's add a small cost for illustration
        return self.coffee.get_cost() + 0.05

class Vanilla(CondimentDecorator):
    """Vanilla syrup condiment decorator"""
    
    def __init__(self, coffee):
        super().__init__(coffee)
    
    def get_description(self):
        return self.coffee.get_description() + ", Vanilla"
    
    def get_cost(self):
        return self.coffee.get_cost() + 0.15

class Caramel(CondimentDecorator):
    """Caramel syrup condiment decorator"""
    
    def __init__(self, coffee):
        super().__init__(coffee)
    
    def get_description(self):
        return self.coffee.get_description() + ", Caramel"
    
    def get_cost(self):
        return self.coffee.get_cost() + 0.15

# Coffee Shop Order System
class CoffeeShop:
    """Coffee shop class to demonstrate the decorator pattern"""
    
    @staticmethod
    def print_order(coffee):
        """Print the coffee order details"""
        print(f"Order: {coffee.get_description()}")
        print(f"Cost: ${coffee.get_cost():.2f}")
        print(f"Ingredients: {coffee.get_ingredients()}")
        print("-" * 50)

# Example usage and testing
if __name__ == "__main__":
    shop = CoffeeShop()
    
    print("=== COFFEE SHOP DECORATOR PATTERN DEMO ===\n")
    
    # Order 1: Simple Espresso
    print("Order 1: Simple Espresso")
    beverage = Espresso()
    shop.print_order(beverage)
    
    # Order 2: Dark Roast with Soy and Mocha
    print("Order 2: Dark Roast with Soy and Mocha")
    beverage2 = DarkRoast()
    beverage2 = Soy(beverage2)
    beverage2 = Mocha(beverage2)
    shop.print_order(beverage2)
    
    # Order 3: House Blend with multiple condiments
    print("Order 3: House Blend with Whip, Mocha, and Milk")
    beverage3 = HouseBlend()
    beverage3 = Whip(beverage3)
    beverage3 = Mocha(beverage3)
    beverage3 = Milk(beverage3)
    shop.print_order(beverage3)
    
    # Order 4: Complex order - Decaf with everything!
    print("Order 4: Decaf with Sugar, Vanilla, Caramel, and Whip")
    beverage4 = Decaf()
    beverage4 = Sugar(beverage4)
    beverage4 = Vanilla(beverage4)
    beverage4 = Caramel(beverage4)
    beverage4 = Whip(beverage4)
    shop.print_order(beverage4)
    
    # Order 5: Double condiments
    print("Order 5: Espresso with Double Mocha and Double Whip")
    beverage5 = Espresso()
    beverage5 = Mocha(beverage5)
    beverage5 = Mocha(beverage5)  # Double mocha
    beverage5 = Whip(beverage5)
    beverage5 = Whip(beverage5)   # Double whip
    shop.print_order(beverage5)
    
    # Order 6: Method chaining style
    print("Order 6: Method chaining style - House Blend with Soy, Sugar, and Vanilla")
    beverage6 = Vanilla(Sugar(Soy(HouseBlend())))
    shop.print_order(beverage6)
    
    print("\n=== DECORATOR PATTERN BENEFITS DEMONSTRATED ===")
    print("✓ Dynamic behavior addition at runtime")
    print("✓ Flexible combination of features")
    print("✓ No class explosion (imagine creating a class for every combination!)")
    print("✓ Open/Closed principle - easily add new condiments without modifying existing code")
    print("✓ Composition over inheritance")