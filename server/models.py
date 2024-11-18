from config import db

class SignUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "userName": self.first_name,
            "email": self.email,
            "password": self.password,
        }

class LabelDict(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Integer, unique=True, nullable=False)
    value = db.Column(db.String(80), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
        }
