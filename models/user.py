from mongoengine import Document, StringField, EmailField, DateTimeField
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(Document):
    fullname = StringField(required=True, max_length=100)
    email = EmailField(required=True, unique=True)
    mobile = StringField(required=True, max_length=15, regex=r'^[6-9]\d{9}$')
    password_hash = StringField(required=True)
    role = StringField(required=True, choices=["student", "instructor"])
    created_at = DateTimeField(default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
