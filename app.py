import psycopg2
from flask import Flask, render_template, request #플라스크 폴더에 렌더 템플릿 임포트

conn_string = "host='localhost' dbname='acnt' user='junbosim' password='1234'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

app = Flask(__name__)


@app.route('/') # <- URL의 경로가 이거 일때 밑에 함수 실행
def index():
    return render_template(
        'index.html',
        # title = 'Flask Template Test',
        # home_str = 'Hello Flask!',
        # home_list = [1, 2, 3, 4, 5]
        )



@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET': #html <a>는 HTTP 리퀘스트 GET 방식임 / HTTP 리퀘스트가 GET인지 POST인지 확인 
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.form.to_dict()
        sql = 'SELECT * FROM id_pw WHERE id = \'' + data['Name'] + '\' and ' + 'pw = ' + data['Password'] + ';' #로그인 정보가 맞는지 확인하는 식
        try:
            cur.execute(sql) #위에 써준 식을 실행하는 함수 #unique 데이터 타입이면 여기서 중복 확인하고 중복되면 에러
        except Exception:
            return 'id or password does not exist.'
        return 'Login OK.'

        # 2가지 방법이 있다.
        # 첫번째는, DB에서 파이썬 코드로 row data 몽땅 가져와서 요청받은 키값, 밸류값과 비교 *(비추: 훨씬느림)
        # 두번쨰는, sql로 DB에서 특정 row만 가져옴

        #acnt DB의 특정 TABLE에 어떻게 접속?
        #접속한 TABLE의 row에서 post 받은 값을 어떻게 true/fasle 비교?

        
@app.route('/registration', methods = ['GET', 'POST']) #GET, POST,...는 request의 종류들
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        data = request.form.to_dict() #request(클래스로 만들어진)오브젝트의 form(클래스로 만들어진)오브젝트의 to_dict()함수를 써서 dictionary한다.
        sql = 'INSERT INTO id_pw (id, pw) VALUES (\'' + data['Name'] + '\', ' + data['Password'] + ');' #dictionary화한 키값:벨류값을 id_pw 테이블에 넣어주기 위해 sql 명령어를 스트링화 해준다.
        cur.execute(sql) #cur의 execute 함수를 써서 위에 적어준 명령어를 실행 시킨다.
        conn.commit() #commit은 insert, delete, update 같은 row 제어할 경우에 마침표 개념으로 꼭 쓴다.
        return 'Registration OK'


