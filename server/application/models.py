from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, func
from flask_login import UserMixin, LoginManager
from flask_bcrypt import Bcrypt
from datetime import datetime
import uuid


bcrypt = Bcrypt()

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

login_manager = LoginManager()


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=255), nullable=False)
   
    is_librarian = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=False)
    is_premium = db.Column(db.Boolean, default=False)
    fs_uniquifier = db.Column(db.String(36), default=str(uuid.uuid4))
    status = db.Column(db.String(length=20), default='pending')
    profile_picture = db.Column(db.String(length=255), nullable=True)
    bio = db.Column(db.String(length=255), nullable=True)
    last_login = db.Column(db.DateTime, default=None)
    last_login_day = db.Column(db.String(length=20), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))       
    role = db.relationship('Role', backref='users')

    @property
    def profile_picture_url(self):
        if self.profile_picture:
            return f"/static/profile_images/{self.profile_picture}"
        return "/static/default_profile_image.png"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def record_login(self):
        self.last_login = datetime.utcnow()
        login_day = datetime.now().strftime("%A")
        self.last_login_day = login_day
        db.session.commit()

    def __init__(self, username, email_address, password):
        self.username = username
        self.email_address = email_address
        self.password = password
        self.role_id=3

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"



class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    
    password_hash = db.Column(db.String(255), nullable=False) 
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    role = db.relationship('Role')

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Librarian(db.Model):
    __tablename__ = 'librarians'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)        
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='librarians')

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    





class Role(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))

###################################################################################    


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    authors = db.Column(db.String(255), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)    
    file_path = db.Column(db.String(255), nullable=True)

    section = db.relationship('Section', backref='books')

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
   
    borrower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    date_issued = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    returned = db.Column(db.Boolean, default=False, nullable=False)    

    borrower = db.relationship('User', backref='rentals')
    book = db.relationship('Book', backref='rentals')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship('User', backref=db.backref('comments', lazy=True))
    book = db.relationship('Book', backref=db.backref('comments', lazy=True))


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    user = db.relationship('User', backref='ratings')
    book = db.relationship('Book', backref='ratings')






