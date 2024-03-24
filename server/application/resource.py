from flask import request,session,jsonify,make_response,send_from_directory
from flask_restful import Resource, Api,reqparse,marshal_with,fields
from .models import db,User,Book,Section,Comment, Admin,Librarian,Role,Rating,Rental
from flask_jwt_extended import create_access_token,get_jwt_identity, jwt_required
import uuid
import os
from werkzeug.utils import secure_filename
from flask import current_app, send_file
from werkzeug.datastructures import FileStorage
from datetime import datetime, timedelta
from sqlalchemy import or_ 
from sqlalchemy.orm import joinedload
from .tasks import create_resource_csv
import flask_excel
from celery.result import AsyncResult
from .instances import cache





api = Api()



parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
parser.add_argument('password', type=str, required=True, help='Password cannot be blank')
parser.add_argument('email_address', type=str, required=True, help='Email cannot be blank') 

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
login_parser.add_argument('password', type=str, required=True, help='Password cannot be blank')


class AuthResource(Resource):
    def post(self):
        data = login_parser.parse_args()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=username, additional_claims={"role": user.role_id})
            return {'access_token': access_token, 'username': username, 'role': 'user','user_id' : user.id}, 200

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            access_token = create_access_token(identity=username, additional_claims={"role": "admin"})
            return {'access_token': access_token, 'username': username, 'role': 'admin'}, 200

        lib = Librarian.query.filter_by(username=username).first()
        if lib and lib.check_password(password):
            access_token = create_access_token(identity=username, additional_claims={"role": "librarian"})
            return {'access_token': access_token, 'username': username, 'role': 'librarian'}, 200

        return {'message': 'Invalid credentials'}, 401
    
class RegisterResource(Resource):
    def post(self):
        data = request.json  
        print(f"Received data: {data}")  

        username = data["username"]
        password = data["password"]
        confirm_password = data["confirm_password"]
        email = data["email_address"]

        if password != confirm_password:
            return {"error": "Passwords do not match"}, 400
     

        user_ex = User.query.filter_by(username=username).first()
        if user_ex:
            return {"error": "User already exists , kindly login "}, 400
        
        role_id = 3
        role = Role.query.get(role_id)
           
        new_user = User(
            username=username,
            email_address=email,
            password=password
                     
        )         
        db.session.add(new_user)
        db.session.commit()

        print(f"Returning response: New user created successfully")  
        return {"message": "New user created successfully"}, 200


class HelloWorld(Resource):
    def get(self):
        return {"message": 'You are now connected to unlimited supply of book click on logo to login '}
    
class Logout(Resource):
  def delete(self):
    if session.get('user_id'):
      session['user_id'] = None
      return {}, 204
    return {'error': 'Unauthorized'}, 401 
 

class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user_role = current_user.get('role')  

        if user_role == 'admin':
            return {'message': 'Welcome, Admin'}, 200
        elif user_role == 'librarian':
            return {'message': 'Welcome, Librarian'}, 200
        elif user_role == 'user':
            user = User.query.filter_by(id=current_user.get('id')).first() 
            if user:
                return {'message': f"Welcome, {user.name}"}, 200
            else:
                return {'message': 'User not found'}, 404
        else:
            return {'message': 'Unauthorized'}, 403
        

class GetUser(Resource):
    @jwt_required()        
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        if user:
            return {"user": user.username}, 200
        else:
            return {"message": "User not found"}, 404
# ...



        
       

api.add_resource(HelloWorld, '/')  
api.add_resource(AuthResource, '/login_api')
api.add_resource(Logout, '/logout')
api.add_resource(GetUser, "/get_user")
api.add_resource(RegisterResource, "/register_api")
api.add_resource(ProtectedResource, '/protected')

######################Tasks#######################

class DownloadResource(Resource):
    def get(self):
        tasks= create_resource_csv.delay()
        return jsonify({"task-id": tasks.id}) 
    
class GetCsvResource(Resource):
    def get(self,task_id):
        res = AsyncResult(task_id)
        if res.ready():
            filename =res.result
            return send_file(filename, as_attachment=True,download_name="test.csv")
        else:
            return {'message' : 'Task Pending'}, 304

api.add_resource(GetCsvResource,'/get_csv/<string:task_id>')
api.add_resource(DownloadResource,'/dload_csv')


 ######################SECTION########################



