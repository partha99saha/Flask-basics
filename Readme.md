python3 -m venv venv
source venv/bin/activate

pip install Flask
pip freeze > requirements.txt
pip install -r requirements.txt


