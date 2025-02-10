import uuid
from models.task import Task

class Project:
    def __init__(self, name, tasks=None, id=None):
        """
        Инициализация проекта.
        name — название проекта.
        tasks — список задач (экземпляры Task).
        """
        self.id = id if id is not None else str(uuid.uuid4())
        self.name = name
        self.tasks = tasks if tasks is not None else []

    def add_task(self, task):
        """Добавляет задачу в проект."""
        self.tasks.append(task)

    def remove_task(self, task_id):
        """Удаляет задачу по её идентификатору.
        Возвращает True, если задача была удалена.
        """
        original_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        return len(self.tasks) < original_count

    def update_task_status(self, task_id, new_status):
        """Обновляет статус задачи по её идентификатору.
        Возвращает True, если задача найдена и обновлена.
        """
        for task in self.tasks:
            if task.id == task_id:
                task.status = new_status
                return True
        return False

    @classmethod
    def from_dict(cls, dict_obj):
        """Создаёт объект Project из словаря."""
        tasks = [Task.from_dict(task) for task in dict_obj.get("tasks", [])]
        return cls(name=dict_obj["name"], tasks=tasks, id=dict_obj["id"])

    def to_dict(self):
        """Преобразует объект проекта в словарь для сохранения."""
        return {
            "id": self.id,
            "name": self.name,
            "tasks": [task.to_dict() for task in self.tasks]
        }