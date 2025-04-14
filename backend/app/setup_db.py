from flask import Flask
from app.models import db  # where SQLAlchemy() is initialized
from app import models  # this will register your models
from app.config import Config  # optional: if you're storing config in a class

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # or just hardcode config if you want
    db.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Tables created successfully!")
