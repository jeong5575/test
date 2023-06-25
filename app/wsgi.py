from flask import Flask, render_template, request, redirect, url_for, session, abort
import mariadb
from datetime import datetime
import bcrypt
from datetime import datetime, timedelta
import requests
import socket

app = Flask(__name__) # 초기화

app = Flask(__name__)
app.secret_key = 'secret_key'

def hash_password(password):
    # 솔트 생성
    salt = bcrypt.gensalt()
    
    # 비밀번호 해시화
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password.decode('utf-8')


#야구 이미지 설정
def team_img(team):
    if team == "Atlanta Braves":
        image = "<img src='/static/baseball/Atlanta-Braves.png'  width='48' height='48'>"
    elif team == 'Miami Marlins':
        image = "<img src='/static/baseball/Miami-Marlins.png'  width='48' height='48'>"
    elif team == 'New York Mets':
        image = "<img src='/static/baseball/New-York-Mets.png'  width='48' height='48'>"
    elif team == "Philadelphia Phillies":
        image = "<img src='/static/baseball/Philadelphia-Phillies.png'  width='48' height='48'>"
    elif team == 'Washington Nationals':
        image = "<img src='/static/baseball/Washington-Nationals.png'  width='48' height='48'>"
    elif team == 'Chicago Cubs':
        image = "<img src='/static/baseball/Chicago-Cubs.png'  width='48' height='48'>"
    elif team == "Cincinnati Reds":
        image = "<img src='/static/baseball/Cincinnati-Reds.png' width='48' height='48'>"
    elif team == "Milwaukee Brewers":
        image = "<img src='/static/baseball/Milwaukee-Brewers.png' width='48' height='48'>"
    elif team == "Pittsburgh Pirates":
        image = "<img src='/static/baseball/Pittsburgh-Pirates.png' width='48' height='48'>"
    elif team == "St. Louis Cardinals":
        image = "<img src='/static/baseball/St.-Louis-Cardinals.png' width='48' height='48'>"
    elif team == "Arizona Diamondbacks":
        image = "<img src='/static/baseball/Arizona-Diamondbacks.png' width='48' height='48'>"
    elif team == "Colorado Rockies":
        image = "<img src='/static/baseball/Colorado-Rockies.png' width='48' height='48'>"
    elif team == "Los Angeles Dodgers":
        image = "<img src='/static/baseball/Los-Angeles-Dodgers.png' width='48' height='48'>"
    elif team == "San Diego Padres":
        image = "<img src='/static/baseball/San-Diego-Padres.png' width='48' height='48'>"
    elif team == "San Francisco Giants":
        image = "<img src='/static/baseball/San-Francisco-Giants.png' width='48' height='48'>"
    elif team == "Baltimore Orioles":
        image = "<img src='/static/baseball/Baltimore-Orioles.png' width='48' height='48'>"
    elif team == "Boston Red Sox":
        image = "<img src='/static/baseball/Boston-Red-Sox.png' width='48' height='48'>"
    elif team == "New York Yankees":
        image = "<img src='/static/baseball/New-York-Yankees.png' width='48' height='48'>"
    elif team == "Tampa Bay Rays":
        image = "<img src='/static/baseball/Tampa-Bay-Rays.png' width='48' height='48'>"
    elif team == "Toronto Blue Jays":
        image = "<img src='/static/baseball/Toronto-Blue-Jays.png' width='48' height='48'>"
    elif team == "Chicago White Sox":
        image = "<img src='/static/baseball/Chicago-White-Sox.png' width='48' height='48'>"
    elif team == "Cleveland Guardians":
        image = "<img src='/static/baseball/Cleveland-Guardians.png' width='48' height='48'>"
    elif team == "Detroit Tigers":
        image = "<img src='/static/baseball/Detroit-Tigers.png' width='48' height='48'>"
    elif team == "Kansas City Royals":
        image = "<img src='/static/baseball/Kansas-City-Royals.png' width='48' height='48'>"
    elif team == "Minnesota Twins":
        image = "<img src='/static/baseball/Minnesota-Twins.png' width='48' height='48'>"
    elif team == "Houston Astros":
        image = "<img src='/static/baseball/Houston-Astros.png' width='48' height='48'>"
    elif team == "Los Angeles Angels":
        image = "<img src='/static/baseball/Los-Angeles-Angels.png' width='48' height='48'>"
    elif team == "Oakland Athletics":
        image = "<img src='/static/baseball/Oakland-Athletics.png' width='48' height='48'>"
    elif team == "Seattle Mariners":
        image = "<img src='/static/baseball/Seattle-Mariners.png' width='48' height='48'>"
    elif team == "Texas Rangers":
        image = "<img src='/static/baseball/Texas-Rangers.png' width='48' height='48'>"
    else:
        image = ""

    return image

