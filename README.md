# INVENTORY_Management_System

A simple desktop-based inventory management system built using Python and Tkinter. This application allows users to manage product inventory, including adding, removing, and viewing products. It also features low stock alerts and the ability to export inventory data to Excel.

## Features

- **User Authentication**: Login screen with a default admin user (`admin` / `password`).
- **Add Product**: Add products to the inventory with details like name, quantity, and price.
- **Remove Product**: Remove products by specifying their unique ID.
- **View Products**: View all products in the inventory along with their details.
- **Low Stock Alert**: Get notified when any product stock is less than 5.
- **Export to Excel**: Export the current product inventory to an Excel file.
  
## Requirements

- Python 3.x
- Tkinter (comes pre-installed with Python)
- SQLite3 (comes pre-installed with Python)
- Pandas (`pip install pandas`)

## Installation

1. **Clone or Download the Repository**:
   Download or clone this project to your local machine.

2. **Install Dependencies**:
   Install the required dependencies using the following command:
   ```bash
   pip install pandas
   ```

3. **Run the Application**:
   - Open the terminal or command prompt.
   - Navigate to the folder where the script is located.
   - Run the script:
   ```bash
   python inventory_system.py
   ```

## Usage

1. Upon running the script, a **Login Screen** appears. Use the default credentials:
   - **Username**: `admin`
   - **Password**: `password`

2. After login, you will be directed to the **Main Screen**, where you can:
   - Add new products
   - Remove products by their ID
   - View the list of products
   - Check low stock items
   - Export the inventory list to Excel.


3. Share the generated `.exe` file (for Windows) or equivalent file for macOS/Linux.

## License

This project is open-source and free to use.

