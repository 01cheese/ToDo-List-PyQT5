# ToDo-List-PyQT5

# To-Do List Application

![image](https://github.com/01cheese/ToDo-List-PyQT5/assets/115219323/dbccb366-8740-4bc0-8983-86d501aadc9b)
![image](https://github.com/01cheese/ToDo-List-PyQT5/assets/115219323/48a97912-fe03-442a-b341-4f25748151b3)

This is a simple to-do list application built using Python and PyQt5. The application allows users to add, update, delete, and view tasks. It also supports theme customization and task management with deadlines and additional information.

### Features

- **Add Task**: Add new tasks with a task name, date added, deadline, and additional information.
- **Update Task**: Update existing tasks with new information.
- **Delete Task**: Delete selected tasks.
- **Print Tasks**: Print selected tasks.
- **Select All**: Select all tasks for batch actions.
- **Theme Customization**: Switch between different themes (Light, Dark, Gray, Blue, Green, Red).
- **Persistent Settings**: Save and load theme settings.

### Dependencies

- Python 3
- PyQt5
- SQLite3

### Installation

1. **Install Python**: Ensure you have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/).

2. **Install PyQt5**: Install PyQt5 using pip.
   ```bash
   pip install pyqt5
   ```

3. **Clone the Repository**: Clone this repository to your local machine.
   ```bash
   git clone https://github.com/yourusername/todo-app.git
   cd todo-app
   ```

4. **Run the Application**: Execute the Python script to run the application.
   ```bash
   python main.py
   ```

### Code Structure

### main.py

This is the main script that runs the To-Do application.

#### Database Setup

The application uses SQLite for storing tasks. The database is set up with a table for tasks.

```python
import sqlite3

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
```

#### Main Application Window

The `ToDoApp` class sets up the main window, including the layout and UI components.

```python
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QComboBox, QDialog, QLabel, QDateTimeEdit, QTextEdit, QCalendarWidget, QMessageBox
from PyQt5.QtCore import Qt, QDateTime, QSettings
from PyQt5.QtGui import QFont

# Constants for font and font size
FONT_FAMILY = 'Roboto'
FONT_SIZE = 72

class ToDoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('To-Do List')
        self.setGeometry(100, 100, 1600, 1200)

        self.settings = QSettings('MyCompany', 'ToDoApp')
        self.layout = QVBoxLayout()
        self.setFont(QFont(FONT_FAMILY, FONT_SIZE))
```

#### Adding Tasks

The `AddTaskDialog` class handles the UI for adding a new task.

```python
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
```

### Running the Application

The application is run by creating an instance of `QApplication` and the `ToDoApp` class, and then starting the application's event loop.

```python
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = ToDoApp()
    main_app.show()
    sys.exit(app.exec_())
```
