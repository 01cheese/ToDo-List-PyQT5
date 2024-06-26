# ToDo-List-PyQT5

# To-Do List Application

This is a PyQt5-based To-Do List application that allows you to manage your tasks effectively. The application supports adding, updating, deleting, and printing tasks. Additionally, it features theme customization to enhance the user experience.

## Features

1. **Add Task**: Add new tasks with details such as task name, date added, deadline, and additional information.
2. **Update Task**: Update existing tasks with new details.
3. **Delete Task**: Delete selected tasks.
4. **Print Tasks**: Print selected tasks.
5. **Select All Tasks**: Select all tasks at once.
6. **Theme Customization**: Change the application's theme (Light, Dark, Gray, Blue, Green, Red).

## Dependencies

- Python 3.x
- PyQt5

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/todo-app.git
    ```
2. Navigate to the project directory:
    ```sh
    cd todo-app
    ```
3. Install the required packages:
    ```sh
    pip install PyQt5
    ```

## Usage

1. Run the application:
    ```sh
    python todo_app.py
    ```

## Code Overview

### Database Setup

The application uses SQLite for storing tasks. The database is set up with a table named `tasks` which has columns for `id`, `task`, `date_added`, `deadline`, and `info`.

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

### AddTaskDialog Class

This class defines a dialog for adding new tasks. It includes input fields for the task name, date added, deadline, and additional information.

```python
class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Task')
        self.setGeometry(300, 300, 800, 600)

        layout = QVBoxLayout()
        self.setFont(QFont('Arial', 24))

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText('Enter a new task')
        layout.addWidget(self.task_input)

        self.date_added_input = QDateTimeEdit(self)
        self.date_added_input.setDateTime(QDateTime.currentDateTime())
        self.date_added_input.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(QLabel("Date Added:"))
        layout.addWidget(self.date_added_input)

        self.deadline_input = QCalendarWidget(self)
        layout.addWidget(QLabel("Deadline:"))
        layout.addWidget(self.deadline_input)

        self.info_input = QTextEdit(self)
        self.info_input.setPlaceholderText('Enter additional information')
        layout.addWidget(QLabel("Information:"))
        layout.addWidget(self.info_input)

        self.add_button = QPushButton('Add', self)
        self.add_button.setFont(QFont('Arial', 24, QFont.Bold))
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

### UpdateTaskDialog Class

This class defines a dialog for updating existing tasks. It includes input fields for the task name, deadline, and additional information.

```python
class UpdateTaskDialog(QDialog):
    def __init__(self, task_id, task, deadline, info, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Update Task')
        self.setGeometry(300, 300, 800, 600)

        self.task_id = task_id
        layout = QVBoxLayout()
        self.setFont(QFont('Arial', 24))

        self.task_input = QLineEdit(self)
        self.task_input.setText(task)
        layout.addWidget(self.task_input)

        self.deadline_input = QCalendarWidget(self)
        self.deadline_input.setSelectedDate(QDateTime.fromString(deadline, "yyyy-MM-dd").date())
        layout.addWidget(QLabel("Deadline:"))
        layout.addWidget(self.deadline_input)

        self.info_input = QTextEdit(self)
        self.info_input.setText(info)
        layout.addWidget(QLabel("Information:"))
        layout.addWidget(self.info_input)

        self.update_button = QPushButton('Update', self)
        self.update_button.setFont(QFont('Arial', 24, QFont.Bold))
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
```

### ToDoApp Class

This class defines the main window of the application. It includes functionalities for adding, updating, deleting, printing, and selecting tasks, as well as theme customization.
