To start up the application, you need to start both backend server and frontend server.

Backend server:
1.1 Database:
	We used PostgreSQL, so you need to install it before run the server. And we have a prepared script to setup initial data.
	1.2 Install dependencies
	cd $PROJECT_FOLDER
	pip install -r requirements.txt
	1.3 Data migration
	cd $PROJECT_FOLDER/prototype
	python manage.py makemigrations
	python manage.py migrate
	1.4 Start the server
	cd $PROJECT_FOLDER/prototype
	python manage.py runserver 7999

2. Frontend server:
	2.1 Node.js
	https://nodejs.org/en/
    Download and install the node.js library according to the platform.
    2.2 Install dependencies
    cd $PROJECT_FOLDER/prototype/apps/frontend
    npm install
    2.3 Run the server
    cd $PROJECT_FOLDER/prototype/apps/frontend
    npm run dev
