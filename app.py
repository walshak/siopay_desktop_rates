import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QMessageBox, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QFileInfo
import sqlite3
import shutil
from os.path import basename, join

class CurrencyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Currency Exchange Rates")
        self.setGeometry(100, 100, 800, 600)

        # Create database and table
        self.conn = sqlite3.connect('currency_rates.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS currency_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT DEFAULT '0.00',
                m_rate TEXT DEFAULT '0.00',
                c_rate TEXT DEFAULT '0.00',
                b_rate TEXT DEFAULT '0.00',
                flag_path TEXT DEFAULT '/',
                comp TEXT DEFAULT 'N/A'
            )
        ''')
        self.conn.commit()

        # Set up the main widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Apply light mode material theme style
        self.setStyleSheet("""
            background-color: #eceff1;  /* Light background color */
            color: #263238;  /* Dark text color */
            font-family: 'Roboto', sans-serif;
        """)


        # Create and set up GUI components
        self.create_widgets()

    def create_widgets(self):
        # Labels and LineEdits for input
        pair_label = QLabel("Currency Pair:")
        m_rate_label = QLabel("Mobile Wallet Rate:")
        c_rate_label = QLabel("Cash Pickup(Rate):")
        b_rate_label = QLabel("Bank Deposit(Rate):")
        comp_label = QLabel("Comapany:")

        pair_label.setStyleSheet("color: #0a3d8f;")
        m_rate_label.setStyleSheet("color: #0a3d8f;")
        c_rate_label.setStyleSheet("color: #0a3d8f;")
        b_rate_label.setStyleSheet("color: #0a3d8f;")
        comp_label.setStyleSheet("color: #0a3d8f;")

        self.pair_entry = QLineEdit(self)
        self.m_rate_entry = QLineEdit(self)
        self.c_rate_entry = QLineEdit(self)
        self.b_rate_entry = QLineEdit(self)
        self.comp_entry = QLineEdit(self)

        self.pair_entry.setStyleSheet("""
            background-color: #eceff1;  /* Light background color */
            color: #263238;  /* Dark text color */
            border: 1px solid black;
            padding: 5px;
        """)
        self.m_rate_entry.setStyleSheet("""
            background-color: #eceff1;
            color: #263238;
            border: 1px solid black;
            padding: 5px;
        """)
        self.c_rate_entry.setStyleSheet("""
            background-color: #eceff1;
            color: #263238;
            border: 1px solid black;
            padding: 5px;
        """)
        self.b_rate_entry.setStyleSheet("""
            background-color: #eceff1;
            color: #263238;
            border: 1px solid black;
            padding: 5px;
        """)
        self.comp_entry.setStyleSheet("""
            background-color: #eceff1;
            color: #263238;
            border: 1px solid black;
            padding: 5px;
        """)


         # Buttons for CRUD operations
        add_button = QPushButton("Add", self)
        manage_button = QPushButton("Manage Rates", self)
        show_button = QPushButton("Show Rates", self)

        add_button.setStyleSheet("""
            background-color: #0a3d8f; 
            color: #eceff1; 
            border: none; 
            padding: 10px; 
            margin-top: 10px;
        """)
        show_button.setStyleSheet("""
            background-color: #0a3d8f; 
            color: #eceff1; 
            border: none; 
            padding: 10px; 
            margin-top: 10px;
        """)

        manage_button.setStyleSheet("""
            background-color: #0a3d8f; 
            color: #eceff1; 
            border: none; 
            padding: 10px; 
            margin-top: 10px;
        """)

        # Button for flag upload
        upload_flag_button = QPushButton("Upload Flag", self)
        upload_flag_button.setStyleSheet("""
            background-color: #0a3d8f; 
            color: #eceff1; 
            border: none; 
            padding: 10px; 
            margin-top: 10px;
        """)
        upload_flag_button.clicked.connect(self.upload_flag)


        # Connect buttons to methods
        add_button.clicked.connect(self.add_rate)
        show_button.clicked.connect(self.show_rates)
        manage_button.clicked.connect(self.manage_rates)

        # Layout setup
        layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        input_layout.addWidget(pair_label)
        input_layout.addWidget(self.pair_entry)
        input_layout.addWidget(m_rate_label)
        input_layout.addWidget(self.m_rate_entry)
        input_layout.addWidget(c_rate_label)
        input_layout.addWidget(self.c_rate_entry)
        input_layout.addWidget(b_rate_label)
        input_layout.addWidget(self.b_rate_entry)
        input_layout.addWidget(comp_label)
        input_layout.addWidget(self.comp_entry)

        button_layout.addWidget(add_button)
        button_layout.addWidget(show_button)
        button_layout.addWidget(manage_button)

        # Add the flag upload button to the button layout
        input_layout.addWidget(upload_flag_button)

        layout.addLayout(input_layout)
        layout.addLayout(button_layout)

        # main_widget.setLayout(layout)
        self.centralWidget().setLayout(layout)

    def upload_flag(self):
        flag_path, _ = QFileDialog.getOpenFileName(self, 'Select Flag Image', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if flag_path:
            # Get the destination path in the program folder
            destination_folder = './flags'  # Change this to your desired folder
            destination_path = join(destination_folder, basename(flag_path))

            try:
                # Copy the selected flag image to the program folder
                shutil.copy(flag_path, destination_path)

                # Do something with the selected flag path (e.g., save it to the database)
                print(f'Selected flag path: {destination_path}')

                # Store the flag path for later use in the add_rate function
                self.flag_path = destination_path

            except shutil.Error as e:
                print(f"Error copying the flag image: {e}")

    def add_rate(self):
        pair = self.pair_entry.text()
        m_rate = self.m_rate_entry.text()
        c_rate = self.c_rate_entry.text()
        b_rate = self.b_rate_entry.text()
        comp = self.comp_entry.text()

         # Get the flag path (you may save it to the database or use it as needed)
        flag_path = self.flag_path if hasattr(self, 'flag_path') else 'N/A'


        # Insert data into the database
        self.cursor.execute('INSERT INTO currency_rates (pair, m_rate, c_rate, b_rate, comp, flag_path) VALUES (?, ?, ?, ?, ?, ?)',
                            (pair, m_rate, c_rate, b_rate, comp, flag_path))
        self.conn.commit()

        # Clear the entry fields and flag path
        self.pair_entry.clear()
        self.m_rate_entry.clear()
        self.b_rate_entry.clear()
        self.c_rate_entry.clear()
        self.comp_entry.clear()
        self.flag_path = None

    def show_rates(self):
        # Display the rates in a new window
        self.rates_window = QDialog(self)
        self.rates_window.setWindowTitle("Exchange Rates")
        self.rates_window.setGeometry(200, 200, 600, 400)  # Adjust the size as needed
        self.rates_window.setStyleSheet("background-color: #263238; color: #eceff1;")

        # Fetch data from the database
        self.cursor.execute('SELECT * FROM currency_rates')
        data = self.cursor.fetchall()

        # Create a table widget for displaying the data
        table = QTableWidget(self.rates_window)
        table.setColumnCount(6)  # Add one more column for the flags
        table.setHorizontalHeaderLabels(["Flag", "Currency Pair", "Mobile Wallet(Rate)", "Cash Pickup(Rate)", "Bank Deposit(Rate)", "Comapany"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Adjust the column width
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

        for row in data:
            row_position = table.rowCount()
            table.insertRow(row_position)

            # Load the flag image
            flag_path = row[5]  # Assuming that the flag path is stored in the 6th column
            flag_item = QTableWidgetItem()
            flag_item.setData(Qt.DecorationRole, QPixmap(flag_path).scaled(70, 70))  # Adjust the size as needed
            table.setItem(row_position, 0, flag_item)

            # Fill other columns
            table.setItem(row_position, 1, QTableWidgetItem(row[1]))
            table.setItem(row_position, 2, QTableWidgetItem(row[2]))
            table.setItem(row_position, 3, QTableWidgetItem(row[3]))
            table.setItem(row_position, 4, QTableWidgetItem(row[4]))
            table.setItem(row_position, 5, QTableWidgetItem(row[6]))

        table.setStyleSheet("""
            background-color: #eceff1; 
            color: #0a3d8f; 
            border: none; 
            padding: 5px;
        """)

        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setFocusPolicy(Qt.NoFocus)

        # Set font for the table
        font = QFont("Roboto", 18)
        table.setFont(font)

        # Adjust the font for the horizontal header
        header_font = QFont("Roboto", 18)  # Choose your desired font and size
        table.horizontalHeader().setFont(header_font)



        rates_layout = QVBoxLayout()
        rates_layout.addWidget(table)

        self.rates_window.setLayout(rates_layout)
        self.rates_window.showMaximized()

    def manage_rates(self):
        # Display the rates in a new window
        self.rates_window = QDialog(self)
        self.rates_window.setWindowTitle("Exchange Rates")
        self.rates_window.setGeometry(200, 200, 600, 400)  # Adjust the size as needed
        self.rates_window.setStyleSheet("background-color: #263238; color: #eceff1;")

        # Fetch data from the database
        self.cursor.execute('SELECT * FROM currency_rates')
        data = self.cursor.fetchall()

        # Create a table widget for displaying the data
        table = QTableWidget(self.rates_window)
        table.setColumnCount(8)  # Add three more columns for Edit, Delete buttons, and Flag
        table.setHorizontalHeaderLabels(["Flag", "Currency Pair", "Mobile Wallet(Rate)", "Cash Pickup(Rate)", "Bank Deposit(Rate)", "Comapany", "Edit", "Delete"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Adjust the column width for the flag
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Fixed)
        table.horizontalHeader().setSectionResizeMode(7, QHeaderView.Fixed)

        for row in data:
            row_position = table.rowCount()
            table.insertRow(row_position)

            # Load the flag image
            flag_path = row[5]  # Assuming that the flag path is stored in the 5th column
            flag_item = QTableWidgetItem()
            flag_item.setData(Qt.DecorationRole, QPixmap(flag_path).scaled(70, 70))  # Adjust the size as needed
            table.setItem(row_position, 0, flag_item)

            # Fill other columns
            table.setItem(row_position, 1, QTableWidgetItem(row[1]))
            table.setItem(row_position, 2, QTableWidgetItem(row[2]))
            table.setItem(row_position, 3, QTableWidgetItem(row[3]))
            table.setItem(row_position, 4, QTableWidgetItem(row[4]))
            table.setItem(row_position, 5, QTableWidgetItem(row[6]))  # Assuming that the company is stored in the 6th column

            # Add Edit button
            edit_button = QPushButton("Edit", table)
            edit_button.clicked.connect(lambda _, r=row[0]: self.edit_rate(r))
            table.setCellWidget(row_position, 6, edit_button)

            # Add Delete button
            delete_button = QPushButton("Delete", table)
            delete_button.clicked.connect(lambda _, r=row[0]: self.delete_rate(r))
            table.setCellWidget(row_position, 7, delete_button)

        table.setStyleSheet("""
            background-color: #eceff1; 
            color: #0a3d8f; 
            border: none; 
            padding: 5px;
        """)

        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setFocusPolicy(Qt.NoFocus)

        # Set font for the table
        font = QFont("Roboto", 12)
        table.setFont(font)

        # Adjust the font for the horizontal header
        header_font = QFont("Roboto", 18)  # Choose your desired font and size
        table.horizontalHeader().setFont(header_font)

        rates_layout = QVBoxLayout()
        rates_layout.addWidget(table)

        self.rates_window.setLayout(rates_layout)
        self.rates_window.showMaximized()

    def edit_rate(self, rate_id):
        # Fetch the existing data for the selected rate
        self.cursor.execute('SELECT * FROM currency_rates WHERE id = ?', (rate_id,))
        data = self.cursor.fetchone()

        # Open a dialog for editing
        edit_dialog = QDialog(self)
        edit_dialog.setWindowTitle("Edit Exchange Rate")
        edit_dialog.setGeometry(300, 300, 500, 450)

        edit_layout = QVBoxLayout()

        # Widgets for editing
        pair_label = QLabel("Currency Pair:")
        m_rate_label = QLabel("Mobile Wallet(Rate):")
        c_rate_label = QLabel("Cash Pickup(Rate:")
        b_rate_label = QLabel("Bank Deposit(Rate):")
        comp_label = QLabel("Comapany:")

        flag_label = QLabel("Flag:")
        flag_button = QPushButton("Upload Flag", edit_dialog)
        flag_button.clicked.connect(lambda: self.upload_flag_for_edit(edit_dialog, flag_label))

        pair_entry = QLineEdit(edit_dialog)
        m_rate_entry = QLineEdit(edit_dialog)
        c_rate_entry = QLineEdit(edit_dialog)
        b_rate_entry = QLineEdit(edit_dialog)
        comp_entry = QLineEdit(edit_dialog)

        pair_entry.setText(data[1])  # Populate with existing data
        m_rate_entry.setText(data[2])
        c_rate_entry.setText(data[3])
        b_rate_entry.setText(data[4])
        comp_entry.setText(data[6])

        edit_layout.addWidget(pair_label)
        edit_layout.addWidget(pair_entry)
        edit_layout.addWidget(m_rate_label)
        edit_layout.addWidget(m_rate_entry)
        edit_layout.addWidget(c_rate_label)
        edit_layout.addWidget(c_rate_entry)
        edit_layout.addWidget(b_rate_label)
        edit_layout.addWidget(b_rate_entry)
        edit_layout.addWidget(comp_label)
        edit_layout.addWidget(comp_entry)
        edit_layout.addWidget(flag_label)
        edit_layout.addWidget(flag_button)

        # Save changes button
        save_button = QPushButton("Save Changes", edit_dialog)
        save_button.clicked.connect(lambda: self.save_changes(rate_id, pair_entry.text(), m_rate_entry.text(), c_rate_entry.text(), b_rate_entry.text(), comp_entry.text(), flag_label.text()))
        save_button.clicked.connect(edit_dialog.accept)  # Close the edit dialog
        save_button.clicked.connect(self.show_rates)  # Refresh the show_rates dialog
        save_button.clicked.connect(self.manage_rates)  # Refresh the manage dialog
        edit_layout.addWidget(save_button)

        edit_dialog.setLayout(edit_layout)
        edit_dialog.exec_()

    def upload_flag_for_edit(self, edit_dialog, flag_label):
        flag_path, _ = QFileDialog.getOpenFileName(edit_dialog, 'Select Flag Image', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if flag_path:
            # Save the flag to the "./flags" folder
            flags_folder = "./flags"
            uploaded_flag_path = join(flags_folder, basename(flag_path))
            shutil.copy(flag_path, uploaded_flag_path)

            # Save the uploaded flag path to the database
            self.flag_path_for_edit = uploaded_flag_path

            # Update the flag label
            flag_label.setText(f"Flag: {uploaded_flag_path}")

    def save_changes(self, rate_id, new_pair, new_m_rate, new_c_rate, new_b_rate, new_comp, new_flag_path):
        # If a new flag was uploaded, use the new_flag_path; otherwise, use the existing flag path
        flag_path_to_save = new_flag_path if hasattr(self, 'flag_path_for_edit') else new_flag_path

        # Update the data in the database
        self.cursor.execute('UPDATE currency_rates SET pair=?, m_rate=?, c_rate=?, b_rate=?, comp=?, flag_path=? WHERE id=?',
                            (new_pair, new_m_rate, new_c_rate, new_b_rate, new_comp, flag_path_to_save, rate_id))
        self.conn.commit()

    def delete_rate(self, rate_id):
        # Confirm deletion
        confirm = QMessageBox.question(self, 'Delete Exchange Rate', 'Are you sure you want to delete this exchange rate?',
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirm == QMessageBox.Yes:
            # Delete the data from the database
            self.cursor.execute('DELETE FROM currency_rates WHERE id = ?', (rate_id,))
            self.conn.commit()

        # Refresh the show_rates dialog after deletion
        self.show_rates()
        self.manage_rates()  # Refresh the manage dialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyApp()
    window.show()
    sys.exit(app.exec_())
