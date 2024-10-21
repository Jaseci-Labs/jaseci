
import:py from functools {wraps}
import:py from typing {Callable, List, Dict, Any}

#Custom Decorator
can log_decorator(func: Callable) -> Callable {
    @wraps(func)
    can wrapper(*args: List, **kwargs: Dict) -> Any {
        print(f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}");
        result = func(*args, **kwargs);
        print(f"{func.__name__} returned {result}");
        return result;
    }
    return wrapper;
}

# Standalone function
@log_decorator
can standalone_function(book_title: str) ->str {
    print(f"Standalone function: Adding book '{book_title}' to the library.");
    return book_title;
}

class LibraryItem{
    can item_info() -> str abs;
}

class Book:LibraryItem:{
    can init(self:Book, title: str,  author: str) -> None {
        self.title = title;
        self.author = author;
    }

    can item_info(self:LibraryItem) -> str {
        return f"{"Book Title: "}{self.title}{", Author: "}{self.author}" ;
    }

    static can get_item_type() -> str {
        return "Book";
    }

    @ classmethod
    can create_from_dict(cls: Any, info: Dict[(str, str)]) -> 'Book' {
        return cls(info['title'], info['author']) ;
    }
}

class Library{
    can init(self:Library) -> None{
        self.catalog: List[LibraryItem] = [];
    }

    @log_decorator
    can add_item(self:Library, item: LibraryItem) -> None{
        self.catalog.append(item);
        print(f"Item '{item.item_info()}' added to the library catalog.");
    }

    can display_catalog(self:Library) -> None{
        for item in self.catalog{
            print(item.item_info());
        }

}
}

with entry {

    book_title: str = standalone_function("Python Programming");

    # Creating a Book instance using a class method
    book_info: Dict[(str, str)] = {'title': book_title, 'author': 'John Doe'};
    book: Book = Book.create_from_dict(book_info);

    # Using static method
    print(f"Item Type: {Book.get_item_type()}");

    # Creating a Library instance and adding a book to the catalog
    library: Library = Library();
    library.add_item(book);

    # Displaying the catalog
    library.display_catalog();
}