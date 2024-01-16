import unittest
import os

# Set environment variables for headless mode
os.environ["KIVY_NO_ARGS"] = "1"
os.environ["DISPLAY"] = ":99.0"  # Use a virtual X server display

from vrtodoapp import TodoApp  # Import your app here

class TestTodoApp(unittest.TestCase):
    def setUp(self):
        self.app = TodoApp()
        self.app.build()  # This will set up the UI elements

    def test_add_todo(self):
        initial_count = len(self.app.todos)
        self.app.add_todo("New Todo")  # Corrected to match your application's structure
        new_count = len(self.app.todos)
        self.assertEqual(new_count, initial_count + 1)

    def test_clear_completed_todos(self):
        # Add your logic for testing clearing completed todos
        pass  # Placeholder, replace with your test code

# Add more tests as needed...

if __name__ == '__main__':
    unittest.main()
