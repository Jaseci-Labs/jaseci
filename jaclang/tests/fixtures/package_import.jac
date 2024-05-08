import:py tkinter as tk ;
import:py from tkinter, messagebox ;

with entry {
    root_=tk.Tk();
    print(root_,"package is imported successfully!") ;
}

can show_message() {
    messagebox.showinfo("Information", "This is an information message box.") ;
}