class AddSections(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        
        parser.add_argument('description', type=str, required=True)
        args = parser.parse_args()
      
       
  
        new_section = Section(
            name=args['name'],
    
            description=args['description']
        )

        db.session.add(new_section)
        db.session.commit()


        return {'message': 'Section added successfully', 'section_id': new_section.id},   201

class Search(Resource):
    def get(self):
        search_query = request.args.get('q', '')  
        sections = Section.query.filter(
                or_(
                Section.name.ilike(f"%{search_query}%"), 
                Section.description.ilike(f"%{search_query}%")
                )
            ).all()
        books = Book.query.filter(
            or_(
                Book.name.ilike(f"%{search_query}%"),
                Book.authors.ilike(f"%{search_query}%"), 
                Book.isbn.ilike(f"%{search_query}%")
                                                       
            )
        ).all()

        if not sections and not books:
            return jsonify({'message': 'No search results found'}), 404

        
        authors = [book.authors for book in books]

        results = {
            'sections': [{'id': section.id, 'name': section.name} for section in sections],
            'books': [{'id': book.id, 'name': book.name, 'authors': book.authors} for book in books],  # Include authors here
            'authors': authors  
        }
        return results,  200

    

class DeleteSection(Resource):
    def delete(self,section_id):
        section=Section.query.get(section_id)    
        if section is None:
            return {'message': 'Section not found'},404
        db.session.delete(section)
        db.session.commit()
        return {'message': 'Section deleted Successfully'},200

class UpdateSection(Resource):
    def post(self, section_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        section = Section.query.get(section_id)
        if section is None:
            return {'message': 'Section not found'},  404
        
        if 'name' in args:
            section.name = args['name']
        
        if 'description' in args:
            section.description = args['description']

        db.session.commit()
        return {'message': 'Section updated successfully'},  200

class getSection(Resource):
    def get(self):
     
        sections = Section.query.all()
        
        section_list = [{'id': section.id, 'name': section.name} for section in sections]
        return jsonify(section_list)    
    


api.add_resource(Search, '/search') 
api.add_resource(AddSections, '/add_section')
api.add_resource(DeleteSection,'/delete_section/<int:section_id>')
api.add_resource(UpdateSection,'/update_section/<int:section_id>')
api.add_resource(getSection, '/sections')



####################BOOKS#########################
 

class FileUpload(Resource):
    def post(self, book_id):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=FileStorage, location='files', required=True)
        args = parser.parse_args()

        file = args['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Retrieve the book object
            book = Book.query.get(book_id)
            if book:
                # Update the book object with the file path
                book.file_path = file_path
                db.session.commit()
                
                return {'message': 'File uploaded successfully', 'file_path': file_path}, 201
            else:
                return {'message': 'Book not found'}, 404
        else:
            return {'message': 'Invalid file format'}, 400


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'epub' ,'mp3'}


class AddBook(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('section_id', type=int, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('authors', type=str, required=True)
        parser.add_argument('content', type=str, required=True)
        parser.add_argument('file_path',type=str)

        args = parser.parse_args()

        new_book = Book(
            name=args['name'],
            content=args['content'],
            authors=args['authors'],
            section_id=args['section_id'],
            file_path = args['file_path']
            
        )

        db.session.add(new_book)
        db.session.commit()

        return {'message': 'Book added successfully', 'book_id': new_book.id}, 201
class BooksBySection(Resource):
    
    def get(self, section_id):
        search_query = request.args.get('q', '')
        section = Section.query.get_or_404(section_id)
        
        books = Book.query.filter_by(section_id=section_id).filter(
            or_(Book.name.ilike(f"%{search_query}%"), Book.authors.ilike(f"%{search_query}%"))
        ).all()
        
        book_data = []
        for book in books:
            book_info = {
                'id': book.id,
                'name': book.name,
                'content': book.content,
                'authors': book.authors,
                'file_path': book.file_path,
                'section_id': book.section_id,
                'section_name': section.name
            }
            book_data.append(book_info)
    
        return {'section': {'id': section.id, 'name': section.name}, 'books': book_data}, 200
  
class GetBooks(Resource):
    def get(self):
        search_query = request.args.get('q', '')
        
        
        books = Book.query.filter(
            or_(Book.name.ilike(f"%{search_query}%"), Book.authors.ilike(f"%{search_query}%"))
        ).all()
        
        book_data = []
        for book in books:
          
            section_name = book.section.name if book.section else None
            
            book_info = {
                'book_id':book.id,
                'name': book.name,
                'content': book.content,
                'authors': book.authors,
                'file_path': book.file_path,
                'section_name': section_name
            }
            book_data.append(book_info)
    
        return {'books': book_data}, 200

  
class DeleteBook(Resource):
    def delete(self, book_id):
        book = Book.query.get(book_id)
        if book is None:
            return {'message': 'Book not found'}, 404

     
        db.session.delete(book)
        db.session.commit()

        return {'message': 'Book deleted successfully'}, 200

class UpdateBook(Resource):
    def put(self, book_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('content', type=str)
        parser.add_argument('authors', type=str)
        parser.add_argument('section_id', type=int)
        parser.add_argument('file_path', type=str)
        args = parser.parse_args()

        book = Book.query.get(book_id)
        if book is None:
            return {'message': 'Book not found'}, 404

        if args['name']:
            book.name = args['name']
        if args['content']:
            book.content = args['content']
        if args['authors']:
            book.authors = args['authors']
        if args['section_id']:
            book.section_id = args['section_id']
        if args['file_path']:
            book.file_path = args['file_path']

        db.session.commit()
        return {'message': 'Book updated successfully'}, 200
    


class RateBook(Resource):
    def post(self, book_id):
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=float, required=True)
        args = parser.parse_args()

        book = Book.query.get_or_404(book_id)
        book.rating = args['rating']
        db.session.commit()

        return {'message': 'Book rated successfully'}, 200
    
class GetSectionsWithBooks(Resource):
    
    def get(self):
        sections = Section.query.all()
        sections_with_books = []
        for section in sections:
            section_data = {
                'id': section.id,
                'name': section.name,
                'description': section.description,
                'date_created': section.date_created.isoformat() if section.date_created else None,
                'books': [
                    {
                        'id': book.id,
                        'name': book.name,
                        'content': book.content,
                        'authors': book.authors,
                        'file_path': book.file_path,
                        'section_id': book.section_id,
                        'section_name': section.name
                    } for book in section.books
                ]
            }
            sections_with_books.append(section_data)
    
        return {'sections': sections_with_books}, 200

api.add_resource(GetSectionsWithBooks, '/get_sections_with_books')    

class CommentBook(Resource):
    def post(self, book_id):
        parser = reqparse.RequestParser()
        parser.add_argument('comment', type=str, required=True)
        args = parser.parse_args()

        new_comment = Comment(book_id=book_id, text=args['comment'])
        db.session.add(new_comment)
        db.session.commit()

        return {'message': 'Comment added successfully'}, 201

api.add_resource(AddBook, '/add_book')
api.add_resource(FileUpload, '/upload_file/<int:book_id>')
api.add_resource(BooksBySection, '/get_books/<int:section_id>')
#api.add_resource(SectionBooks,'/getsectionwithbooks')
api.add_resource(RateBook, '/rate_book/<int:book_id>')
api.add_resource(CommentBook, '/comment_book/<int:book_id>')
api.add_resource(DeleteBook,'/delete_book/<int:book_id>')
api.add_resource(UpdateBook, '/update_book/<int:book_id>')
api.add_resource(GetBooks,'/getbooks')
  
################################Count##########################


class Count(Resource):
    def get(self):
        user_count = User.query.count()
        section_count = Section.query.count()  # Corrected typo in "count()"
        book_count = Book.query.count()
        requests_count=Rental.query.count()
        
        return {'users': user_count,
                'sections': section_count,  
                'books': book_count,
                'requests': requests_count
               }

api.add_resource(Count, '/count')

######################USER access#################################

class DisplayRental(Resource):
    def get(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument('book_id')


class RequestBook(Resource):
    def __init__(self):
        super(RequestBook, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('book_id', type=int, required=True, help='No book ID provided')
        self.reqparse.add_argument('user_id', type=int, required=True, help='No user ID provided')

    def post(self):
        args = self.reqparse.parse_args()
        book_id = args['book_id']
        user_id = args['user_id']

        bookscount = Rental.query.filter_by(borrower_id=user_id, returned=False).count()

        if bookscount >= 5:
            return {'message': 'You have reached the maximum limit of checked out books.'}, 403

        new_rental = Rental(
            book_id=book_id,
            borrower_id=user_id,
        )
        db.session.add(new_rental)
        db.session.commit()
        return {'message': 'Your request has been submitted for approval.','rental_id': new_rental.id}, 201



class Approve(Resource):
    def get(self):

        pending_requests = Rental.query.filter_by(approved=False).all()

        return [{'book_id': req.book_id, 'borrower_id': req.borrower_id} for req in pending_requests]

    def put(self, rental_id):
       
        rental_request = Rental.query.get(rental_id)
        if not rental_request:
            return {'message': 'Rental request not found'}, 404

        if rental_request.approved:
            return {'message': 'Rental request is already approved'}, 400

     
        rental_request.approved = True
        rental_request.approval_time = datetime.utcnow()
        rental_request.access_duration = 5 

        db.session.commit()

       
        return {'message': 'Rental request approved for 5 minutes', 'rental_id': rental_request.id,'book_id': rental_request.book_id}, 200

    
class RentalResource(Resource):
    def get(self):
        rentals = Rental.query.all()
        rental_list = [{'id': rental.id, 'book_id': rental.book_id, 'borrower_id': rental.borrower_id, 'date_issued': rental.date_issued.isoformat(), 'return_date': rental.return_date.isoformat() if rental.return_date else None, 'returned': rental.returned, 'approved': rental.approved, 'access_duration': rental.access_duration, 'approval_time': rental.approval_time.isoformat() if rental.approval_time else None, 'book_count': rental.book_count} for rental in rentals]
        return jsonify(rental_list)
    
class DeleteRental(Resource):
    def delete(self, rental_id):
        rental = Rental.query.get(rental_id)
        if not rental:
            return {'message': 'Rental not found'}, 404

        db.session.delete(rental)
        db.session.commit()
        
        return {'message': 'Rental request deleted successfully'}, 200




class Revoke(Resource):
    def put(self, rental_id):
        rental_request = Rental.query.get(rental_id)
        if not rental_request:
            return {'message': 'Rental request not found'}, 404

        rental_request.approved = False
        rental_request.returned = True
        rental_request.return_date = datetime.utcnow()
        db.session.commit()

        return {'message': 'Access revoked for the e-book'}, 200
    
class ReadBook(Resource):
    def get(self, rental_id):
        
        rental = Rental.query.get(rental_id)
        if not rental:
            return {'message': 'Rental request not found'}, 404

        
        if not rental.approved:
            return {'message': 'Rental request is not approved'}, 403

        
        book = Book.query.get(rental.book_id)
        if not book:
            return {'message': 'Book not found'}, 404

        file_path = book.file_path
        if not file_path:
            return {'message': 'File path not provided for the book'}, 404

      
        if not os.path.exists(file_path):
            return {'message': 'File not found'}, 404

       
        file_extension = os.path.splitext(file_path)[1].lower()

        
        if file_extension not in ['.pdf', '.epub']:
            return {'message': 'Unsupported file format'}, 400

       
        return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path))
    


class BookDetails(Resource):
    def get(self, rental_id):
        rental = Rental.query.get(rental_id)
        if rental and rental.approved:
            book = Book.query.get(rental.book_id)
            if book:
                book_details = {
                    'name': book.name,
                    'content': book.content,
                    'file_path': book.file_path
                }
                return jsonify(book_details)
        return jsonify({'error': 'Rental not approved yet'})
    

class UserBooks(Resource):
    def get(self):
        data = request.get_json()  
        user_id = data.get('user_id')  
        if not user_id:
            return {'error': 'User ID is required'}, 400

        books = db.session.query(Book).options(joinedload(Book.rentals)).all()

        books_data = []
        for book in books:
            rental_status = 'Not Requested'
            rental_id = None
        
            for rental in book.rentals:
                if rental.borrower_id == user_id:
                    if rental.approved:
                        rental_status = 'Approved'
                    else:
                        rental_status = 'Requested'
                    rental_id = rental.id
                    break
            
            books_data.append({
                'id': book.id,
                'name': book.name,
                'authors': book.authors,
                'status': rental_status,
                'rental_id': rental_id,
            })

        return {'books': books_data}, 200
    
class Filesend(Resource):
    def get(self, filename):
        
        file_extension = filename.split('.')[-1]
        if file_extension.lower() in ['pdf', 'epub', 'mp3']:
            return send_from_directory('uploads', filename)
        else:
            return {"message": "Unsupported file format"}, 400

api.add_resource(Filesend, '/uploads/<path:filename>')


    
api.add_resource(UserBooks, '/books')    
api.add_resource(BookDetails, '/bookdetails/<int:rental_id>')
api.add_resource(ReadBook, '/read_book/<int:rental_id>')    
api.add_resource(DeleteRental, '/delete_rental/<int:rental_id>')    
api.add_resource(RentalResource, '/rentals')
api.add_resource(Revoke, '/revoke_access/<int:rental_id>')    
api.add_resource(Approve, '/approve', '/approve/<int:rental_id>')
api.add_resource(RequestBook, '/requestbook')    