from flask import Flask, render_template, request, session
from flask_session import Session
from datetime import timedelta
import requests
import uuid
import os
import random
from random import randint
import psycopg2
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # 配置7天有效
app._static_folder = "./static"
# database_url = subprocess.run(
#     ['heroku', 'config:get', 'DATABASE_URL', '--app', 'your-heroku-app-name'],
#     stdout=subprocess.PIPE,
# ).stdout
DATABASE_URL = os.environ['DATABASE_URL']


def insert_row_to_users(value):

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    insert_user = '''
        INSERT INTO Effects
        VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    cur.execute(insert_user, value)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    letterList = ['A', 'B', 'C']
    firstSession = ['11', '12']
    secondSession = ['21', '22']
    thirdSession = ['31', '32']

    letter = random.choice(letterList)
    first = letter + random.choice(firstSession)
    second = letter + random.choice(secondSession)
    third = letter + random.choice(thirdSession)
    number = str(uuid.uuid4())

    userId = letter + '-' + first + '-' + second + '-' + third + '-' + number
    session['user'] = userId
    session.permanent = True

    return render_template('index.html')

@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/firstScenario')
def firstScenario():
    return render_template('firstScenario.html')

@app.route('/firstGame')
def firstgame():
    userId = session.get('user', None)
    letter = userId[0]
    interface = userId[2:5] +'.png'
    question = 'q' + userId[3:5]
    return render_template('firstGame.html', question=question, interface=interface, letter=letter)

@app.route('/q11')
def q11():
    return render_template('q11.html')

@app.route('/q12')
def q12():
    return render_template('q12.html')

@app.route('/secondScenario', methods=['POST'])
def secondScenario():
    if request.method == 'POST':
        session['q1Time'] = request.form['time']
        session['q1Progress'] = request.form['progress']
        
        return render_template('secondScenario.html')

@app.route('/secondGame')
def secondGame():
    userId = session.get('user', None)
    letter = userId[0]
    interface = userId[6:9] +'.png'
    question = 'q' + userId[7:9]
    return render_template('secondGame.html', question=question, interface=interface, letter=letter)

@app.route('/q21')
def q21():
    return render_template('q21.html')

@app.route('/q22')
def q22():
    return render_template('q22.html')

@app.route('/thirdScenario', methods=['POST'])
def thirdScenario():
    if request.method == 'POST':
        session['q2Progress'] = request.form['progress']
        print(session.get('q2Progress', None))
        return render_template('thirdScenario.html')

@app.route('/thirdGame')
def thirdGame():
    userId = session.get('user', None)
    letter = userId[0]
    interface = userId[10:13] +'.png'
    question = 'q' + userId[11:13]
    return render_template('thirdGame.html', question=question, interface=interface, letter=letter)

@app.route('/q31')
def q31():
    return render_template('q31.html')

@app.route('/q32')
def q32():
    return render_template('q32.html')

@app.route('/questionnaire',methods=['POST'])
def questionnaire():
    if request.method == 'POST':
        session['q3Time'] = request.form['time']
        session['q3Progress'] = request.form['progress']
        
        return render_template('questionnaire.html')


@app.route('/final',methods=['POST'])
def final():
    insertValue = []
    insertValue.append(session.get('q1Time', None))
    insertValue.append(session.get('q1Progress', None))
    insertValue.append(session.get('q2Progress', None))
    insertValue.append(session.get('q3Time', None))
    insertValue.append(session.get('q3Progress', None))
    
    if request.method == 'POST':
        for i in range(1,16):
            name = 's' + str(i)
            insertValue.append(request.form[name])
            
        insert_row_to_users(insertValue)
        print(insertValue)
        code = session.get('user', None)
        return render_template('final.html',code=code)

if __name__ == '__main__':  
    app.run(debug=True)