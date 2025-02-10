from models.todo_list import TodoList
from storage.file_storage import FileStorage
from cli.cli import CLI

def main():
    # Инициализируем хранилище и загружаем существующие задачи
    storage = FileStorage("tasks.json")
    tasks = storage.load_tasks()
    
    # Создаем список задач на основе загруженных данных
    todo_list = TodoList(tasks)
    
    # Инициализируем и запускаем консольный интерфейс
    cli = CLI(todo_list, storage)
    cli.run()

if __name__ == "__main__":
    main()