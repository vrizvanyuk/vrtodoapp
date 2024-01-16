import unittest
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock  # Import Clock to trigger Kivy App creation
from vrtodoapp import ToDoRecycleView

class TestTodoApp(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Kivy app using Clock.schedule_once
        Clock.schedule_once(self.create_app, 0)

    def create_app(self, dt):
        self.app = App()
        self.app.run()

    def tearDown(self):
        # Close the Kivy app when the test is finished
        self.app.stop()

    def test_app_initialization(self):
        self.assertIsInstance(self.app, App)

    def test_add_todo_button(self):
        add_button = self.app.root.children[3].children[0]
        self.assertIsInstance(add_button, Button)
        self.assertEqual(add_button.text, 'Add Todo')

    def test_new_todo_input(self):
        new_todo_input = self.app.root.children[4]
        self.assertIsInstance(new_todo_input, TextInput)
        self.assertEqual(new_todo_input.hint_text, 'Enter a new todo')

    def test_todo_list_view(self):
        todo_list_view = self.app.root.children[2]
        self.assertIsInstance(todo_list_view, ToDoRecycleView)
        # You may add more assertions here based on your specific TODO app structure

    def test_clear_completed_button(self):
        clear_completed_button = self.app.root.children[1]
        self.assertIsInstance(clear_completed_button, Button)
        self.assertEqual(clear_completed_button.text, 'Clear Completed Items')

if __name__ == '__main__':
    unittest.main()
