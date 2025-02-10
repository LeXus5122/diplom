import os
import json
from models.user import User

class UserStorage:
    def __init__(self, filename='users.json'):
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
        self.filename = os.path.join(base_dir, filename)
    
    def load_users(self):
        """Загружает список пользователей из JSON-файла."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                users = [User.from_dict(item) for item in data]
            return users
        except FileNotFoundError:
            return []
    
    def save_users(self, users):
        """Сохраняет список пользователей в JSON-файл."""
        data = [user.to_dict() for user in users]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)