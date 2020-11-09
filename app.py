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
# app.config['SECRET_KEY'] = os.urandom(24)
app.config['SECRET_KEY'] = 'AAAAaaaaaatest'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # 配置7天有效
app._static_folder = "./static"
# CORS(app)
# database_url = subprocess.run(
#     ['heroku', 'config:get', 'DATABASE_URL', '--app', 'your-heroku-app-name'],
#     stdout=subprocess.PIPE,
# ).stdout
DATABASE_URL = os.environ['DATABASE_URL']


def create_user_table():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    create_users = "CREATE TABLE IF NOT EXISTS Users (code TEXT NOT NULL, Q1Time TEXT NOT NULL, Q1Progress TEXT NOT NULL, Q2Progress TEXT NOT NULL, Q3Time TEXT NOT NULL, Q3Progress TEXT NOT NULL, S1 TEXT NOT NULL, S2 TEXT NOT NULL, S3 TEXT NOT NULL, S4 TEXT NOT NULL, S5 TEXT NOT NULL, S6 TEXT NOT NULL, S7 TEXT NOT NULL, S8 TEXT NOT NULL, S9 TEXT NOT NULL, S10 TEXT NOT NULL, S11 TEXT NOT NULL, S12 TEXT NOT NULL, S13 TEXT NOT NULL, S14 TEXT NOT NULL, S15 TEXT NOT NULL);"
    

    cur.execute(create_users)

    conn.commit()
    conn.close()

def insert_row_to_users(value):

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    cur.execute("INSERT INTO dflp6gjthan76g (code, Q1Time, Q1Progress, Q2Progress, Q3Time, Q3Progress, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12, S13, S14, S15) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8], value[9], value[10], value[11], value[12], value[13], value[14], value[15], value[16], value[17], value[18], value[19], value[20]))
    
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

    # userId = letter + '-' + first + '-' + second + '-' + third + '-' + number
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
            
        
        letter = session.get('letter', None)
        first = session.get('first', None)
        second = session.get('second', None)
        third = session.get('third', None)
        number = str(uuid.uuid4())

        code = letter + '-' + first + '-' + second + '-' + third + '-' + number
        insertValue.append(code)
        # create_user_table()
        insert_row_to_users(insertValue)
        print(insertValue)
        return render_template('final.html',code=code)

if __name__ == '__main__':  
    app.run(debug=True)