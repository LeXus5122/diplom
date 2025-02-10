from models.task import Task

class CLI:
    def __init__(self, todo_list, storage):
        """
        Инициализация CLI с объектами списка задач и хранилища.
        """
        self.todo_list = todo_list
        self.storage = storage

    def show_menu(self):
        """Выводит меню команд."""
        print("\nВыберите команду:")
        print("1. Показать задачи")
        print("2. Добавить задачу")
        print("3. Отметить задачу как выполненную")
        print("4. Удалить задачу")
        print("5. Выход")

    def run(self):
        """Запускает основной цикл взаимодействия с пользователем."""
        while True:
            self.show_menu()
            choice = input("Введите номер команды: ").strip()
            if choice == "1":
                self.list_tasks()
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.mark_task_done()
            elif choice == "4":
                self.remove_task()
            elif choice == "5":
                # При завершении работы сохраняем задачи
                self.storage.save_tasks(self.todo_list.get_tasks())
                print("Выход из приложения...")
                break
            else:
                print("Неверная команда! Пожалуйста, попробуйте снова.")

    def list_tasks(self):
        """Выводит список задач."""
        tasks = self.todo_list.get_tasks()
        if tasks:
            print("\nСписок задач:")
            for task in tasks:
                print(task)
        else:
            print("\nНет задач.")

    def add_task(self):
        """Запрашивает описание задачи и добавляет её в список."""
        description = input("Введите описание задачи: ").strip()
        if description:
            task = Task(description)
            self.todo_list.add_task(task)
            print("Задача успешно добавлена.")
        else:
            print("Описание не может быть пустым!")

    def mark_task_done(self):
        """Запрашивает ID задачи и отмечает её как выполненную."""
        task_id = input("Введите ID задачи для отметки выполнения: ").strip()
        if self.todo_list.mark_task_done(task_id):
            print("Задача отмечена как выполненная.")
        else:
            print("Задача с таким ID не найдена.")

    def remove_task(self):
        """Запрашивает ID задачи и удаляет её из списка."""
        task_id = input("Введите ID задачи для удаления: ").strip()
        if self.todo_list.remove_task(task_id):
            print("Задача удалена.")
        else:
            print("Задача с таким ID не найдена.")