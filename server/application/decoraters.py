from flask import abort
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from models import User

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        current_username = get_jwt_identity()
        user = User.query.filter_by(username=current_username).first()

        if not user or user.role_id != 1:
            abort(403, description="Admin access required")  

        return func(*args, **kwargs)
    return decorated_function

def librarian_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        current_username = get_jwt_identity()
        user = User.query.filter_by(username=current_username).first()

        if not user or user.role_id != 2:
            abort(403, description="Librarian access required")  

        return func(*args, **kwargs)
    return decorated_function
