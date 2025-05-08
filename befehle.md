# to run celery
celery -A app.celery_app  worker --loglevel INFO

# to redis 

sudo apt install redis-server
sudo systemctl start redis
sudo systemctl status redis 



##
# django channels
pip install -U 'channels[daphne]'


##
pip freeze > requirement.txt