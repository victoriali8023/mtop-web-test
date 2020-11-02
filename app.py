from flask import Flask, render_template, request, session
from flask_session import Session
from datetime import timedelta
import requests
import uuid
import os
import random
from random import randint
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 配置7天有效
app._static_folder = "./static"
# app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://isagwxjbrwjrvt:387f572542c82fd58f586b71c11a6f999c4035a43239b02f65292424e827dab9@ec2-3-208-224-152.compute-1.amazonaws.com:5432/dflp6gjthan76g'

# def create_user_table():
#     conn = sqlite3.connect("pokeInfo.sqlite")
#     cur = conn.cursor()

#     create_users = '''
#         CREATE TABLE IF NOT EXISTS "Users" (
#             "Id"    INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
#             "UserId" TEXT NOT NULL,
#             "FirstAnswer"  TEXT NOT NULL,
#             "SecondAnswer" TEXT NOT NULL,
#             "ThirdAnswer" TEXT NOT NULL
#         );
#     '''
#     cur.execute(create_users)

#     conn.commit()
#     conn.close()

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
    session.permanent = True # 长期有效

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
    return render_template('secondScenario.html')

@app.route('/secondGame')
def secondGame():
    userId = session.get('user', None)
    letter = userId[0]
    interface = userId[6:9] +'.png'
    question = 'q' + userId[7:9]
    return render_template('secondGame.html', question=question, interface=interface, letter=letter)

# @app.route('/questionnaire')
# def questionnaire():
#     return render_template('questionnaire.html')

if __name__ == '__main__':  
    app.run(debug=True)