class TodoList:
    def __init__(self, tasks=None):
        """
        Инициализация списка задач.
        Если задачи не переданы, создаётся пустой список.
        """
        self.tasks = tasks if tasks is not None else []

    def add_task(self, task):
        """Добавляет задачу в список."""
        self.tasks.append(task)

    def remove_task(self, task_id):
        """Удаляет задачу по её идентификатору.
        
        Возвращает True, если задача была удалена.
        """
        original_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        return len(self.tasks) < original_count

    def mark_task_done(self, task_id):
        """Отмечает задачу как выполненную по идентификатору.
        
        Возвращает True, если задача найдена и отмечена.
        """
        for task in self.tasks:
            if task.id == task_id:
                task.mark_done()
                return True
        return False

    def get_tasks(self):
        """Возвращает текущий список задач."""
        return self.tasks
