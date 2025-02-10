import os
import json
from models.project import Project
from models.task import Task

class FileStorage:
    def __init__(self, filename='projects.json'):
        """
        Инициализация хранилища.
        Данные сохраняются в указанном файле, который находится внутри папки 'to_do_app'.
        """
        # Определяем базовую директорию проекта, поднимаясь на уровень выше из директории storage
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
        self.filename = os.path.join(base_dir, filename)

    def load_projects(self):
        """
        Загружает список проектов из JSON-файла.
        Если файл не найден, возвращает пустой список.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                projects = [Project.from_dict(item) for item in data]
            return projects
        except FileNotFoundError:
            return []

    def save_projects(self, projects):
        """
        Сохраняет список проектов в JSON-файл.
        """
        data = [project.to_dict() for project in projects]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_tasks(self):
        """
        Загружает список задач из JSON-файла.
        Если файл не найден, возвращает пустой список.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                tasks = [Task.from_dict(item) for item in data]
            return tasks
        except FileNotFoundError:
            return []

    def save_tasks(self, tasks):
        """
        Сохраняет список задач в JSON-файл.
        """
        data = [task.to_dict() for task in tasks]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)