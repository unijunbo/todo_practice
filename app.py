from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__, static_url_path='/static', static_folder='static') #static = javascript, css 등

# config.py 설정파일
app.config.from_object('config') #경로

db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import User, TodoFolder, Todo

ma = Marshmallow(app)
from serializers import TodoFolderSchema, TodoSchema




test_user_id = 19 #로그인 구현 안되서 임의로 사용하는 유저 아이디

@app.route('/')
def index():
    return render_template (
        'index.html'
    )

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        data = request.form.to_dict() #{'Name': 'lorem', 'Password': 'ipsum'}
        user = User(data['Name'], data['Password'])
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            return jsonify({'message': 'already exist'})
        return jsonify({'message': 'Registration OK'})


@app.route('/registration_check', methods=['POST'])
def registration_check():
    data = request.form.to_dict()
    user_list = User.query.filter_by(username=data['Name']).all() #.all() = 필터링 하고 가져오는 조건
    if len(user_list) >= 1:
        return jsonify({'message': 'already exist'})
    else:
        return jsonify({'message': 'good'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.form.to_dict()
        user_list = User.query.filter_by(username=data['Name'], password=data['Password']).all()
        if len(user_list) != 0:
            return redirect(url_for('todo_folder'))
        else:
            return 'Login fail'


@app.route('/todo_folder')
def todo_folder():
    return render_template (
        'todo_folder.html'
    )

@app.route('/todo_folder_api', methods=['GET', 'POST'])
def todo_folder_api():
    if request.method == 'GET':
        todo_folder_list = TodoFolder.query.filter_by(user_id=test_user_id).all() #object의 list 상태
        serializer = TodoFolderSchema(many=True) #파이썬의 기본 데이터타입으로 시리얼라이즈화
        response_data = serializer.dump(todo_folder_list) #적용
        return jsonify(response_data) #리턴

    elif request.method == 'POST':
        data = request.form.to_dict()
        todo_folder = TodoFolder(test_user_id, data['title'])
        try:
            db.session.add(todo_folder)
            db.session.commit()
        except Exception:
            return jsonify({'message': 'already exist'})

        todo_folder_list = TodoFolder.query.filter_by(user_id=test_user_id).all() #all() -> object가 리스트 형태로 변한됨
        # list_tasks = [List_task, List_task, ...]
        serializer = TodoFolderSchema(many=True)
        response_data = serializer.dump(todo_folder_list)
        return jsonify(response_data)
        

#################################################
#todo에 대한 내용

@app.route('/todo_folder/<int:todo_folder_id>')
def todos(todo_folder_id):
    return render_template (
        'todos.html'
    )

@app.route('/todo_folder_api/<int:todo_folder_id>', methods=['GET', 'POST'])
def todos_api(todo_folder_id):
    if request.method == 'GET':
        todo_folder = TodoFolder.query.get(todo_folder_id)
        todo_list = Todo.query.filter_by(todo_folder_id=todo_folder_id).all()
        serializer = TodoSchema(many=True)
        response_data = {
            'todoFolderTitle': todo_folder.title,
            'todoList': serializer.dump(todo_list)
        }
        return jsonify(response_data)

    elif request.method == 'POST':
        data = request.form.to_dict() #javascript로 만들어진 json형태의 데이터를 python 딕셔너리로 변환
        todo_title = Todo(test_user_id, todo_folder_id, data['todo_title'])
        try:
            db.session.add(todo_title)
            db.session.commit()
        except Exception as e:
            return jsonify({'message': str(e)})
        
        todo_list = Todo.query.filter_by(todo_folder_id=todo_folder_id).all()
        serializer = TodoSchema(many=True)
        response_data = serializer.dump(todo_list)
        return jsonify(response_data)
        
#################################################