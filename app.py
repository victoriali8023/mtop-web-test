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
from flask_cors import CORS, cross_origin

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
@cross_origin(supports_credentials=True)
def index():
    letterList = ['A', 'B', 'C']
    # firstSession = ['11', '12']
    # secondSession = ['21', '22']
    # thirdSession = ['31', '32']

    letter = random.choice(letterList)
    # first = letter + random.choice(firstSession)
    # second = letter + random.choice(secondSession)
    # third = letter + random.choice(thirdSession)
    # number = str(uuid.uuid4())

    userId = letter + '-' + first + '-' + second + '-' + third + '-' + number
    session['letter'] = letter
    # session['user'] = userId
    session.permanent = True

    return render_template('index.html')

@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/firstScenario')
def firstScenario():
    return render_template('firstScenario.html')

@app.route('/firstGame')
@cross_origin(supports_credentials=True)
def firstgame():
    firstSession = ['11', '12']
    first = random.choice(firstSession)

    letter = session.get('letter', None)
    interface = letter + first +'.png'
    question = 'q' + first
    session['first'] = first
    session.permanent = True
    return render_template('firstGame.html', question=question, interface=interface, letter=letter)

@app.route('/q11')
def q11():
    return render_template('q11.html')

@app.route('/q12')
def q12():
    return render_template('q12.html')

@app.route('/secondScenario', methods=['POST'])
@cross_origin(supports_credentials=True)
def secondScenario():
    if request.method == 'POST':
        session['q1Time'] = request.form['time']
        session['q1Progress'] = request.form['progress']
        
        return render_template('secondScenario.html')

@app.route('/secondGame')
@cross_origin(supports_credentials=True)
def secondGame():
    secondSession = ['21', '22']
    second = random.choice(secondSession)

    letter = session.get('letter', None)
    interface = letter + second +'.png'
    question = 'q' + second
    session['second'] = second
    session.permanent = True
    return render_template('secondGame.html', question=question, interface=interface, letter=letter)

@app.route('/q21')
def q21():
    return render_template('q21.html')

@app.route('/q22')
def q22():
    return render_template('q22.html')

@app.route('/thirdScenario', methods=['POST'])
@cross_origin(supports_credentials=True)
def thirdScenario():
    if request.method == 'POST':
        session['q2Progress'] = request.form['progress']
        session.permanent = True
        return render_template('thirdScenario.html')

@app.route('/thirdGame')
@cross_origin(supports_credentials=True)
def thirdGame():
    thirdSession = ['31', '32']
    third = random.choice(thirdSession)

    letter = session.get('letter', None)
    interface = letter + third +'.png'
    question = 'q' + third
    session['third'] = third
    session.permanent = True
    return render_template('thirdGame.html', question=question, interface=interface, letter=letter)

@app.route('/q31')
def q31():
    return render_template('q31.html')

@app.route('/q32')
def q32():
    return render_template('q32.html')

@app.route('/questionnaire',methods=['POST'])
@cross_origin(supports_credentials=True)
def questionnaire():
    if request.method == 'POST':
        session['q3Time'] = request.form['time']
        session['q3Progress'] = request.form['progress']
        session.permanent = True
        return render_template('questionnaire.html')


@app.route('/final',methods=['POST'])
@cross_origin(supports_credentials=True)
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
        letter = session.get('letter', None)
        first = session.get('first', None)
        second = session.get('second', None)
        third = session.get('third', None)
        number = str(uuid.uuid4())

        code = letter + '-' + first + '-' + second + '-' + third + '-' + number
        return render_template('final.html',code=code)

if __name__ == '__main__':  
    app.run(debug=True)