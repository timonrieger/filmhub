# Filmhub

Filmhub is a web application that allows users to track and rate their favorite movies. Users can register, log in, add movies to their collection, and provide ratings and reviews.

## Features

- User authentication (registration, login, logout)
- Add movies to personal collection
- Rate and review movies
- View and edit movie details
- Delete movies from collection
- View top-rated movies

## Requirements

- Flask
- Flask-Bootstrap
- Flask-Login
- Flask-SQLAlchemy
- Requests
- Dotenv

## Setup

1. Clone the repository:
	```bash
	git clone https://github.com/timonrieger/filmhub.git
	cd filmhub
	```

2. Create a virtual environment and activate it:
	```bash
	python -m venv venv
	source venv/bin/activate  # On Windows use `venv\Scripts\activate`
	```

3. Install the required packages:
	```bash
	pip install -r requirements.txt
	```

4. Create a `.env` file and add your configuration:
	```env
	SECRET_KEY=your_secret_key
	DB_URI=your_database_uri
	AUTH_URL=your_auth_url (refer to [auth-service](https://github.com/timonrieger/auth-service))
	THEMOVIEDB_KEY=your_themoviedb_api_key (https://www.themoviedb.org/)
	```

5. Run the application:
	```bash
	flask run
	```

## Endpoints

- `/` - Home page showing top-rated movies
- `/<username>` - User's movie collection
- `/login` - User login
- `/register` - User registration
- `/logout` - User logout
- `/edit` - Edit movie rating and review
- `/delete` - Delete a movie from the collection
- `/add` - Add a new movie to the collection
- `/details` - View movie details and add to collection

## Usage

### Register a new user

1. Navigate to the registration page: `/register`
2. Fill in the registration form with your email, username, and password
3. Submit the form to create a new account

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.