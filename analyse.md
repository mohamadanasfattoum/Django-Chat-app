Daphne as ASGI Server

htmx 

Redis


----------------------------------------

HTTP REQUEST ----> urls.py, views.py, return

WEBSOCKET ------> routing.py, consumers.py, send()

CHannel Layer ------> async_to_sync, group_send()

------------------------------------------
pip freeze > requirement.txt


python manage.py migrate
python manage.py runserver