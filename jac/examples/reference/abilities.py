from abc import ABC, abstractmethod
from functools import wraps
from typing import Callable, Any, Dict, List


# Custom Decorator
def log_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {func.__name__} with {args} and {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result

    return wrapper


# Standalone function
@log_decorator
def standalone_function(book_title: str) -> str:
    print(f"Standalone function: Adding book '{book_title}' to the library.")
    return book_title


# Abstract Base Class
class LibraryItem(ABC):
    @abstractmethod
    def item_info(self) -> str:
        pass


# Derived Class with overridden abstract method
class Book(LibraryItem):
    def __init__(self, title: str, author: str) -> None:
        self.title = title
        self.author = author

    def item_info(self) -> str:
        return f"Book Title: {self.title}, Author: {self.author}"

    # Static method
    @staticmethod
    def get_item_type() -> str:
        return "Book"

    # Class method
    @classmethod
    def create_from_dict(cls, info: Dict[str, str]) -> "Book":
        return cls(info["title"], info["author"])


# Class with instance method and custom decorator
class Library:
    def __init__(self) -> None:
        self.catalog: List[LibraryItem] = []

    @log_decorator
    def add_item(self, item: LibraryItem) -> None:
        self.catalog.append(item)
        print(f"Item '{item.item_info()}' added to the library catalog.")

    def display_catalog(self) -> None:
        for item in self.catalog:
            print(item.item_info())


# Using the various functions and methods
if __name__ == "__main__":
    # Using standalone function
    book_title: str = standalone_function("Python Programming")

    # Creating a Book instance using a class method
    book_info: Dict[str, str] = {"title": book_title, "author": "John Doe"}
    book: Book = Book.create_from_dict(book_info)

    # Using static method
    print(f"Item Type: {Book.get_item_type()}")

    # Creating a Library instance and adding a book to the catalog
    library: Library = Library()
    library.add_item(book)

    # Displaying the catalog
    library.display_catalog()
