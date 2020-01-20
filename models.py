from app import db

class User(db.Model): #클래스 안에 또 클래스를 씀
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class TodoFolder(db.Model):
    __table_name__ = 'todo_folder'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, title):
        self.user_id = user_id
        self.title = title
    

class Todo(db.Model):
    __table_name__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    todo_folder_id = db.Column(db.Integer, db.ForeignKey('todo_folder.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, list_task_id, todo):
        self.user_id = user_id
        self.list_task_id = list_task_id
        self.todo = todo
    


