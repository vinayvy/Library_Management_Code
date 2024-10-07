#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
from datetime import datetime, timedelta


# In[ ]:


import csv
from datetime import datetime, timedelta

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class Book:
    def __init__(self, book_id, title, author, genre, copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.copies = copies
        self.issued_to = None

class Member:
    def __init__(self, member_id, name, membership_type):
        self.member_id = member_id
        self.name = name
        self.membership_type = membership_type
        self.issued_books = []
        self.fines = 0

    def issue_book(self, book):
        self.issued_books.append((book, datetime.now()))
    
    def return_book(self, book):
        self.issued_books.remove(book)
    
    def calculate_fine(self, book_id):
        fine_per_day = 1  # $1 per day overdue
        for book, issue_date in self.issued_books:
            if book.book_id == book_id:
                days_overdue = (datetime.now() - issue_date).days - 14  # Assuming 14 days borrowing period
                if days_overdue > 0:
                    self.fines += days_overdue * fine_per_day
        return self.fines
    
    def pay_fine(self, amount):
        if amount >= self.fines:
            self.fines = 0
            return "Fine paid successfully."
        else:
            return f"Partial payment accepted. Remaining fine: ${self.fines - amount}"

class Library:
    def __init__(self):
        self.books = self.load_books()
        self.members = self.load_members()
        self.users = self.load_users()
    
    def load_books(self):
        books = {}
        with open(r'C:\Users\acer\Downloads\Library Mangement\library\library\books.csv' ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                book = Book(int(row['book_id']), row['title'], row['author'], row['genre'], int(row['copies']))
                books[book.book_id] = book
        return books
    
    def load_members(self):
        members = {}
        with open(r'C:\Users\acer\Downloads\Library Mangement\library\library\members.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                member = Member(int(row['member_id']), row['name'], row['membership_type'])
                members[member.member_id] = member
        return members

    def load_users(self):
        users = {}
        with open(r'C:\Users\acer\Downloads\Library Mangement\library\library\users.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row['username']] = row['password']
        return users

    def authenticate(self, username, password):
        if username in self.users and self.users[username] == password:
            if username == 'admin':
                return User(username, password, 'admin')
            else:
                return User(username, password, 'user')
        return None

    def add_book(self, book_id, title, author, genre, copies):
        if book_id in self.books:
            return "Book ID already exists."
        self.books[book_id] = Book(book_id, title, author, genre, copies)
        return "Book added successfully."

    def add_member(self, member_id, name, membership_type):
        if member_id in self.members:
            return "Member ID already exists."
        self.members[member_id] = Member(member_id, name, membership_type)
        return "Member added successfully."

    def update_book(self, book_id, title=None, author=None, genre=None, copies=None):
        if book_id not in self.books:
            return "Book ID does not exist."
        book = self.books[book_id]
        if title:
            book.title = title
        if author:
            book.author = author
        if genre:
            book.genre = genre
        if copies is not None:
            book.copies = copies
        return "Book updated successfully."

    def update_member(self, member_id, name=None, membership_type=None):
        if member_id not in self.members:
            return "Member ID does not exist."
        member = self.members[member_id]
        if name:
            member.name = name
        if membership_type:
            member.membership_type = membership_type
        return "Member updated successfully."

    def issue_book(self, member_id, book_id):
        if member_id not in self.members:
            return "Member ID does not exist."
        if book_id not in self.books:
            return "Book ID does not exist."
        book = self.books[book_id]
        member = self.members[member_id]
        if book.copies <= 0:
            return "No copies available."
        book.copies -= 1
        member.issue_book(book)
        return "Book issued successfully."

    def return_book(self, member_id, book_id):
        if member_id not in self.members:
            return "Member ID does not exist."
        if book_id not in self.books:
            return "Book ID does not exist."
        member = self.members[member_id]
        book = self.books[book_id]
        if (book, datetime.now()) in member.issued_books:
            member.return_book((book, datetime.now()))
            book.copies += 1
            fine = member.calculate_fine(book_id)
            if fine > 0:
                return f"Book returned. You have a fine of ${fine}. Please pay your fine."
            return "Book returned successfully."
        return "This book was not issued to this member."

    def pay_fine(self, member_id, amount):
        if member_id not in self.members:
            return "Member ID does not exist."
        member = self.members[member_id]
        return member.pay_fine(amount)

    def search_books(self, query):
        results = [book for book in self.books.values() if query.lower() in book.title.lower() or query.lower() in book.author.lower()]
        return results if results else "No books found."

    def list_available_books(self):
        available_books = [f"{book.title} by {book.author} - Copies available: {book.copies}" for book in self.books.values() if book.copies > 0]
        return available_books if available_books else "No books available."

    def list_issued_books(self):
        issued_books = [(book.title, member.name) for member in self.members.values() for book, _ in member.issued_books if member.issued_books]
        return issued_books if issued_books else "No books issued."

    def overdue_books(self):
        overdue_list = []
        for member in self.members.values():
            for book, issue_date in member.issued_books:
                fine = member.calculate_fine(book.book_id)
                if fine > 0:
                    overdue_list.append((book.title, member.name, fine))
        return overdue_list if overdue_list else "No overdue books."

# Initialize the library
library = Library()

# Command Line Interface
def library_menu():
    print("\nWelcome to the Library Management System")
    print("1. Login as Admin")
    print("2. Login as User")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        admin_menu()
    elif choice == "2":
        user_menu()
    elif choice == "3":
        exit()
    else:
        print("Invalid choice. Try again.")
        library_menu()

def admin_menu():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    admin = library.authenticate(username, password)

    if admin and admin.role == "admin":
        print(f"Welcome, {admin.username} (Admin)")
        while True:
            print("\nAdmin Menu:")
            print("1. Add Book")
            print("2. Add Member")
            print("3. Update Book")
            print("4. Update Member")
            print("5. View Available Books")
            print("6. View Issued Books")
            print("7. View Overdue Books")
            print("8. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                book_id = int(input("Enter book ID: "))
                title = input("Enter title: ")
                author = input("Enter author: ")
                genre = input("Enter genre: ")
                copies = int(input("Enter number of copies: "))
                print(library.add_book(book_id, title, author, genre, copies))
            elif choice == "2":
                member_id = int(input("Enter member ID: "))
                name = input("Enter member name: ")
                membership_type = input("Enter membership type: ")
                print(library.add_member(member_id, name, membership_type))
            elif choice == "3":
                book_id = int(input("Enter book ID: "))
                title = input("Enter title (leave blank to skip): ")
                author = input("Enter author (leave blank to skip): ")
                genre = input("Enter genre (leave blank to skip): ")
                copies = input("Enter number of copies (leave blank to skip): ")
                if copies:
                    copies = int(copies)
                else:
                    copies = None
                print(library.update_book(book_id, title, author, genre, copies))
            elif choice == "4":
                member_id = int(input("Enter member ID: "))
                name = input("Enter member name (leave blank to skip): ")
                membership_type = input("Enter membership type (leave blank to skip): ")
                print(library.update_member(member_id, name, membership_type))
            elif choice == "5":
                print("Available Books:")
                print(library.list_available_books())
            elif choice == "6":
                print("Issued Books:")
                print(library.list_issued_books())
            elif choice == "7":
                print("Overdue Books:")
                print(library.overdue_books())
            elif choice == "8":
                library_menu()
            else:
                print("Invalid choice. Try again.")
    
    else:
        print("Invalid admin credentials.")
        library_menu()

def user_menu():
    username = input("Enter username: ")
    password = input("Enter password: ")

    user = library.authenticate(username, password)

    if user and user.role == "user":
        print(f"Welcome, {user.username} (User)")
        while True:
            print("\nUser Menu:")
            print("1. Issue Book")
            print("2. Return Book")
            print("3. Pay Fine")
            print("4. View Available Books")
            print("5. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                member_id = int(input("Enter your member ID: "))
                book_id = int(input("Enter book ID to issue: "))
                print(library.issue_book(member_id, book_id))
            elif choice == "2":
                member_id = int(input("Enter your member ID: "))
                book_id = int(input("Enter book ID to return: "))
                print(library.return_book(member_id, book_id))
            elif choice == "3":
                member_id = int(input("Enter your member ID: "))
                amount = float(input("Enter amount to pay: "))
                print(library.pay_fine(member_id, amount))
            elif choice == "4":
                print("Available Books:")
                print(library.list_available_books())
            elif choice == "5":
                library_menu()
            else:
                print("Invalid choice. Try again.")

# Run the library management system
library_menu()




# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




