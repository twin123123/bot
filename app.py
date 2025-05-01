from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    account_number = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=0.0)

# Создать БД при старте
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/register', methods=['POST'])
def register():
    user = User(
        name=request.form['name'],
        address=request.form['address'],
        age=int(request.form['age']),
        account_number=request.form['account_number']
    )
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/roulette', methods=['GET', 'POST'])
def roulette():
    result = None
    if request.method == 'POST':
        bet = float(request.form['bet'])
        number = random.randint(0, 36)
        # выигрыш 35× при угадывании точного числа
        if number == int(request.form['number']):
            result = f"Выпало {number}! Вы выиграли {bet*35:.2f}."
        else:
            result = f"Выпало {number}. Вы проиграли {bet:.2f}."
    return render_template('roulette.html', result=result)

@app.route('/redblack', methods=['GET', 'POST'])
def redblack():
    result = None
    colors = ['Красное', 'Чёрное']
    # для примера: чётные – чёрное, нечётные – красное
    if request.method == 'POST':
        bet = float(request.form['bet'])
        choice = request.form['color']
        rolled = random.choice(colors)
        if rolled == choice:
            result = f"Выпало {rolled}! Вы выиграли {bet*2:.2f}."
        else:
            result = f"Выпало {rolled}. Вы проиграли {bet:.2f}."
    return render_template('redblack.html', result=result)

@app.route('/rate')
def rate():
    # Пример получения курса с CoinGecko
    res = requests.get(
        'https://api.coingecko.com/api/v3/simple/price',
        params={'ids': 'bitcoin', 'vs_currencies': 'usd'}
    ).json()
    price = res.get('bitcoin', {}).get('usd')
    return render_template('rate.html', price=price)

if __name__ == '__main__':
    app.run(debug=True)
