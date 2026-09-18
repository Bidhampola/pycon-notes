from db.conn import db

#create dataabse tables

class PyconNotes(db.Model):
    __tablename__ = 'pycon_notes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    speaker = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<PyconNotes {self.title}>'


#user Model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'