from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os

API_KEY = os.environ.get('THE_MOVIE_DB_API')
MOVIE_SEARCH_URL = 'https://api.themoviedb.org/3/search/movie'
MOVIE_INFO_URL = 'https://api.themoviedb.org/3/movie'
MOVIE_DB_IMAGE_URL = 'https://image.tmdb.org/t/p/w500'

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# SQLite Database with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
Bootstrap(app)
db = SQLAlchemy(app=app)

# WTForm - adding a movie
class AddMovieForm(FlaskForm):
    movie_title = StringField(label='Movie Title', validators=[DataRequired()])
    submit = SubmitField(label='Add Movie')

# WTForm - RateMovieForm
class RateMovieForm(FlaskForm):
    rating_form = StringField(label='Your rating out of 10 (e.g. 7.5)', validators=[DataRequired()])
    review_form = StringField(label='Your review', validators=[DataRequired()])
    submit = SubmitField(label='Done')

# create Movies table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=True)
    year = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(500), unique=True, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, unique=True, nullable=True)
    review = db.Column(db.String(100), unique=True, nullable=True)
    img_url = db.Column(db.String, unique=True, nullable=True)

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
    # get all movies - sorted by ranting
    all_movies = Movie.query.order_by(Movie.rating).all()

    # loop through the movies
    for i in range(len(all_movies)):
        # give each movie a ranking 
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("index.html", movies=all_movies)

@app.route('/add', methods=['GET', 'POST'])
def add():
    add_movie_form = AddMovieForm()
    if add_movie_form.validate_on_submit():
        movie_title = add_movie_form.movie_title.data   # get the requested movie title
        response = requests.get(url=MOVIE_SEARCH_URL, params={'api_key': API_KEY, 'query': movie_title})
        data = response.json()['results']
        # pprint(data)
        return render_template('select.html', result=data)
    return render_template('add.html', form=add_movie_form)

@app.route('/edit', methods=['GET', 'POST'])
def rate_movie():
    rate_movie_form = RateMovieForm()
    # get current movie id
    movie_id = request.args.get('id')
    print(movie_id)
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

# finding details for a specific movie
@app.route('/find')
def movie_find():
    # get the movie id
    movie_id = request.args.get('id')
    if movie_id:
        # if movie id exits, then find the movie
        movie_details_url = f'{MOVIE_INFO_URL}/{movie_id}'
        response = requests.get(url=movie_details_url, params={'api_key':API_KEY})
        data = response.json()
        # create new Movie object
        new_movie = Movie(
                        title=data['title'],
                        year=data['release_date'].split('-')[0],
                        description=data['overview'],
                        img_url=f'{MOVIE_DB_IMAGE_URL}{data["poster_path"]}',
                        )
        # add movie to database
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('rate_movie', id=new_movie.id))

@app.route('/delete')
def delete_movie():
    # delete movie
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    # delete movie in database
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
