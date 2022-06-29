from venv import create
from __init__ import db, create_app
from models import User
from flask_migrate import Migrate

#db.create_all(app=create_app())

migrate = Migrate(app=create_app(),db=db)