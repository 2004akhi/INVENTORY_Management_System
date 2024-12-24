import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd
from tkinter.filedialog import asksaveasfilename

# Initialize Database
def initialize_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    # Add default user
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", "password"))
    conn.commit()
    conn.close()

# User Authentication
def login_screen():
    def validate_login():
        username = username_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            login_window.destroy()
            main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("400x300")
    login_window.configure(bg="#e3f2fd")

    tk.Label(login_window, text="Login", font=("Helvetica", 20, "bold"), bg="#e3f2fd", fg="#0d47a1").pack(pady=20)

    frame = tk.Frame(login_window, bg="#e3f2fd")
    frame.pack(pady=20)

    tk.Label(frame, text="Username:", font=("Helvetica", 12), bg="#e3f2fd").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(frame, font=("Helvetica", 12))
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(frame, text="Password:", font=("Helvetica", 12), bg="#e3f2fd").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(frame, font=("Helvetica", 12), show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(login_window, text="Login", command=validate_login, font=("Helvetica", 12), bg="#4caf50", fg="white").pack(pady=20)

    login_window.mainloop()

# Add Product
def add_product():
    def save_product():
        name = name_entry.get()
        quantity = quantity_entry.get()
        price = price_entry.get()

        if not name or not quantity.isdigit() or not price.replace('.', '', 1).isdigit():
            messagebox.showerror("Input Error", "Please provide valid inputs!")
            return

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
                       (name, int(quantity), float(price)))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Product added successfully!")
        add_window.destroy()

    add_window = tk.Toplevel()
    add_window.title("Add Product")
    add_window.geometry("400x300")
    add_window.configure(bg="#f0f8ff")

    tk.Label(add_window, text="Add Product", font=("Helvetica", 16, "bold"), bg="#f0f8ff", fg="#000080").pack(pady=10)

    frame = tk.Frame(add_window, bg="#f0f8ff")
    frame.pack(pady=20)

    tk.Label(frame, text="Name:", font=("Helvetica", 12), bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(frame, font=("Helvetica", 12))
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Quantity:", font=("Helvetica", 12), bg="#f0f8ff").grid(row=1, column=0, padx=10, pady=5)
    quantity_entry = tk.Entry(frame, font=("Helvetica", 12))
    quantity_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Price:", font=("Helvetica", 12), bg="#f0f8ff").grid(row=2, column=0, padx=10, pady=5)
    price_entry = tk.Entry(frame, font=("Helvetica", 12))
    price_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(add_window, text="Save", command=save_product, font=("Helvetica", 12), bg="#4caf50", fg="white").pack(pady=20)

# Remove Product
def remove_product():
    def delete_product():
        product_id = product_id_entry.get()

        if not product_id.isdigit():
            messagebox.showerror("Input Error", "Invalid Product ID!")
            return

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (int(product_id),))
        product = cursor.fetchone()

        if not product:
            messagebox.showerror("Error", "Product ID not found!")
        else:
            cursor.execute("DELETE FROM products WHERE id = ?", (int(product_id),))
            conn.commit()
            messagebox.showinfo("Success", "Product removed successfully!")
        conn.close()
        remove_window.destroy()

    remove_window = tk.Toplevel()
    remove_window.title("Remove Product")
    remove_window.geometry("400x200")
    remove_window.configure(bg="#f0f8ff")

    tk.Label(remove_window, text="Remove Product", font=("Helvetica", 16, "bold"), bg="#f0f8ff", fg="#000080").pack(pady=10)

    frame = tk.Frame(remove_window, bg="#f0f8ff")
    frame.pack(pady=20)

    tk.Label(frame, text="Enter Product ID:", font=("Helvetica", 12), bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=5)
    product_id_entry = tk.Entry(frame, font=("Helvetica", 12))
    product_id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(remove_window, text="Delete", command=delete_product, font=("Helvetica", 12), bg="#f44336", fg="white").pack(pady=20)

# View Products
def view_products():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    view_window = tk.Toplevel()
    view_window.title("View Products")
    view_window.geometry("600x400")
    view_window.configure(bg="#f0f8ff")

    tk.Label(view_window, text="Product Inventory", font=("Helvetica", 16, "bold"), bg="#f0f8ff", fg="#000080").pack(pady=10)

    frame = tk.Frame(view_window, bg="#f0f8ff")
    frame.pack()

    headers = ["Row", "ID", "Name", "Quantity", "Price"]
    for col, header in enumerate(headers):
        tk.Label(frame, text=header, font=("Helvetica", 12, "bold"), bg="#f0f8ff").grid(row=0, column=col, padx=10, pady=5)

    for row, product in enumerate(products, start=1):
        tk.Label(frame, text=row, font=("Helvetica", 12), bg="#f0f8ff").grid(row=row, column=0, padx=10, pady=5)
        tk.Label(frame, text=product[0], font=("Helvetica", 12), bg="#f0f8ff").grid(row=row, column=1, padx=10, pady=5)
        tk.Label(frame, text=product[1], font=("Helvetica", 12), bg="#f0f8ff").grid(row=row, column=2, padx=10, pady=5)
        tk.Label(frame, text=product[2], font=("Helvetica", 12), bg="#f0f8ff").grid(row=row, column=3, padx=10, pady=5)
        tk.Label(frame, text=product[3], font=("Helvetica", 12), bg="#f0f8ff").grid(row=row, column=4, padx=10, pady=5)

# Low Stock Alert
def low_stock_alert():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE quantity < 5")
    products = cursor.fetchall()
    conn.close()

    if products:
        alert_text = "\n".join([f"{product[1]} (ID: {product[0]}) - Qty: {product[2]}" for product in products])
        messagebox.showwarning("Low Stock Alert", f"The following items are low in stock:\n\n{alert_text}")
    else:
        messagebox.showinfo("No Low Stock", "There are no products with low stock.")

# Export to Excel
def export_to_excel():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    # Create DataFrame for export
    df = pd.DataFrame(products, columns=["ID", "Name", "Quantity", "Price"])

    # Ask for save location
    filepath = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")])
    if filepath:
        df.to_excel(filepath, index=False)
        messagebox.showinfo("Export Successful", "Product list exported successfully!")

# Main Screen
def main_screen():
    main_window = tk.Tk()
    main_window.title("Inventory Management")
    main_window.geometry("400x400")
    main_window.configure(bg="#e3f2fd")

    tk.Label(main_window, text="Inventory Management System", font=("Helvetica", 20, "bold"), bg="#e3f2fd", fg="#0d47a1").pack(pady=20)

    tk.Button(main_window, text="Add Product", command=add_product, font=("Helvetica", 12), bg="#9C27B0", fg="white").pack(pady=10)
    tk.Button(main_window, text="Remove Product", command=remove_product, font=("Helvetica", 12), bg="#f44336", fg="white").pack(pady=10)
    tk.Button(main_window, text="View Products", command=view_products, font=("Helvetica", 12), bg="#2196f3", fg="white").pack(pady=10)
    tk.Button(main_window, text="low_stock_alert", command=low_stock_alert, font=("Helvetica", 12), bg="#FF5722", fg="white").pack(pady=10)
    tk.Button(main_window, text="Export to Excel", command=export_to_excel, font=("Helvetica", 12), bg="#4caf50", fg="white").pack(pady=10)

    main_window.mainloop()

# Run the login screen first
initialize_db()
login_screen()
