# librarymanagemnet.py
# Name:Rishabh Bhardwaj
#Rollno- 2501730355
# ---------------------- Book Class ----------------------
class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def __str__(self):
        return f"{self.title} | {self.author} | {self.isbn} | {self.status}"


# ---------------------- Inventory Manager ----------------------
class LibraryInventory:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        if not self.books:
            print("No books in the library.")
        else:
            for b in self.books:
                print(b)


# ---------------------- CLI MENU ----------------------
def menu():
    inventory = LibraryInventory()

    while True:
        print("\n----- Library Menu -----")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            title = input("Title: ")
            author = input("Author: ")
            isbn = input("ISBN: ")
            inventory.add_book(Book(title, author, isbn))
            print("Book added successfully.")

        elif choice == "2":
            isbn = input("Enter ISBN to issue: ")
            book = inventory.search_by_isbn(isbn)
            if book and book.issue():
                print("Book issued!")
            else:
                print("Book not available or not found.")

        elif choice == "3":
            isbn = input("Enter ISBN to return: ")
            book = inventory.search_by_isbn(isbn)
            if book and book.return_book():
                print("Book returned!")
            else:
                print("Book not found or already available.")

        elif choice == "4":
            inventory.display_all()

        elif choice == "5":
            title = input("Enter title to search: ")
            results = inventory.search_by_title(title)
            if results:
                for b in results:
                    print(b)
            else:
                print("No matching books found.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


# Run program
menu()
