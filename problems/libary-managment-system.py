# Q: Design a Libary Managment System 

"""
Clarifying requirements:

- Who is going to use the system? 
    - Libarian 
    - Libary Members
    - Sys Admin 

- Will there be different access rights for different users? 
    - Libary Members : can search for/borrow/return books + view their borrowing history + manage their profile
    - Librarians: all member privalleges + add/ remove books + manage member accounts + handle overdue books + process fines
    - Sys Admin: full system access including user management + system configuration
    
- What actions can users take?
    - already answered above 


- Questions i didnt get to : 

    - What types of items can be borrowed?
        - Just books

    - How long can the items be borrowed for? 
        - 2 weeks with one renewal possible

    - Can users reserve books that are already checked out? 
        - users can reserve books that are checked out

    - How many concurrent users 
        - 100

    - How many copies of the same book can exist? 
        - multiple copies 

    - How much does it cost to take out a book? 
        - free

    - How many books can one user check out at once? 
        - 5 

    - Should the system send notifications? 
        - emails for due dates and reservations 

    - How many books are in the system? 
        - 10,000

"""

# Identifying Entities

"""
1. Lib member
2. Admin 
3. Librarian 
4. Book 
5. Borrow
6. Reserve 

"""

# Relatiionship between Entities

"""
LibMember:

Can have many Borrows (1-to-many)
Can have many Reserves (1-to-many)

Book:
Can have many Borrows over time (1-to-many)
Can have many Reserves (1-to-many)

Borrow:
Belongs to one LibMember (many-to-1)
Associated with one Book (many-to-1)

Reserve:
Belongs to one LibMember (many-to-1)
Associated with one Book (many-to-1)
"""


# Classes and attributes

"""
LibMember: 
- Name
- Age 
- Number

Admin:
-Name
-EmployeeId
-Email
-Password

Librarian:
-Name
-EmployeeId
-Email
-Password

Book: 
- Name
- Author
- Copy number
- Curr Availiable 
- Curr Borrowed


Borrowed: 
- Book
- Member
- Borrowed Date
- Due Date
- Return Date
- Status

Reserve:
-Book
-Member
-ReservedDate
-Status (ACTIVE, FULFILLED, CANCELLED)
-Priority/Position (if multiple people reserve the same book)

"""

# Methods and interfaces

"""
Approach:
- Define key methods for each entity (Book, Member, Borrow, Reserve)
- Create LibraryManager class to handle main business operations
- Add basic validation and edge case handling
- Keep entities simple - mostly data + basic operations
- Manager handles complex workflows like borrowing/returning/reserving

Entity methods:
- Book: availability checks, borrow/return logic
- Member: borrowing limits, validation
- Borrow/Reserve: status management

LibraryManager methods:
- borrowBook(), returnBook(), reserveBook()
- searchBooks(), addBook(), addMember()
- Basic business rule enforcement

"""

from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional

class BorrowStatus(Enum):
    ACTIVE = "active"
    RETURNED = "returned"

class ReserveStatus(Enum):
    ACTIVE = "active"
    FULFILLED = "fulfilled"

# Entities
class LibMember:
    def __init__(self, name: str, member_id: str, age: int):
        self.name = name
        self.member_id = member_id
        self.age = age
        self.current_borrows: List['Borrow'] = []
    
    def can_borrow(self) -> bool:
        return len(self.current_borrows) < 5

class Book:
    def __init__(self, book_id: str, name: str, author: str, total_copies: int):
        self.book_id = book_id
        self.name = name
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies
    
    def is_available(self) -> bool:
        return self.available_copies > 0

class Borrow:
    def __init__(self, borrow_id: str, book: Book, member: LibMember):
        self.borrow_id = borrow_id
        self.book = book
        self.member = member
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + timedelta(days=14)
        self.return_date: Optional[datetime] = None
        self.status = BorrowStatus.ACTIVE

