from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from functools import wraps
from models.project import Project
from models.task import Task
from models.user import User
from storage.file_storage import FileStorage
from storage.file_storage_users import UserStorage

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Задайте надежный секретный ключ

# Инициализируем хранилище проектов
project_storage = FileStorage("projects.json")
projects = project_storage.load_projects()

def save_projects():
    """Сохраняет текущий список проектов в файл."""
    project_storage.save_projects(projects)

def get_project(project_id):
    """Возвращает проект по его идентификатору."""
    for project in projects:
        if project.id == project_id:
            return project
    return None

# Инициализируем хранилище пользователей
user_storage = UserStorage("users.json")
users = user_storage.load_users()

# Если админ отсутствует, добавляем его по умолчанию
if not any(u.username == 'admin' for u in users):
    default_admin = User('admin', 'admin')
    users.append(default_admin)
    user_storage.save_users(users)

# Декоратор для проверки авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Пожалуйста, войдите в систему.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Декоратор для проверки прав администратора
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') != 'admin':
            flash("Доступ только для администратора.", "danger")
            return redirect(url_for('project_list'))
        return f(*args, **kwargs)
    return decorated_function

# Корневой URL
@app.route('/')
def home():
    return redirect(url_for('login'))

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = next((u for u in users if u.username == username and u.password == password), None)
        if user:
            session['logged_in'] = True
            session['username'] = username
            flash("Вы успешно вошли в систему.", "success")
            return redirect(url_for('project_list'))
        else:
            flash("Неверный логин или пароль.", "danger")
    return render_template('login.html')

# Выход из системы
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash("Вы вышли из системы.", "info")
    return redirect(url_for('login'))

# Новый маршрут для добавления/загрузки комментариев
@app.route('/project/<project_id>/task/<task_id>/comments', methods=['GET', 'POST'])
@login_required
def handle_comments(project_id, task_id):
    project = get_project(project_id)
    if not project:
        return jsonify({"error": "Проект не найден"}), 404
    task = next((t for t in project.tasks if t.id == task_id), None)
    if not task:
        return jsonify({"error": "Задача не найдена"}), 404
    
    if request.method == 'POST':
        comment_text = request.form.get('comment')
        author = session.get('username', 'unknown')
        if comment_text:
            task.add_comment(author, comment_text)
            save_projects()  # сохраняем изменения в файле
            return jsonify({"success": True, "comment": {"author": author, "text": comment_text}})
        else:
            return jsonify({"error": "Пустой комментарий"}), 400
    else:
        return jsonify({"comments": task.comments})

# Страница выбора проектов
@app.route('/projects')
@login_required
def project_list():
    return render_template("project_list.html", projects=projects)

# Создание нового проекта
@app.route('/projects/add', methods=['POST'])
@login_required
def add_project():
    name = request.form.get("name")
    if name:
        new_project = Project(name)
        projects.append(new_project)
        save_projects()
        flash("Проект успешно создан.", "success")
    else:
        flash("Название проекта не может быть пустым!", "warning")
    return redirect(url_for("project_list"))

# Удаление проекта
@app.route('/projects/delete/<project_id>')
@login_required
def delete_project(project_id):
    project = get_project(project_id)
    if project:
        projects.remove(project)
        save_projects()
        flash("Проект удалён.", "success")
    else:
        flash("Проект не найден.", "warning")
    return redirect(url_for("project_list"))

# Доска задач проекта (канбан)
@app.route('/project/<project_id>')
@login_required
def project_board(project_id):
    project = get_project(project_id)
    if not project:
        flash("Проект не найден.", "warning")
        return redirect(url_for("project_list"))
    statuses = ["Планы", "В работе", "Тестирование", "Завершено"]
    tasks_by_status = {status: [] for status in statuses}
    for task in project.tasks:
        tasks_by_status[task.status].append(task)
    return render_template("project_board.html", project=project, tasks_by_status=tasks_by_status, statuses=statuses, users=users)

# Добавление новой задачи в проект
@app.route('/project/<project_id>/task/add', methods=["POST"])
@login_required
def add_task(project_id):
    project = get_project(project_id)
    if not project:
        flash("Проект не найден.", "warning")
        return redirect(url_for("project_list"))
    title = request.form.get("title")
    description = request.form.get("description")
    assigned_to = request.form.get("assigned_to") or "admin"
    if title and description:
        new_task = Task(title, description, status="Планы", assigned_to=assigned_to)
        project.add_task(new_task)
        save_projects()
        flash("Задача успешно добавлена.", "success")
    else:
        flash("Название и описание задачи не могут быть пустыми!", "warning")
    return redirect(url_for("project_board", project_id=project_id))

# Обновление статуса задачи
@app.route('/project/<project_id>/task/<task_id>/update/<new_status>')
@login_required
def update_task_status(project_id, task_id, new_status):
    project = get_project(project_id)
    if not project:
        flash("Проект не найден.", "warning")
        return redirect(url_for("project_list"))
    if new_status not in ["Планы", "В работе", "Тестирование", "Завершено"]:
        flash("Некорректный статус.", "danger")
        return redirect(url_for("project_board", project_id=project_id))
    if project.update_task_status(task_id, new_status):
        save_projects()
        flash("Статус задачи обновлён.", "success")
    else:
        flash("Задача не найдена.", "warning")
    return redirect(url_for("project_board", project_id=project_id))

# Удаление задачи
@app.route('/project/<project_id>/task/<task_id>/delete')
@login_required
def delete_task(project_id, task_id):
    project = get_project(project_id)
    if not project:
        flash("Проект не найден.", "warning")
        return redirect(url_for("project_list"))
    if project.remove_task(task_id):
        save_projects()
        flash("Задача удалена.", "success")
    else:
        flash("Задача не найдена.", "warning")
    return redirect(url_for("project_board", project_id=project_id))

# Управление пользователями (только для admin)
@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_users():
    global users
    if request.method == 'POST':
        new_username = request.form.get('new_username').strip()
        new_password = request.form.get('new_password').strip()
        if new_username and new_password:
            if any(u.username == new_username for u in users):
                flash("Пользователь с таким логином уже существует.", "warning")
            else:
                new_user = User(new_username, new_password)
                users.append(new_user)
                user_storage.save_users(users)
                flash("Новый пользователь успешно создан.", "success")
        else:
            flash("Логин и пароль не могут быть пустыми.", "warning")
    return render_template("user_management.html", users=users)

# Удаление пользователя (только для admin)
@app.route('/admin/users/delete/<user_id>')
@login_required
@admin_required
def delete_user(user_id):
    global users
    user_to_delete = next((u for u in users if u.id == user_id), None)
    if user_to_delete:
        if user_to_delete.username == 'admin':
            flash("Нельзя удалить пользователя admin.", "danger")
        else:
            users = [u for u in users if u.id != user_id]
            user_storage.save_users(users)
            flash("Пользователь удалён.", "success")
    else:
        flash("Пользователь не найден.", "warning")
    return redirect(url_for('manage_users'))

if __name__ == '__main__':
    app.run(debug=True)