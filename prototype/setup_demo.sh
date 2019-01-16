cp -p -r DemoData/user_files .
python3 manage.py makemigrations backend
python3 manage.py migrate
python3 manage.py loaddata DemoData/skillstash.json
cd apps/frontend
npm install
