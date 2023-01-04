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

# WTForm - RateMovieForm
class RateMovieForm(FlaskForm):
    rating_form = StringField(label='Your rating out of 10 (e.g. 7.5)', validators=[DataRequired()])
    review_form = StringField(label='Your review', validators=[DataRequired()])
    submit = SubmitField(label='Done')

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

# new_movie = Movie(title="Phone Booth",
#                         year=2002,
#                         description="Publicist Stuart Shepard finds himself trapped in a phone booth, "\
#                             "pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, "\
#                                 "Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#                         rating=7.3,            
#                         ranking=10,
#                         review="My favourite character was the caller.",
#                         img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#                     )
# db.session.add(new_movie)
# db.session.commit()

@app.route("/")
def home():
    # get all movies
    all_movies = Movie.query.all()          
    return render_template("index.html", movies=all_movies)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/edit', methods=['GET', 'POST'])
def rate_movie():
    rate_movie_form = RateMovieForm()
    # get current movie id
    movie_id = request.args.get('id')
    # use that id to get the movie associated with it
    movie = Movie.query.get(movie_id)
    if rate_movie_form.validate_on_submit():
        # change the rating and the review
        movie.rating = float(rate_movie_form.rating_form.data)
        movie.review = rate_movie_form.review_form.data
        # commit changes onto database
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=rate_movie_form, movie=movie)


if __name__ == '__main__':
    app.run(debug=True)