class Reserve:
    def __init__(self, reserve_id: str, book: Book, member: LibMember):
        self.reserve_id = reserve_id
        self.book = book
        self.member = member
        self.reserve_date = datetime.now()
        self.status = ReserveStatus.ACTIVE

class Librarian:
    def __init__(self, name: str, employee_id: str):
        self.name = name
        self.employee_id = employee_id

class Admin:
    def __init__(self, name: str, employee_id: str):
        self.name = name
        self.employee_id = employee_id

# Main Library Manager
class LibraryManager:
    def __init__(self):
        self.books = {}  # book_id -> Book
        self.members = {}  # member_id -> LibMember
        self.borrows = {}  # borrow_id -> Borrow
        self.reserves = {}  # reserve_id -> Reserve
        self.borrow_counter = 0
        self.reserve_counter = 0
    
    # Book operations
    def add_book(self, book_id: str, name: str, author: str, copies: int):
        self.books[book_id] = Book(book_id, name, author, copies)
    
    def search_books(self, query: str) -> List[Book]:
        results = []
        for book in self.books.values():
            if query.lower() in book.name.lower() or query.lower() in book.author.lower():
                results.append(book)
        return results
    
    # Member operations
    def add_member(self, member_id: str, name: str, age: int):
        self.members[member_id] = LibMember(name, member_id, age)
    
    # Borrow operations
    def borrow_book(self, member_id: str, book_id: str) -> bool:
        if member_id not in self.members or book_id not in self.books:
            return False
        
        member = self.members[member_id]
        book = self.books[book_id]
        
        if not member.can_borrow() or not book.is_available():
            return False
        
        # Create borrow record
        self.borrow_counter += 1
        borrow_id = f"BOR{self.borrow_counter}"
        borrow = Borrow(borrow_id, book, member)
        
        # Update records
        book.available_copies -= 1
        member.current_borrows.append(borrow)
        self.borrows[borrow_id] = borrow
        
        return True
    
    def return_book(self, borrow_id: str) -> bool:
        if borrow_id not in self.borrows:
            return False
        
        borrow = self.borrows[borrow_id]
        if borrow.status != BorrowStatus.ACTIVE:
            return False
        
        # Update records
        borrow.status = BorrowStatus.RETURNED
        borrow.return_date = datetime.now()
        borrow.book.available_copies += 1
        borrow.member.current_borrows.remove(borrow)
        
        return True
    
    # Reserve operations
    def reserve_book(self, member_id: str, book_id: str) -> bool:
        if member_id not in self.members or book_id not in self.books:
            return False
        
        member = self.members[member_id]
        book = self.books[book_id]
        
        if book.is_available():  # No need to reserve if available
            return False
        
        self.reserve_counter += 1
        reserve_id = f"RES{self.reserve_counter}"
        reserve = Reserve(reserve_id, book, member)
        self.reserves[reserve_id] = reserve
        
        return True
    
    # Utility methods
    def get_member_books(self, member_id: str) -> List[Book]:
        if member_id not in self.members:
            return []
        
        member = self.members[member_id]
        return [borrow.book for borrow in member.current_borrows]
    
    def get_overdue_books(self) -> List[Borrow]:
        overdue = []
        current_time = datetime.now()
        for borrow in self.borrows.values():
            if borrow.status == BorrowStatus.ACTIVE and current_time > borrow.due_date:
                overdue.append(borrow)
        return overdue

# Example Usage
if __name__ == "__main__":
    library = LibraryManager()
    
    # Add books
    library.add_book("B001", "Harry Potter", "J.K. Rowling", 3)
    library.add_book("B002", "1984", "George Orwell", 2)
    
    # Add members
    library.add_member("M001", "John Doe", 25)
    library.add_member("M002", "Jane Smith", 30)
    
    # Borrow book
    print(library.borrow_book("M001", "B001"))  # True
    
    # Search books
    results = library.search_books("Harry")
    print(f"Found {len(results)} books")
    
    # Reserve book
    print(library.reserve_book("M002", "B001"))  # True if all copies borrowed