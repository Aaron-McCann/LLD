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