import uuid

class Task:
    def __init__(self, title, description, status="Планы", assigned_to="admin", comments=None, id=None):
        """
        Инициализация задачи.
        title — название задачи.
        description — подробное описание задачи.
        status — состояние задачи: "Планы", "В работе", "Тестирование", "Завершено".
        assigned_to — логин исполнителя, по умолчанию "admin".
        comments — список комментариев; каждый комментарий представляется словарём с ключами "author" и "text".
        """
        self.id = id if id is not None else str(uuid.uuid4())
        self.title = title
        self.description = description
        self.status = status
        self.assigned_to = assigned_to
        self.comments = comments if comments is not None else []

    def add_comment(self, author, text):
        """Добавляет комментарий к задаче."""
        comment = {"author": author, "text": text}
        self.comments.append(comment)

    def to_dict(self):
        """Преобразует задачу в словарь для сохранения."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "comments": self.comments
        }
    
    @classmethod
    def from_dict(cls, dict_obj):
        """Создаёт объект Task из словаря.
        Если старые записи не содержат поля title, используем описание как заголовок.
        """
        return cls(
            title=dict_obj.get("title", dict_obj.get("description", "Без названия")),
            description=dict_obj.get("description", ""),
            status=dict_obj.get("status", "Планы"),
            assigned_to=dict_obj.get("assigned_to", "admin"),
            comments=dict_obj.get("comments", []),
            id=dict_obj.get("id")
        )

    def __str__(self):
        return f"[{self.status}] {self.title} (ID: {self.id}) - Отв.: {self.assigned_to}"