import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit,
                             QListWidget, QListWidgetItem, QMessageBox, QDateTimeEdit, QTextEdit, QLabel,
                             QCalendarWidget, QComboBox, QDialog)
from PyQt5.QtCore import Qt, QDateTime, QSettings
from PyQt5.QtGui import QFont

# Constants for font and font size
FONT_FAMILY = 'Roboto'
FONT_SIZE = 72

# Database setup
conn = sqlite3.connect('todo.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                 id INTEGER PRIMARY KEY,
                 task TEXT NOT NULL,
                 date_added TEXT NOT NULL,
                 deadline TEXT NOT NULL,
                 info TEXT
             )''')
conn.commit()

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Task')
        self.setGeometry(300, 300, 800, 600)

        layout = QVBoxLayout()
        self.setFont(QFont(FONT_FAMILY, FONT_SIZE))

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText('Enter a new task')
        self.task_input.setFont(QFont(FONT_FAMILY, FONT_SIZE))
        layout.addWidget(self.task_input)

        self.date_added_input = QDateTimeEdit(self)
        self.date_added_input.setDateTime(QDateTime.currentDateTime())
        self.date_added_input.setDisplayFormat("yyyy-MM-dd")
        self.date_added_input.setFont(QFont(FONT_FAMILY, FONT_SIZE))
        layout.addWidget(QLabel("Date Added:", self).setFont(QFont(FONT_FAMILY, FONT_SIZE)))
        layout.addWidget(self.date_added_input)

        self.deadline_input = QCalendarWidget(self)
        layout.addWidget(QLabel("Deadline:", self).setFont(QFont(FONT_FAMILY, FONT_SIZE)))
        layout.addWidget(self.deadline_input)

        self.info_input = QTextEdit(self)
        self.info_input.setPlaceholderText('Enter additional information')
        self.info_input.setFont(QFont(FONT_FAMILY, FONT_SIZE))
        layout.addWidget(QLabel("Information:", self).setFont(QFont(FONT_FAMILY, FONT_SIZE)))
        layout.addWidget(self.info_input)

        self.add_button = QPushButton('Add', self)
        self.add_button.setFont(QFont(FONT_FAMILY, FONT_SIZE, QFont.Bold))
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 20px 40px;")
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_task(self):
        task = self.task_input.text()
        date_added = self.date_added_input.dateTime().toString("yyyy-MM-dd")
        deadline = self.deadline_input.selectedDate().toString("yyyy-MM-dd")
        info = self.info_input.toPlainText()
        if task:
            c.execute("INSERT INTO tasks (task, date_added, deadline, info) VALUES (?, ?, ?, ?)",
                      (task, date_added, deadline, info))
            conn.commit()
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Task cannot be empty")

class UpdateTaskDialog(QDialog):
    def __init__(self, task_id, task, deadline, info, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Update Task')
        self.setGeometry(300, 300, 800, 600)

        self.task_id = task_id
        layout = QVBoxLayout()
        self.setFont(QFont(FONT_FAMILY, FONT_SIZE))

        self.task_input = QLineEdit(self)
        self.task_input.setText(task)
        self.task_input.setFont(QFont(FONT_FAMILY, FONT_SIZE))
        layout.addWidget(self.task_input)

        self.deadline_input = QCalendarWidget(self)
        self.deadline_input.setSelectedDate(QDateTime.fromString(deadline, "yyyy-MM-dd").date())
        layout.addWidget(QLabel("Deadline:", self).setFont(QFont(FONT_FAMILY, FONT_SIZE)))
        layout.addWidget(self.deadline_input)

        self.info_input = QTextEdit(self)
        self.info_input.setText(info)
        self.info_input.setFont(QFont(FONT_FAMILY, FONT_SIZE))
        layout.addWidget(QLabel("Information:", self).setFont(QFont(FONT_FAMILY, FONT_SIZE)))
        layout.addWidget(self.info_input)

        self.update_button = QPushButton('Update', self)
        self.update_button.setFont(QFont(FONT_FAMILY, FONT_SIZE, QFont.Bold))
        self.update_button.setStyleSheet("background-color: #FFA500; color: white; padding: 20px 40px;")
        self.update_button.clicked.connect(self.update_task)
        layout.addWidget(self.update_button)

        self.setLayout(layout)

    def update_task(self):
        new_task = self.task_input.text()
        new_deadline = self.deadline_input.selectedDate().toString("yyyy-MM-dd")
        new_info = self.info_input.toPlainText()
        if new_task:
            c.execute("UPDATE tasks SET task = ?, deadline = ?, info = ? WHERE id = ?",
                      (new_task, new_deadline, new_info, self.task_id))
            conn.commit()
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Task cannot be empty")

class ToDoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('To-Do List')
        self.setGeometry(100, 100, 1600, 1200)

        self.settings = QSettings('MyCompany', 'ToDoApp')
        self.layout = QVBoxLayout()
        self.setFont(QFont(FONT_FAMILY, FONT_SIZE))

        self.theme_combo = QComboBox(self)
        self.theme_combo.addItem('Light Theme')
        self.theme_combo.addItem('Dark Theme')
        self.theme_combo.addItem('Gray Theme')
        self.theme_combo.addItem('Blue Theme')
        self.theme_combo.addItem('Green Theme')
        self.theme_combo.addItem('Red Theme')
        self.theme_combo.setFont(QFont(FONT_FAMILY, FONT_SIZE))
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        self.layout.addWidget(self.theme_combo)

        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton('Add Task', self)
        self.add_button.setFont(QFont(FONT_FAMILY, FONT_SIZE, QFont.Bold))
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 20px 40px;")
        self.add_button.clicked.connect(self.open_add_dialog)
        self.button_layout.addWidget(self.add_button)

        self.update_button = QPushButton('Update Task', self)
        self.update_button.setFont(QFont(FONT_FAMILY, FONT_SIZE, QFont.Bold))
        self.update_button.setStyleSheet("background-color: #FFA500; color: white; padding: 20px 40px;")
        self.update_button.clicked.connect(self.open_update_dialog)
        self.button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton('Delete Task', self)
        self.delete_button.setFont(QFont(FONT_FAMILY, FONT_SIZE, QFont.Bold))
        self.delete_button.setStyleSheet("background-color: #F44336; color: white; padding: 20px 40px;")
        self.delete_button.clicked.connect(self.delete_task)
        self.button_layout.addWidget(self.delete_button)

        self.print_button = QPushButton('Print Tasks', self)
        self.print_button.setFont(QFont(FONT_FAMILY, FONT_SIZE, QFont.Bold))
        self.print_button.setStyleSheet("background-color: #2196F3; color: white; padding: 20px 40px;")
        self.print_button.clicked.connect(self.print_tasks)
        self.button_layout.addWidget(self.print_button)

        self.select_all_button = QPushButton('Select All', self)
        self.select_all_button.setFont(QFont(FONT_FAMILY, FONT_SIZE, QFont.Bold))
        self.select_all_button.setStyleSheet("background-color: #9E9E9E; color: white; padding: 20px 40px;")
        self.select_all_button.clicked.connect(self.select_all_tasks)
        self.button_layout.addWidget(self.select_all_button)

        self.layout.addLayout(self.button_layout)

        self.task_list = QListWidget(self)
        self.task_list.setFont(QFont(FONT_FAMILY, FONT_SIZE))
        self.layout.addWidget(self.task_list)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.load_tasks()
        self.load_settings()

    def load_tasks(self):
        self.task_list.clear()
        c.execute("SELECT * FROM tasks")
        tasks = c.fetchall()
        for task in tasks:
            item = QListWidgetItem(f"{task[1]} (Added: {task[2]}, Deadline: {task[3]})")
            item.setData(Qt.UserRole, task[0])
            item.setData(Qt.UserRole + 1, task[3])  # Deadline
            item.setData(Qt.UserRole + 2, task[4])  # Info
            self.task_list.addItem(item)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)

    def open_add_dialog(self):
        dialog = AddTaskDialog(self)
        if dialog.exec():
            self.load_tasks()

    def open_update_dialog(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task_id = selected_item.data(Qt.UserRole)
            task_text = selected_item.text().split(" (Added")[0]
            task_deadline = selected_item.data(Qt.UserRole + 1)
            task_info = selected_item.data(Qt.UserRole + 2)
            dialog = UpdateTaskDialog(task_id, task_text, task_deadline, task_info, self)
            if dialog.exec():
                self.load_tasks()
        else:
            QMessageBox.warning(self, "Warning", "No task selected")

    def delete_task(self):
        selected_items = [item for item in self.task_list.findItems("*", Qt.MatchWildcard) if
                          item.checkState() == Qt.Checked]
        if selected_items:
            reply = QMessageBox.question(self, 'Confirm Delete',
                                         "Are you sure you want to delete the selected tasks?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                for item in selected_items:
                    task_id = item.data(Qt.UserRole)
                    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                conn.commit()
                self.load_tasks()
        else:
            QMessageBox.warning(self, "Warning", "No tasks selected")

    def print_tasks(self):
        selected_items = [item for item in self.task_list.findItems("*", Qt.MatchWildcard) if
                          item.checkState() == Qt.Checked]
        if selected_items:
            tasks = [f"{item.text()} (Info: {item.data(Qt.UserRole + 2)})" for item in selected_items]
            QMessageBox.information(self, "Selected Tasks", "\n".join(tasks))
        else:
            QMessageBox.information(self, "Tasks", "No tasks selected")

    def select_all_tasks(self):
        for index in range(self.task_list.count()):
            item = self.task_list.item(index)
            item.setCheckState(Qt.Checked)

    def change_theme(self, index):
        theme = self.theme_combo.itemText(index)
        self.apply_theme(theme)
        self.settings.setValue('theme', theme)

    def apply_theme(self, theme):
        if theme == 'Light Theme':
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: #f0f0f0;
                    color: #000;
                    font-size: {FONT_SIZE}px;
                }}
                QLineEdit, QTextEdit, QListWidget, QCalendarWidget, QComboBox {{
                    background-color: #ffffff;
                    color: #000;
                    font-size: {FONT_SIZE}px;
                }}
                QPushButton {{
                    background-color: #dcdcdc;
                    color: #000;
                    font-size: {FONT_SIZE}px;
                    padding: 20px 40px;
                }}
            """)
        elif theme == 'Dark Theme':
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: #2b2b2b;
                    color: #fff;
                    font-size: {FONT_SIZE}px;
                }}
                QLineEdit, QTextEdit, QListWidget, QCalendarWidget, QComboBox {{
                    background-color: #3c3c3c;
                    color: #fff;
                    font-size: {FONT_SIZE}px;
                }}
                QPushButton {{
                    background-color: #555555;
                    color: #fff;
                    font-size: {FONT_SIZE}px;
                    padding: 20px 40px;
                }}
            """)
        elif theme == 'Gray Theme':
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: #808080;
                    color: #fff;
                    font-size: {FONT_SIZE}px;
                }}
                QLineEdit, QTextEdit, QListWidget, QCalendarWidget, QComboBox {{
                    background-color: #a9a9a9;
                    color: #fff;
                    font-size: {FONT_SIZE}px;
                }}
                QPushButton {{
                    background-color: #696969;
                    color: #fff;
                    font-size: {FONT_SIZE}px;
                    padding: 20px 40px;
                }}
            """)
        elif theme == 'Blue Theme':
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: #87CEEB;
                    color: #000;
                    font-size: {FONT_SIZE}px;
                }}
                QLineEdit, QTextEdit, QListWidget, QCalendarWidget, QComboBox {{
                    background-color: #B0E0E6;
                    color: #000;
                    font-size: {FONT_SIZE}px;
                }}
                QPushButton {{
                    background-color: #1E90FF;
                    color: #fff;
                    font-size: {FONT_SIZE}px;
                    padding: 20px 40px;
                }}
            """)
        elif theme == 'Green Theme':
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: #8FBC8F;
                    color: #000;
                    font-size: {FONT_SIZE}px;
                }}
                QLineEdit, QTextEdit, QListWidget, QCalendarWidget, QComboBox {{
                    background-color: #98FB98;
                    color: #000;
                    font-size: {FONT_SIZE}px;
                }}
                QPushButton {{
                    background-color: #3CB371;
                    color: #fff;
                    font-size: {FONT_SIZE}px;
                    padding: 20px 40px;
                }}
            """)
        elif theme == 'Red Theme':
            self.setStyleSheet(f"""
                QWidget {{
                    background-color: #CD5C5C;
                    color: #000;
                    font-size: {FONT_SIZE}px;
                }}
                QLineEdit, QTextEdit, QListWidget, QCalendarWidget, QComboBox {{
                    background-color: #FA8072;
                    color: #000;
                    font-size: {FONT_SIZE}px;
                }}
                QPushButton {{
                    background-color: #B22222;
                    color: #fff;
                    font-size: {FONT_SIZE}px;
                    padding: 20px 40px;
                }}
            """)

    def load_settings(self):
        theme = self.settings.value('theme', 'Light Theme')
        index = self.theme_combo.findText(theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
        self.apply_theme(theme)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = ToDoApp()
    main_app.show()
    sys.exit(app.exec_())
