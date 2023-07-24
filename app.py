from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# instantiate flask class
app = Flask(__name__)

# instantiate database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2016@localhost:5432/magicdb'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:2016@localhost:5432/magicdb'
# to deploy to cloud hosting platform like heroku, you need to provision a database server on heroku and replace with
#database u used during development
#app.config['SQLALCHEMY_DATABASE_URI'] = 'heroku database url'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instantiate sqlalchemy
db = SQLAlchemy(app)

app.app_context().push()


class Favquote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50))
    quote = db.Column(db.String(5000))

    

# create a route
@app.route('/')
def index():
    #fruits = ['apple','mango','rapsberries','banana','papaya','avocado']
    #quote = 'Kindness needs no translation'
    results = Favquote.query.all()
    return render_template('index.html', results=results) #quote=quote, fruits=fruits)


#@app.route('/about')
#def about():
#    return render_template('about.html')


@app.route('/quotes')
def quotes():
    return render_template('quotes.html')


@app.route('/process', methods=['POST'])
def process():
    author = request.form['author'] 
    quote = request.form['quote']
    quotedata = Favquote(author=author, quote=quote)

    db.session.add(quotedata)
    db.session.commit()
    return redirect(url_for('index'))

    
