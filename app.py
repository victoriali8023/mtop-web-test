from flask import Flask, render_template, request, session
from flask_session import Session
from datetime import timedelta
import uuid
import os
import random
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 配置7天有效



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
    userId = session.get('user', None)
    return render_template('intro.html', userId=userId)

@app.route('/first')
def first():
    userId = session.get('user', None)
    return render_template('first.html', userId=userId)

if __name__ == '__main__':  
    app.run(debug=True)