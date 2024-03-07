from celery import shared_task  
from .models import User
import flask_excel
from flask import current_app
from .mailservice import send_message
from .models import User,Role
from jinja2 import Template
import os

@shared_task(ignore_result=False)
def create_resource_csv():
    with current_app.app_context():    
       
        dload=User.query.with_entities(User.username,User.email_address).all()
        csv_output =flask_excel.make_response_from_query_sets(dload, ["username","email_address"], "csv")
        filename ="test.csv"

        with open(filename, 'wb') as f:
            f.write(csv_output.data)

        return filename    
    

@shared_task(ignore_result=True)
def daily_reminder(to, subject):
    users = User.query.all()
    for user in users:
       
        file_path = os.path.join(os.path.dirname(__file__), 'test.html')
        with open(file_path, 'r') as f:
            template = Template(f.read())
            send_message(user.email_address, subject,
                         template.render(email=user.email_address))
    return "OK"