@app.route('/') # 요청 주소
def hello_world(): # 함수
    name = '클라우드'
    # 데이터베이스에서 랜덤한 운세(luck) 값 가져오기
    conn = mariadb.connect(
        user='team2',
        password='team2',
        host='15.164.153.191',
        port=3306,
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT luck FROM luckyday ORDER BY RAND() LIMIT 1")
    luck = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    hostname = socket.gethostname() #호스트 정보를 받아와서 저장
    return render_template('index.html', use_name=name, fortune=luck ,hostname = hostname )

	

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 데이터베이스에서 사용자 정보 확인
        conn = mariadb.connect(
            user='team2',
            password='team2',   
            host='15.164.153.191',
            port=3306,
            database='team2'
        )
        cursor = conn.cursor()
        query = "SELECT * FROM member WHERE email = %s"
        cursor.execute(query, (email,))
        result2 = cursor.fetchone()
        
        if result2:
            result = bcrypt.checkpw(password.encode('utf-8'), result2[1].encode('utf-8'))
            if result:
                # 로그인 성공 시 세션에 사용자 정보 저장
                session['email'] = email
                session['name'] = result2[2]
                cursor.close()
                conn.close()
                return redirect(url_for('home'))
            else:
                cursor.close()
                conn.close()
                return "<script>alert(\'비밀번호가 일치하지 않습니다.\');window.history.back();</script>"
        else:
            cursor.close()
            conn.close()
            return "<script>alert(\'해당 이메일에 대한 사용자 정보가 없습니다.\');window.history.back();</script>"
        
        
@app.route('/dashboard')
def dashboard():
    return  render_template('home.html')
def get_weather_data(city):
    api_key = 'e18e47c8dab3f721628d4b3b493da7ab'  # OpenWeatherMap API 키
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    return data

def kelvin_to_fahrenheit(kelvin):
    fahrenheit = (kelvin - 273.15) * 9/5 + 32
    return fahrenheit

def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return celsius


#메인화면
@app.route('/home')
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        city = 'Seoul'  # 날씨 정보를 가져올 도시명
        weather_data = get_weather_data(city)
        #   온도 변환
        temperature = weather_data['main']['temp']
        celsius = kelvin_to_celsius(temperature)
        fahrenheit = kelvin_to_fahrenheit(temperature)
        
        return render_template('home.html', weather_data=weather_data, celsius=celsius, fahrenheit=fahrenheit)


#로그아웃
@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')


#회원가입
@app.route('/join', methods=['GET','POST']) #GET(정보보기), POST(정보수정) 메서드 허용
def join():
    if request.method == 'GET':
        return render_template("join.html")
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        Password = request.form.get('password')
        
        Hashedpassword =  hash_password(Password)
        confirm_password = request.form.get('confirm_password')
       
        if not(name and email and Password and confirm_password):
            return "<script>alert(\'입력되지 않은 정보가 있습니다.\');window.history.back();</script>"
        elif Password != confirm_password:
            return "<script>alert(\'비밀번호가 일치하지 않습니다.\');window.history.back();</script>"
        else:
            conn = mariadb.connect(
            user='team2',
            password='team2',   
            host='15.164.153.191',
            port=3306,
            database='team2'
            )
            cursor = conn.cursor()
            confirm = "SELECT * FROM member WHERE email = %s;"
            cursor.execute(confirm,(email,))
            result = cursor.fetchone()
            if result :
                cursor.close()
                conn.close()
                return "<script>alert(\'이미 가입된 이메일입니다.\');window.history.back();</script>"
            else :
                query = "INSERT INTO member(NAME, PASSWORD, email) VALUE (%s,%s,%s);"
                cursor.execute(query, (name, Hashedpassword,email))
                conn.commit()
                cursor.close()
                conn.close()

            return render_template('index.html')

           




#################################################################################################################
#################################################################################################################
####자유게시판
@app.route('/community')
def community():
    conn = mariadb.connect(
        host='15.164.153.191',
        port=3306,
        user='team2',
        password='team2',
        database='team2'
    )
    cursor = conn.cursor()

    freesearch = request.args.get('freesearch')

    if freesearch:
        query = "SELECT B_numb,title, member.name, TIME FROM board JOIN member ON  member.email=board.email WHERE board_type='free' AND (content like concat('%%', %s, '%%') OR title like concat('%%', %s, '%%')) ORDER BY B_numb DESC;"
        cursor.execute(query,(freesearch,freesearch))
        posts = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return  render_template('community.html', posts=posts)
    else: 
        query = "SELECT B_numb, title, member.name, TIME FROM board JOIN member ON member.email=board.email WHERE board_type='free' ORDER BY B_numb DESC;"
        cursor.execute(query)
        posts = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return  render_template('community.html', posts=posts)


    # 게시글 보기와 댓글 작성
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    if request.method == 'POST':
        content = request.form['content']
        email = session['email']  # 현재 로그인한 사용자의 이메일

        conn = mariadb.connect(
            user='team2',
            password='team2',   
            host='15.164.153.191',
            port=3306,
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO comments (answer, time, B_numb, email)
            VALUES (%s, %s, %s, %s)
        ''', (content, datetime.now(), post_id, email))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('view_post', post_id=post_id))

    conn = mariadb.connect(
        user='team2',
        password='team2',   
        host='15.164.153.191',
        port=3306,
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute('''SELECT B_numb, title, email, content, time
                     FROM board
                     WHERE B_numb = %s''', (post_id,))
    post = cursor.fetchone()
    cursor.execute('''SELECT * FROM comments WHERE B_numb = %s ORDER BY C_numb ASC''', (post_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('post.html', post=post, comments=comments)



@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        author = session['email']  # 현재 로그인한 사용자의 이메일을 사용합니다.
        content = request.form['content']
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = mariadb.connect(
            host='15.164.153.191',
            port=3306,
            user='team2',
            password='team2',
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO board (title, email, content, time, board_type)
                         VALUES (%s, %s, %s, %s, %s)''', (title, author, content, created_at, 'free'))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('community'))
    return render_template('new_post.html')



