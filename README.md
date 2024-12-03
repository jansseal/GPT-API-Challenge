# Fridge Raider Web App
GPT API Challenge Group for Oregon State University Capstone Project: Alex Rogers, Kevin Luk, Matthew Bourque, and Daksh Pandit

## Requirements
- Python 3.x
- Node.js and npm

## Current Status
The app is live and hosted on Heroku. You can access it here: https://gentle-fjord-52441-774e6189e8cb.herokuapp.com/
- The frontend build has been integrated into Flask for deployment on Heroku.
- While there are still CORS errors to resolve, the project can be run locally to view frontend/UI updates and test the recipe generation feature. However, login and account creation won't work locally due to the backend URL pointing to the live Heroku instance.

### Running the App Locally
1. From the root of the project, run:
~~~
python run.py
~~~
2. Before running the app, ensure the frontend build is updated by:
- Navigating to the frontend folder:
~~~
cd frontend
~~~
- Building the frontend:
~~~
npm run build
~~~
- Copying the contents of the frontend/public folder to the backend/static folder, replacing the existing contents.

## Deployment to Heroku
To deploy changes to Heroku, follow these steps:

### Prerequisites
- Ensure you have the Heroku CLI installed.

### Deployment Steps
1. Log in to Heroku:
~~~
heroku login
~~~
2. Add the Heroku remote if not already added:
~~~
git remote add heroku <your-heroku-git-url>
~~~
3. Push changes to Heroku:
~~~
git push heroku <your-branch-name>:main
~~~
4. If database migrations are required (e.g., changes to models):
- Open a Heroku shell:
~~~
heroku run bash
~~~
- Navigate to the app folder and run:
~~~
flask db upgrade
~~~
5. Exit the Heroku shell:
~~~
exit
~~~

## Notes
- The Heroku app uses a Heroku Postgres database tied to the project. Any changes to the database schema should be migrated using Flask-Migrate as shown above.

## Backend Setup (Flask + SQLite)

1. Clone the repository
2. Create and activate the virtual environment:
~~~
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
~~~
3. Install dependencies:
~~~
pip install -r requirements.txt
~~~
4. Initialize the SQLite Database:
~~~
python -m backend.setup_db
~~~
5. Run the Flask server to ensure there are no errors:
~~~
python run.py
~~~

## Frontend Setup (Svelte)

1. Navigate to the frontend folder:
~~~
cd frontend
~~~
2. Install dependencies:
~~~
npm install
~~~
3. Run the Svelte development server to ensure there are no errors:
~~~
npm run dev
~~~

## Contributing
Please branch off from `main` and submit a pull request for any changes.
