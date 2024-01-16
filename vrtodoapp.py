from kivy.config import Config
Config.set('graphics', 'width', '300')  # Set desired width
Config.set('graphics', 'height', '600')  # Set desired height

from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

Builder.load_string('''
<ToDoRecycleView>:
    viewclass: 'Label'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
                    
''')

class ToDoRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(ToDoRecycleView, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 64/255.0, 1)  # Darker navy blue
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_data(self, todo_list):
        self.data = [{'text': f'[i][s]{str(todo).strip()}[/s][/i]' if 'completed' in todo else f'{index + 1}. {todo.strip()}', 'markup': True} for index, todo in enumerate(todo_list)]

class TodoApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Display current date
        current_date = datetime.now().strftime("%A, %b %d, %Y")
        date_label = Label(text=current_date, size_hint_y=None, height=30)
        self.layout.add_widget(date_label)
        
        # Read todos from file
        self.todos = self.read_todos()

        # Todo list view
        self.todo_list_view = ToDoRecycleView()
        self.layout.add_widget(self.todo_list_view)

        # Button to clear completed todos
        clear_completed_button = Button(text='Clear Completed Items', size_hint_y=None, height=30)
        clear_completed_button.bind(on_press=self.clear_completed_todos)
        self.layout.add_widget(clear_completed_button)

        # Text input for new todo
        self.new_todo = TextInput(hint_text='Enter a new todo', size_hint_y=None, height=30)
        self.layout.add_widget(self.new_todo)

        # Add, Remove, and Complete buttons
        button_layout = BoxLayout(size_hint_y=None, height=30)

        # TextInput for Todo number to complete
        self.todo_number_input = TextInput(hint_text='Enter number of todo to complete', size_hint_y=None, height=30)
        self.layout.add_widget(self.todo_number_input)

        add_button = Button(text='Add Todo')
        add_button.bind(on_press=self.add_todo)
        button_layout.add_widget(add_button)

        complete_button = Button(text='Complete Todo')
        complete_button.bind(on_press=self.complete_todo)
        button_layout.add_widget(complete_button)

        self.layout.add_widget(button_layout)

        # Update the todo list view
        self.update_todo_list()

        return self.layout

    def clear_completed_todos(self, instance):
        self.todos = [todo for todo in self.todos if 'completed' not in todo]
        self.write_todos()
        self.update_todo_list()
    
    def read_todos(self):
        try:
            with open("todo_data.txt", "r") as file:
                return file.readlines()
        except FileNotFoundError:
            return []

    def write_todos(self):
        with open("todo_data.txt", "w") as file:
            file.writelines(self.todos)

    def add_todo(self, instance):
        todo = self.new_todo.text + '\n'
        if todo.strip():
            self.todos.append(todo)
            self.write_todos()
            self.update_todo_list()
            self.new_todo.text = ''

    def complete_todo(self, instance):
        try:
            todo_number = int(self.todo_number_input.text) - 1
            if 0 <= todo_number < len(self.todos):
                todo = self.todos[todo_number]
                if 'completed' not in todo:
                    self.todos[todo_number] = f'{todo.strip()} completed\n'
                    self.write_todos()
                    self.update_todo_list()
            self.todo_number_input.text = ''  # Clear the input field
        except ValueError:
            print("Please enter a valid number.")

        self.write_todos()
        self.update_todo_list()

    def update_todo_list(self):
        self.todo_list_view.update_data(self.todos)

if __name__ == '__main__':
    TodoApp().run()
