from flask import Flask, render_template, request, jsonify #플라스크 폴더에 렌더 템플릿 임포트
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static', static_folder='static')

# config.py 설정파일
app.config.from_object('config') #경로

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User

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
            return 'Login OK'
        else:
            return 'Login fail'
