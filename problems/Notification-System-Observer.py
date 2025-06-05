# Simple Notification System using Observer Pattern
# This is a classic interview question!

from abc import ABC, abstractmethod
from typing import List

# 1. Observer Interface - things that want to be notified
class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

# 2. Subject Interface - things that send notifications
class Subject(ABC):
    @abstractmethod
    def add_observer(self, observer: Observer):
        pass
    
    @abstractmethod
    def remove_observer(self, observer: Observer):
        pass
    
    @abstractmethod
    def notify_observers(self, message: str):
        pass

# 3. Concrete Subject - News Agency that publishes news
class NewsAgency(Subject):
    def __init__(self):
        self._observers: List[Observer] = []
        self._latest_news = ""
    
    def add_observer(self, observer: Observer):
        self._observers.append(observer)
        print(f"Observer added. Total observers: {len(self._observers)}")
    
    def remove_observer(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"Observer removed. Total observers: {len(self._observers)}")
    
    def notify_observers(self, message: str):
        print(f"\n📢 Broadcasting: {message}")
        for observer in self._observers:
            observer.update(message)
    
    def publish_news(self, news: str):
        self._latest_news = news
        self.notify_observers(news)

# 4. Concrete Observers - Different types of subscribers

class EmailSubscriber(Observer):
    def __init__(self, email: str):
        self.email = email
    
    def update(self, message: str):
        print(f"📧 Email sent to {self.email}: {message}")

class SMSSubscriber(Observer):
    def __init__(self, phone: str):
        self.phone = phone
    
    def update(self, message: str):
        print(f"📱 SMS sent to {phone_format(self.phone)}: {message[:50]}...")

class AppNotificationSubscriber(Observer):
    def __init__(self, username: str):
        self.username = username
    
    def update(self, message: str):
        print(f"📲 App notification for @{self.username}: {message}")

class SlackSubscriber(Observer):
    def __init__(self, channel: str):
        self.channel = channel
    
    def update(self, message: str):
        print(f"💬 Slack message in #{self.channel}: {message}")

# Helper function
def phone_format(phone: str) -> str:
    return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"

# Demo usage
if __name__ == "__main__":
    print("=== Simple Notification System Demo ===\n")
    
    # Create the news agency (subject)
    news_agency = NewsAgency()
    
    # Create subscribers (observers)
    email_sub1 = EmailSubscriber("alice@example.com")
    email_sub2 = EmailSubscriber("bob@example.com")
    sms_sub = SMSSubscriber("5551234567")
    app_sub = AppNotificationSubscriber("charlie")
    slack_sub = SlackSubscriber("general")
    
    # Subscribe to news
    print("🔔 Setting up subscriptions...")
    news_agency.add_observer(email_sub1)
    news_agency.add_observer(sms_sub)
    news_agency.add_observer(app_sub)
    
    # Publish some news
    news_agency.publish_news("Breaking: New Python version released!")
    
    # Add more subscribers
    print(f"\n➕ Adding more subscribers...")
    news_agency.add_observer(email_sub2)
    news_agency.add_observer(slack_sub)
    
    # Publish more news
    news_agency.publish_news("Tech Update: AI breakthrough announced!")
    
    # Remove a subscriber
    print(f"\n➖ Removing SMS subscriber...")
    news_agency.remove_observer(sms_sub)
    
    # Final news
    news_agency.publish_news("Sports: Local team wins championship!")
    
    print(f"\n=== Pattern Benefits ===")
    print("✅ Loose coupling: News agency doesn't need to know about specific subscribers")
    print("✅ Dynamic relationships: Can add/remove subscribers at runtime")
    print("✅ Broadcast communication: One news reaches all subscribers automatically")
    print("✅ Easy to extend: Can add new subscriber types without changing existing code")

# Bonus: Simple example with built-in Python features
print(f"\n" + "="*60)
print("🐍 BONUS: Python-style Observer with callbacks")

class SimpleNewsAgency:
    def __init__(self):
        self.subscribers = []
    
    def subscribe(self, callback):
        self.subscribers.append(callback)
    
    def unsubscribe(self, callback):
        if callback in self.subscribers:
            self.subscribers.remove(callback)
    
    def publish(self, news):
        print(f"\n📢 {news}")
        for callback in self.subscribers:
            callback(news)

# Usage with lambda functions
simple_agency = SimpleNewsAgency()

# Subscribe with simple functions
simple_agency.subscribe(lambda news: print(f"  📧 Email: {news}"))
simple_agency.subscribe(lambda news: print(f"  📱 SMS: {news[:30]}..."))
simple_agency.subscribe(lambda news: print(f"  📲 App: {news}"))

simple_agency.publish("Quick news update!")