# 자유게시판 검색
@app.route('/search_free')
def search_free():
    query = request.args.get('query')

    conn = mariadb.connect(
        user='team2',
        password='team2',
        host='15.164.153.191',
        port=3306,
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM board WHERE board_type = 'free' AND title LIKE %s", ('%' + query + '%',))
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('search_free.html', results=results)

#검색
@app.route('/search')
def search():
    query = request.args.get('query')

    conn = mariadb.connect(
        user='team2',
        password='team2',
        host='15.164.153.191',
        port=3306,
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM board WHERE title LIKE %s", ('%' + query + '%',))
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('search_results.html', results=results)


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        # 게시글 작성자 정보 가져오기
        conn = mariadb.connect(
            host='15.164.153.191',
            port=3306,
            user='team2',
            password='team2',
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM board WHERE B_numb = %s", (post_id,))
        post_author = cursor.fetchone()
        cursor.close()
        conn.close()
        
        # 현재 로그인한 사용자 정보 가져오기
        current_user = session.get('email')

        # 현재 로그인한 사용자와 게시글 작성자가 일치하는 경우에만 수정 가능
        if current_user == post_author[0]:
            conn = mariadb.connect(
                host='15.164.153.191',
                port=3306,
                user='team2',
                password='team2',
                database='team2'
            )
            cursor = conn.cursor()
            cursor.execute("UPDATE board SET title = %s, content = %s WHERE B_numb = %s", (title, content, post_id))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('view_post', post_id=post_id))
        else:
            # 권한이 없는 경우에 대한 처리 (예: 에러 페이지 또는 메시지 표시)
            return "You are not authorized to edit this post."
        
    conn = mariadb.connect(
        host='15.164.153.191',
        port=3306,
        user='team2',
        password='team2',
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM board WHERE B_numb = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_post.html', post=post)

# 게시글 삭제
@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    # 게시글 작성자 정보 가져오기
    conn = mariadb.connect(
        host='15.164.153.191',
        port=3306,
        user='team2',
        password='team2',
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM board WHERE B_numb = %s", (post_id,))
    post_author = cursor.fetchone()
    cursor.close()
    conn.close()
    
    # 현재 로그인한 사용자 정보 가져오기
    current_user = session.get('email')

    # 현재 로그인한 사용자와 게시글 작성자가 일치하는 경우에만 삭제 가능
    if current_user == post_author[0]:
        conn = mariadb.connect(
            host='15.164.153.191',
            port=3306,
            user='team2',
            password='team2',
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM board WHERE B_numb = %s", (post_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('community'))
    else:
        # 권한이 없는 경우에 대한 처리 (예: 에러 페이지 또는 메시지 표시)
        return "You are not authorized to delete this post."
# 댓글 삭제
@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    conn = mariadb.connect(
        user='team2',
        password='team2',
        host='15.164.153.191',
        port=3306,
        database='team2'
    )
    cursor = conn.cursor()

    # 댓글 작성자 확인
    cursor.execute("SELECT email FROM comments WHERE C_numb = %s", (comment_id,))
    result = cursor.fetchone()
    if result is None:
        abort(404)  # 댓글을 찾을 수 없음
    comment_author = result[0]

    # 현재 사용자 확인
    current_user = session.get('email')
    if current_user != comment_author:
        abort(403)  # 접근이 금지됨
    
    # 댓글 삭제
    cursor.execute("DELETE FROM comments WHERE C_numb = %s", (comment_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(request.referrer)




#################################################################################################################
#################################################################################################################

####질의응답
@app.route('/qna')
def getQNAList():
    conn = mariadb.connect(
            user='team2',
            password='team2',   
            host='15.164.153.191',
            port=3306,
            database='team2'
            )
    cursor = conn.cursor()
    qnasearch = request.args.get('qnasearch')

    if qnasearch:
        query = "SELECT title, member.name, TIME, B_numb FROM board JOIN member ON  member.email=board.email WHERE board_type='QnA' AND (content like concat('%%', %s, '%%') OR title like concat('%%', %s, '%%')) ORDER BY B_numb DESC;"
        cursor.execute(query,(qnasearch,qnasearch))
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return  render_template('qna.html', rows=rows)
    else: 
        query = "SELECT title, member.name, TIME, B_numb FROM board JOIN member ON member.email=board.email WHERE board_type='QnA'ORDER BY B_numb DESC;"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return  render_template('qna.html', rows=rows)
    

      # 질문내용 보기와 댓글 작성
@app.route('/qna/<int:post_id>', methods=['GET', 'POST'])
def view_qna(post_id):
    if request.method == 'POST':
        content = request.form['content']
        email = session['email']  # 현재 로그인한 사용자의 이메일

        conn = mariadb.connect(
            user='team2',
            password='team2',   
            host='15.164.153.191',
            port=3306,
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO comments (answer, time, B_numb, email)
            VALUES (%s, %s, %s, %s)
        ''', (content, datetime.now(), post_id, email))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('view_qna', post_id=post_id))

    conn = mariadb.connect(
        user='team2',
        password='team2',   
        host='15.164.153.191',
        port=3306,
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute('''SELECT B_numb, title, email, content, time
                     FROM board
                     WHERE B_numb = %s''', (post_id,))
    qna = cursor.fetchone()
    cursor.execute('''SELECT * FROM comments WHERE B_numb = %s ORDER BY C_numb ASC''', (post_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_qna.html', qna=qna, comments=comments)


@app.route('/new_qna', methods=['GET', 'POST'])
def new_qna():
    if request.method == 'POST':
        title = request.form['title']
        author = session['email']  # 현재 로그인한 사용자의 이메일을 사용합니다.
        content = request.form['content']
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = mariadb.connect(
            host='15.164.153.191',
            port=3306,
            user='team2',
            password='team2',
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO board (title, email, content, time, board_type)
                         VALUES (%s, %s, %s, %s, %s)''', (title, author, content, created_at, 'QnA'))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('getQNAList'))
    return render_template('new_qna.html')


@app.route('/edit_qna/<int:post_id>', methods=['GET', 'POST'])
def edit_qna(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        # 게시글 작성자 정보 가져오기
        conn = mariadb.connect(
            host='15.164.153.191',
            port=3306,
            user='team2',
            password='team2',
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM board WHERE B_numb = %s", (post_id,))
        post_author = cursor.fetchone()
        cursor.close()
        conn.close()
        
        # 현재 로그인한 사용자 정보 가져오기
        current_user = session.get('email')

        # 현재 로그인한 사용자와 게시글 작성자가 일치하는 경우에만 수정 가능
        if current_user == post_author[0]:
            conn = mariadb.connect(
                host='15.164.153.191',
                port=3306,
                user='team2',
                password='team2',
                database='team2'
            )
            cursor = conn.cursor()
            cursor.execute("UPDATE board SET title = %s, content = %s WHERE B_numb = %s", (title, content, post_id))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('view_qna', post_id=post_id))
        else:
            # 권한이 없는 경우에 대한 처리 (예: 에러 페이지 또는 메시지 표시)
            return "<script>alert(\'권한이 없습니다.\');window.history.back();</script>"
        
    conn = mariadb.connect(
        host='15.164.153.191',
        port=3306,
        user='team2',
        password='team2',
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM board WHERE B_numb = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_qna.html', post=post)

# 질문 삭제
@app.route('/delete_qna/<int:post_id>', methods=['POST'])
def delete_qna(post_id):
    # 질문 작성자 정보 가져오기
    conn = mariadb.connect(
        host='15.164.153.191',
        port=3306,
        user='team2',
        password='team2',
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM board WHERE B_numb = %s", (post_id,))
    post_author = cursor.fetchone()
    cursor.close()
    conn.close()
    
    # 현재 로그인한 사용자 정보 가져오기
    current_user = session.get('email')

    # 현재 로그인한 사용자와 게시글 작성자가 일치하는 경우에만 삭제 가능
    if current_user == post_author[0]:
        conn = mariadb.connect(
            host='15.164.153.191',
            port=3306,
            user='team2',
            password='team2',
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM board WHERE B_numb = %s", (post_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('getQNAList'))
    else:
        # 권한이 없는 경우에 대한 처리 (예: 에러 페이지 또는 메시지 표시)
        return "<script>alert(\'권한이 없습니다.\');window.history.back();</script>"











#################################################################################################################
#################################################################################################################
##스터디 모집 게시판
@app.route('/study')
def study():
    conn = mariadb.connect(
            user='team2',
            password='team2',   
            host='15.164.153.191',
            port=3306,
            database='team2'
            )
    cursor = conn.cursor()
    studysearch = request.args.get('studysearch')

    if studysearch:
        query = "SELECT title, member.name, TIME, B_numb FROM board JOIN member ON  member.email=board.email WHERE board_type='Study' AND (content like concat('%%', %s, '%%') OR title like concat('%%', %s, '%%')) ORDER BY B_numb DESC;"
        cursor.execute(query,(studysearch,studysearch))
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return  render_template('study.html', rows=rows)
    else: 
        query = "SELECT title, member.name, TIME, B_numb FROM board JOIN member ON member.email=board.email WHERE board_type='Study'ORDER BY B_numb DESC;"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return  render_template('study.html', rows=rows)
    

      # 질문내용 보기와 댓글 작성
@app.route('/study/<int:post_id>', methods=['GET', 'POST'])
def view_study(post_id):
    if request.method == 'POST':
        content = request.form['content']
        email = session['email']  # 현재 로그인한 사용자의 이메일

        conn = mariadb.connect(
            user='team2',
            password='team2',   
            host='15.164.153.191',
            port=3306,
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO comments (answer, time, B_numb, email)
            VALUES (%s, %s, %s, %s)
        ''', (content, datetime.now(), post_id, email))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('view_study', post_id=post_id))

    conn = mariadb.connect(
        user='team2',
        password='team2',   
        host='15.164.153.191',
        port=3306,
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute('''SELECT B_numb, title, email, content, time
                     FROM board
                     WHERE B_numb = %s''', (post_id,))
    study = cursor.fetchone()
    cursor.execute('''SELECT * FROM comments WHERE B_numb = %s ORDER BY C_numb ASC''', (post_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_study.html', study=study, comments=comments)


@app.route('/new_study', methods=['GET', 'POST'])
def new_study():
    if request.method == 'POST':
        title = request.form['title']
        author = session['email']  # 현재 로그인한 사용자의 이메일을 사용합니다.
        content = request.form['content']
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = mariadb.connect(
            host='15.164.153.191',
            port=3306,
            user='team2',
            password='team2',
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO board (title, email, content, time, board_type)
                         VALUES (%s, %s, %s, %s, %s)''', (title, author, content, created_at, 'Study'))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('study'))
    return render_template('new_study.html')


@app.route('/edit_study/<int:post_id>', methods=['GET', 'POST'])
def edit_study(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        # 게시글 작성자 정보 가져오기
        conn = mariadb.connect(
            host='15.164.153.191',
            port=3306,
            user='team2',
            password='team2',
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM board WHERE B_numb = %s", (post_id,))
        post_author = cursor.fetchone()
        cursor.close()
        conn.close()
        
        # 현재 로그인한 사용자 정보 가져오기
        current_user = session.get('email')

        # 현재 로그인한 사용자와 게시글 작성자가 일치하는 경우에만 수정 가능
        if current_user == post_author[0]:
            conn = mariadb.connect(
                host='15.164.153.191',
                port=3306,
                user='team2',
                password='team2',
                database='team2'
            )
            cursor = conn.cursor()
            cursor.execute("UPDATE board SET title = %s, content = %s WHERE B_numb = %s", (title, content, post_id))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('view_study', post_id=post_id))
        else:
            # 권한이 없는 경우에 대한 처리 (예: 에러 페이지 또는 메시지 표시)
            return "<script>alert(\'권한이 없습니다.\');window.history.back();</script>"
        
    conn = mariadb.connect(
        host='15.164.153.191',
        port=3306,
        user='team2',
        password='team2',
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM board WHERE B_numb = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_study.html', post=post)

# 질문 삭제
@app.route('/delete_study/<int:post_id>', methods=['POST'])
def delete_study(post_id):
    # 질문 작성자 정보 가져오기
    conn = mariadb.connect(
        host='15.164.153.191',
        port=3306,
        user='team2',
        password='team2',
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM board WHERE B_numb = %s", (post_id,))
    post_author = cursor.fetchone()
    cursor.close()
    conn.close()
    
    # 현재 로그인한 사용자 정보 가져오기
    current_user = session.get('email')

    # 현재 로그인한 사용자와 게시글 작성자가 일치하는 경우에만 삭제 가능
    if current_user == post_author[0]:
        conn = mariadb.connect(
            host='15.164.153.191',
            port=3306,
            user='team2',
            password='team2',
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM board WHERE B_numb = %s", (post_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('study'))
    else:
        # 권한이 없는 경우에 대한 처리 (예: 에러 페이지 또는 메시지 표시)
        return "<script>alert(\'권한이 없습니다.\');window.history.back();</script>"
    


#################################################################################################################
#################################################################################################################
##공지사항


@app.route('/notice')
def notice():
    conn = mariadb.connect(
            user='team2',
            password='team2',   
            host='15.164.153.191',
            port=3306,
            database='team2'
            )
    cursor = conn.cursor()
    noticesearch = request.args.get('noticesearch')

    if noticesearch:
        query = "SELECT title, member.name, TIME, B_numb FROM board JOIN member ON  member.email=board.email WHERE board_type='Notice' AND (content like concat('%%', %s, '%%') OR title like concat('%%', %s, '%%')) ORDER BY B_numb DESC;"
        cursor.execute(query,(noticesearch,noticesearch))
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        print(rows)
        return  render_template('notice.html', rows=rows)
    else: 
        query = "SELECT title, member.name, TIME, B_numb FROM board JOIN member ON member.email=board.email WHERE board_type='Notice'ORDER BY B_numb DESC;"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        print(rows)

        return  render_template('notice.html', rows=rows)
    
    

      # 질문내용 보기와 댓글 작성
@app.route('/notice/<int:post_id>', methods=['GET', 'POST'])
def view_notice(post_id):
    if request.method == 'POST':
        content = request.form['content']
        email = session['email']  # 현재 로그인한 사용자의 이메일

        conn = mariadb.connect(
            user='team2',
            password='team2',   
            host='15.164.153.191',
            port=3306,
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO comments (answer, time, B_numb, email)
            VALUES (%s, %s, %s, %s)
        ''', (content, datetime.now(), post_id, email))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('view_notice', post_id=post_id))

    conn = mariadb.connect(
        user='team2',
        password='team2',   
        host='15.164.153.191',
        port=3306,
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute('''SELECT B_numb, title, email, content, time
                     FROM board
                     WHERE B_numb = %s''', (post_id,))
    notice = cursor.fetchone()
    cursor.execute('''SELECT * FROM comments WHERE B_numb = %s ORDER BY C_numb ASC''', (post_id,))
    comments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_notice.html', notice=notice, comments=comments)


@app.route('/new_notice', methods=['GET', 'POST'])
def new_notice():

    if (session['email'] == 'admin@admin.com'):
        if request.method == 'POST':
            title = request.form['title']
            author = session['email']  # 현재 로그인한 사용자의 이메일을 사용합니다.
            content = request.form['content']
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
            conn = mariadb.connect(
                host='15.164.153.191',
                port=3306,
                user='team2',
                password='team2',
                database='team2'
            )
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO board (title, email, content, time, board_type)
                            VALUES (%s, %s, %s, %s, %s)''', (title, author, content, created_at, 'Notice'))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('notice'))
        return render_template('new_notice.html')
    else: return "<script>alert(\'접근 권한이 없습니다.\');window.history.back();</script>" # Redirect to login page if not authenticated


@app.route('/edit_notice/<int:post_id>', methods=['GET', 'POST'])
def edit_notice(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        # 게시글 작성자 정보 가져오기
        conn = mariadb.connect(
            host='15.164.153.191',
            port=3306,
            user='team2',
            password='team2',
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM board WHERE B_numb = %s", (post_id,))
        post_author = cursor.fetchone()
        cursor.close()
        conn.close()
        
        # 현재 로그인한 사용자 정보 가져오기
        current_user = session.get('email')

        # 현재 로그인한 사용자와 게시글 작성자가 일치하는 경우에만 수정 가능
        if current_user == post_author[0]:
            conn = mariadb.connect(
                host='15.164.153.191',
                port=3306,
                user='team2',
                password='team2',
                database='team2'
            )
            cursor = conn.cursor()
            cursor.execute("UPDATE board SET title = %s, content = %s WHERE B_numb = %s", (title, content, post_id))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('view_notice', post_id=post_id))
        else:
            # 권한이 없는 경우에 대한 처리 (예: 에러 페이지 또는 메시지 표시)
            return "<script>alert(\'권한이 없습니다.\');window.history.back();</script>"
        
    conn = mariadb.connect(
        host='15.164.153.191',
        port=3306,
        user='team2',
        password='team2',
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM board WHERE B_numb = %s", (post_id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_notice.html', post=post)

# 질문 삭제
@app.route('/delete_notice/<int:post_id>', methods=['POST'])
def delete_notice(post_id):
    # 질문 작성자 정보 가져오기
    conn = mariadb.connect(
        host='15.164.153.191',
        port=3306,
        user='team2',
        password='team2',
        database='team2'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM board WHERE B_numb = %s", (post_id,))
    post_author = cursor.fetchone()
    cursor.close()
    conn.close()
    
    # 현재 로그인한 사용자 정보 가져오기
    current_user = session.get('email')

    # 현재 로그인한 사용자와 게시글 작성자가 일치하는 경우에만 삭제 가능
    if current_user == post_author[0]:
        conn = mariadb.connect(
            host='15.164.153.191',
            port=3306,
            user='team2',
            password='team2',
            database='team2'
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM board WHERE B_numb = %s", (post_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('notice'))
    else:
        # 권한이 없는 경우에 대한 처리 (예: 에러 페이지 또는 메시지 표시)
        return "<script>alert(\'권한이 없습니다.\');window.history.back();</script>"
    

#################################################################################################################


## 야구 api 시작 ## 

@app.route('/games')
def show_scores():
    game_index = request.args.get('game_index', 0, type=int)

    # 현재 날짜를 구합니다.
    current_date = datetime.now().date()

    # 어제의 날짜를 계산합니다.
    yesterday = current_date - timedelta(days=1)

    # 어제의 경기 결과를 가져오는 API 호출
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={yesterday}"
    response = requests.get(url)
    data = response.json()

    # 경기 결과 추출
    games = []
    if "dates" in data and len(data["dates"]) > 0:
        games = data["dates"][0].get("games", [])

    num_games = len(games)
    if game_index < 0 or game_index >= num_games:
        game_index = 0

    game = games[game_index]
    away_team = game["teams"]["away"]["team"]["name"]
    home_team = game["teams"]["home"]["team"]["name"]

    # 점수 데이터가 'score' 키 아래에 있는지 확인하고 가져옵니다.
    away_score = game["teams"]["away"].get("score")
    home_score = game["teams"]["home"].get("score")

    if away_score is not None and home_score is not None:
        if away_score == home_score:
            winning_team = "동점"
        else:
            winning_team = away_team if away_score > home_score else home_team
    else:
        # 경기가 없는 경우 "경기를 하지 않았습니다" 출력
        winning_team = "경기를 하지 않았습니다"

    # 팀 로고 이미지 경로를 생성합니다.
    away_logo = url_for('static', filename=f'baseball/{away_team.replace(" ", "-")}.png')
    home_logo = url_for('static', filename=f'baseball/{home_team.replace(" ", "-")}.png')

    scores = [{
        "away_team": away_team,
        "home_team": home_team,
        "away_score": away_score,
        "home_score": home_score,
        "winning_team": winning_team,
        "away_logo": away_logo,
        "home_logo": home_logo
    }]

    return render_template('scores.html', scores=scores, current_game_index=game_index, num_games=num_games)

@app.route('/scores')
def redirect_to_scores():
    return redirect(url_for('show_scores'))

### 야구 api 끝 ##


#################################################################################################################

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True) # flask 실행

