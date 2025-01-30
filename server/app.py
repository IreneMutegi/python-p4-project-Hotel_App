from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS  # Import CORS
from models import db, User, Room, Amenity, UserRoomBooking, UserAmenityBooking

app = Flask(__name__)

# Configure CORS to allow requests from React frontend
CORS(app, origins="http://localhost:3000", supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.json.compact = False 

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        return {"message": "Welcome to the Booking API"}, 200

api.add_resource(Home, '/')  

class Users(Resource):
    def get(self):
        return [user.to_dict() for user in User.query.all()], 200

    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201

api.add_resource(Users, '/users')  
# class Login(Resource):
#     def post(self):
#         data = request.get_json()

#         # Check if email exists in the database
#         user = User.query.filter_by(email=data['email']).first()
#         if not user:
#             return {"error": "Email not found"}, 404

#         # Check if the password matches
#         if not user.check_password(data['password']):
#             return {"error": "Invalid password"}, 401

#         return {"message": "Login successful", "user": user.to_dict()}, 200

# api.add_resource(Login, '/login')

class UserByID(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user.to_dict(), 200
        return {"message": "User not found"}, 404

api.add_resource(UserByID, '/users/<int:user_id>') 

class Rooms(Resource):
    def get(self):
        return [room.to_dict() for room in Room.query.all()], 200
    
    def post(self):
        data = request.get_json()
        new_room = Room(**data)
        db.session.add(new_room)
        db.session.commit()
        return new_room.to_dict(), 201

api.add_resource(Rooms, '/rooms')  

class Amenities(Resource):
    def get(self):
        return [amenity.to_dict() for amenity in Amenity.query.all()], 200
    
    def post(self):
        data = request.get_json()
        new_amenity = Amenity(**data)
        db.session.add(new_amenity)
        db.session.commit()
        return new_amenity.to_dict(), 201

api.add_resource(Amenities, '/amenities')

class UserRoomBookings(Resource):
    def get(self):
        return [booking.to_dict() for booking in UserRoomBooking.query.all()], 200
    
    def post(self):
        data = request.get_json()
        new_booking = UserRoomBooking(**data)
        db.session.add(new_booking)
        db.session.commit()
        return new_booking.to_dict(), 201

api.add_resource(UserRoomBookings, '/user_room_bookings')

class UserAmenityBookings(Resource):
    def get(self):
        return [booking.to_dict() for booking in UserAmenityBooking.query.all()], 200
    
    def post(self):
        data = request.get_json()
        if not all(k in data for k in ['user_id', 'amenity_id', 'booking_time']):
            return {"error": "User ID, Amenity ID, and Booking Time are required"}, 400
        new_booking = UserAmenityBooking(**data)
        db.session.add(new_booking)
        db.session.commit()
        return new_booking.to_dict(), 201
    
    def delete(self, booking_id):
        booking = UserAmenityBooking.query.get(booking_id)
        if booking:
            db.session.delete(booking)
            db.session.commit()
            return {"message": "Booking deleted successfully"}, 200
        return {"error": "Booking not found"}, 404

api.add_resource(UserAmenityBookings, '/amenity_bookings', '/amenity_bookings/<int:booking_id>')

class UserBookings(Resource):
    def get(self):
        user_email = request.args.get('clientEmail')
        if user_email:
            user = User.query.filter_by(email=user_email).first()
            if user:
                room_bookings = [b.to_dict() for b in UserRoomBooking.query.filter_by(user_id=user.id).all()]
                amenity_bookings = [b.to_dict() for b in UserAmenityBooking.query.filter_by(user_id=user.id).all()]
                return room_bookings + amenity_bookings, 200
            return {"message": "User not found"}, 404
        return {"message": "Client email is required"}, 400

api.add_resource(UserBookings, '/bookings')

class RoomUsers(Resource):
    def get(self, room_id):
        bookings = UserRoomBooking.query.filter_by(room_id=room_id).all()
        users = [booking.user.to_dict() for booking in bookings]
        return users, 200

api.add_resource(RoomUsers, '/rooms/<int:room_id>/users')

class AmenityUsers(Resource):
    def get(self, amenity_id):
        bookings = UserAmenityBooking.query.filter_by(amenity_id=amenity_id).all()
        users = [booking.user.to_dict() for booking in bookings]
        return users, 200

api.add_resource(AmenityUsers, '/amenities/<int:amenity_id>/users')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
