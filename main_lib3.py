import json

# Function to add a new book
def add_book(books):
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    publication_year = int(input("Enter the publication year: "))

    new_book = {
        "title": title,
        "author": author,
        "publication_year": publication_year,
        "borrowed": False,
        "due_date": None,
        "borrowed_by": None
    }
    books.append(new_book)
    print("Book added successfully!\n")
    return books

# Function to edit a book
def edit_book(books):
    title = input("Enter the title of the book to edit: ").strip().lower()

    for book in books:
        if book["title"].lower() == title:
            new_title = input("Enter the new title (leave blank to keep current): ").strip()
            new_author = input("Enter the new author (leave blank to keep current): ").strip()
            new_year = input("Enter the new publication year (leave blank to keep current): ").strip()

            if new_title:
                book["title"] = new_title
            if new_author:
                book["author"] = new_author
            if new_year:
                book["publication_year"] = int(new_year)

            print("Book updated successfully!\n")
            return books

    print("Book not found.\n")
    return books

# Function to borrow a book
def borrow_book(books):
    book_title = input("Enter the title of the book to borrow: ").strip().lower()
    for book in books:
        if book["title"].lower() == book_title:
            if book["borrowed"]:
                print("Sorry, this book is already borrowed.")
                return books
            else:
                borrower_name = input("Enter your name: ")
                return_date = input("Enter the return date (DD/MM/YYYY): ")
                book["borrowed"] = True
                book["due_date"] = return_date
                book["borrowed_by"] = borrower_name
                print("You have successfully borrowed the book.")
                return books

    print("No book found with the given title.")
    return books

# Function to return a book
def return_book(books):
    book_title = input("Enter the title of the book to return: ").strip().lower()
    for book in books:
        if book["title"].lower() == book_title:
            if not book["borrowed"]:
                print("This book is not borrowed.")
                return books
            else:
                book["borrowed"] = False
                book["due_date"] = None
                book["borrowed_by"] = None
                print(f"The book '{book['title']}' has been successfully returned.")
                return books

    print("No book found with the given title.")
    return books

# Function to filter books by a specific field
def filter_books(books):
    filter_field = input("Enter the field to filter by (author, publication_year): ").strip().lower()
    filter_value = input("Enter the value to filter by: ").strip()

    if filter_field == "publication_year":
        filter_value = int(filter_value)

    filtered_books = [
        book for book in books if book.get(filter_field, None) == filter_value
    ]

    if filtered_books:
        print("Filtered books:")
        for book in filtered_books:
            print(json.dumps(book, indent=2))
    else:
        print("No books match the given criteria.")

# Function to search for books by title or author
def search_books(books):
    search_query = input("Enter the title or author to search: ").strip().lower()
    found_books = []
    for book in books:
        if search_query in book["title"].lower() or search_query in book["author"].lower():
            found_books.append(book)

    if found_books:
        print("Books found:")
        for book in found_books:
            print(json.dumps(book, indent=2))
    else:
        print("No books found for the given query.")

# Function to validate login
def login(filename, role):
    with open(filename, "r") as file:
        users = json.load(file)[role]

    username = input(f"Enter {role} username: ").strip()
    password = input(f"Enter {role} password: ").strip()

    for user in users:
        if user["user_name"] == username and user["password"] == password:
            print(f"Login successful. Welcome, {role.capitalize()}!")
            return True

    print("Invalid username or password.")
    return False

# Function to add a user or admin
def add_user_or_admin(filename, role):
    with open(filename, "r") as file:
        data = json.load(file)

    username = input(f"Enter new {role} username: ").strip()
    password = input(f"Enter new {role} password: ").strip()

    new_entry = {
        "user_name": username,
        "password": password
    }

    data[role].append(new_entry)

    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

    print(f"New {role} added successfully!")

# Function to manage library
if __name__ == "__main__":
    with open("books.json", "r") as file:
        data = json.load(file)

    books = data["books"]
while True:
    print("Choose your role:")
    print("1. User")
    print("2. Admin")
    print("3. Exit")
    role_choice = input("Enter your role (1/2/3): ").strip()

    if role_choice == "1":
        if login("Users.json", "users"):
            while True:
                print("\nUser Menu:")
                print("1. View all books")
                print("2. Search books")
                print("3. Borrow a book")
                print("4. Return a book")
                print("5. Filter books")
                print("6. Save & Exit")

                user_choice = input("Enter your choice: ").strip()

                if user_choice == "1":
                    print(json.dumps(books, indent=2))
                elif user_choice == "2":
                    search_books(books)
                elif user_choice == "3":
                    books = borrow_book(books)
                elif user_choice == "4":
                    books = return_book(books)
                elif user_choice == "5":
                    filter_books(books)
                elif user_choice == "6":
                    with open("books.json", "w") as file:
                        json.dump({"books": books}, file, indent=2)
                    print("Changes saved.")
                    break
                else:
                    print("Invalid choice. Please try again.")

    elif role_choice == "2":
        if login("Admins.json", "admins"):
            while True:
                print("\nAdmin Menu:")
                print("1. View all books")
                print("2. Search books")
                print("3. Add a book")
                print("4. Edit a book")
                print("5. Filter books")
                print("6. Add a User")
                print("7. Add an Admin")
                print("8. Save & Exit")

                admin_choice = input("Enter your choice: ").strip()

                if admin_choice == "1":
                    print(json.dumps(books, indent=2))
                elif admin_choice == "2":
                    search_books(books)
                elif admin_choice == "3":
                    books = add_book(books)
                elif admin_choice == "4":
                    books = edit_book(books)
                elif admin_choice == "5":
                    filter_books(books)
                elif admin_choice == "6":
                    add_user_or_admin("Users.json", "users")
                elif admin_choice == "7":
                    add_user_or_admin("Admins.json", "admins")
                elif admin_choice == "8":
                    with open("books.json", "w") as file:
                        json.dump({"books": books}, file, indent=2)
                    print("Changes saved.")
                    break
                else:
                    print("Invalid choice. Please try again.")
    elif role_choice == "3":
        print("You exited the program. Goodbye!")
        break

    else:
        print("Invalid role choice. Please choose from those choices (1/2/3) .")
