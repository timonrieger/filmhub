from flask import Flask, abort, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
import requests
import os
from database import db, create_all, User as UserModel, TopMovies
from dotenv import load_dotenv
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from forms import EditRatingForm, AddMovieForm, LoginForm, RegistrationForm, PasswordResetForm

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
db.init_app(app)
AUTH_URL = os.getenv("AUTH_URL")
THEMOVIEDB_KEY = os.getenv("THEMOVIEDB_KEY")


class User(UserMixin, UserModel):
    pass


with app.app_context():
    create_all(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.route("/")
def home():
    unique_movies = TopMovies.query.distinct(TopMovies.title).all()

    for movie in unique_movies:
        same_movie = TopMovies.query.filter_by(title=movie.title).all()
        movie.rating = sum([m.rating for m in same_movie]) / len(same_movie)

    sorted_movies = sorted(unique_movies, key=lambda x: x.rating)
    for i, movie in enumerate(sorted_movies):
        movie.ranking = len(sorted_movies) - i

    return render_template("index.html", movies=sorted_movies[::-1])


@app.route("/<username>")
def user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    movies = sorted(TopMovies.query.filter_by(user_id=user.id).all(), key=lambda x: x.rating)
    for i, movie in enumerate(movies):
        movie.ranking = len(movies) - i

    return render_template("index.html", movies=movies[::-1], user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        data = {
            "email": email,
            "password": password
        }
        app.logger.info(AUTH_URL)
        response = requests.post(url=f"{AUTH_URL}/login", json=data)
        if response.status_code == 200:
            flash(response.json()['message'], "success")
            login_user(user)
            return redirect(url_for("user", username=current_user.username))
        flash(response.json()['message'], "error")
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]
        data = {
            "email": email,
            "password": password,
            "username": username,
            "then": "https://filmhub.timonrieger.de/login"
        }
        response = requests.post(f"{AUTH_URL}/register", json=data)
        flash(response.json()['message'], "success") if response.status_code == 200 else flash(response.json()['message'], "error")
        
    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/reset", methods=["GET", "POST"])
def reset():
    form = PasswordResetForm()
    
    if form.validate_on_submit():
        email = form.email.data
        data = {
            "email": email,
            "then": "https://filmhub.timonrieger.de/login"
        }
        response = requests.post(url=f"{AUTH_URL}/reset", json=data)
        flash(response.json()['message'], "success") if response.status_code == 200 else flash(response.json()['message'], "error")
        
    return render_template("reset.html", form=form)


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    id = request.args.get("id")
    form = EditRatingForm()
    edit_movie = TopMovies.query.filter_by(id=id).first()
    if form.validate_on_submit():
        edit_movie.rating = form.rating.data
        edit_movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("user", username=current_user.username))
    movie = TopMovies.query.filter_by(id=id).first()
    if movie:
        form = EditRatingForm(rating=movie.rating, review=movie.review)
        return render_template("edit.html", form=form, id=id, movie_name=movie.title)
    return render_template("edit.html", form=form, id=id, movie_name=movie.title)


@app.route("/delete")
@login_required
def delete():
    id = request.args.get("id")
    delete_book = TopMovies.query.filter_by(id=id).first()
    db.session.delete(delete_book)
    db.session.commit()
    return redirect(url_for("user", username=current_user.username))


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        movie_list = requests.get(url=f"https://api.themoviedb.org/3/search/movie?query={movie_title}&api_key={THEMOVIEDB_KEY}").json()["results"]
        return render_template("select.html", movies=movie_list)

    return render_template("add.html", form=form)


@app.route("/details")
def movie_details():
    tmdb_movie_id = request.args.get("id")
    movie_details = requests.get(url=f"https://api.themoviedb.org/3/movie/{tmdb_movie_id}?api_key={THEMOVIEDB_KEY}").json()
    user_movies = TopMovies.query.filter_by(user_id=current_user.id).all()
    if movie_details['title'] in [movie.title for movie in user_movies]:
        flash("You have already added this movie.", "error")
        return
    else:
        movie = TopMovies(
            user_id=current_user.id,
            title=movie_details['title'],
            year=movie_details['release_date'].split("-")[0],
            description=movie_details['overview'],
            rating=0,
            review="None",
            img_url=f"https://image.tmdb.org/t/p/w500{movie_details['poster_path']}")
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for("edit", id=movie.id))


if __name__ == '__main__':
    app.run(debug=False)
