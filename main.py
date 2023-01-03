from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# SQLite Database with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
Bootstrap(app)
db = SQLAlchemy(app=app)

# create Movies table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, unique=True, nullable=False)
    review = db.Column(db.String(100), unique=True, nullable=False)
    img_url = db.Column(db.String, unique=True, nullable=False)

app.app_context().push()
db.create_all()

@app.route("/")
def home():
    new_movie = Movie(title="Phone Booth",
                        year=2002,
                        description="Publicist Stuart Shepard finds himself trapped in a phone booth, "\
                            "pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, "\
                                "Stuart's negotiation with the caller leads to a jaw-dropping climax.",
                        rating=7.3,            
                        ranking=10,
                        review="My favourite character was the caller.",
                        img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
                    )
                        
    return render_template("index.html", movie=new_movie)

@app.route('/add')
def add():
    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)
