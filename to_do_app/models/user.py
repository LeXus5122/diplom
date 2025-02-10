import uuid

class User:
    def __init__(self, username, password, id=None):
        """
        Инициализация пользователя.
        username — логин пользователя.
        password — пароль (в демонстрационных целях хранится в простом виде, на практике следует применять хеширование).
        """
        self.id = id if id is not None else str(uuid.uuid4())
        self.username = username
        self.password = password

    def to_dict(self):
        """Преобразует объект пользователя в словарь для сохранения."""
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password
        }
    
    @classmethod
    def from_dict(cls, dict_obj):
        """Создаёт объект User из словаря."""
        return cls(dict_obj['username'], dict_obj['password'], dict_obj.get('id'))