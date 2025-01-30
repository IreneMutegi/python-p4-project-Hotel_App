from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User, Room, Amenity, UserRoomBooking, UserAmenityBooking  # Your models

app = Flask(__name__)
CORS(app, origins="http://localhost:3000", supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.json.compact = False 

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Home Route 
class Home(Resource):
    def get(self):
        response_dict = {"message": "Welcome to the Booking API"}
        response = make_response(response_dict, 200)
        return response

api.add_resource(Home, '/')  

# Users Resource 
class Users(Resource):
    @cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
    def post(self):
        
        data = request.get_json()  # Assuming the request sends JSON
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()

        response_dict = new_user.to_dict()
        response = make_response(response_dict, 201)
        return response

api.add_resource(Users, '/users')  

# User by ID Resource 
class UserByID(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            response_dict = user.to_dict()
            response = make_response(response_dict, 200)
        else:
            response = make_response({"message": "User not found"}, 404)
        return response

api.add_resource(UserByID, '/users/<int:user_id>') 

# Rooms Resource 
class Rooms(Resource):
    def get(self):
        response_dict_list = [room.to_dict() for room in Room.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        data = request.get_json()
        new_room = Room(name=data['name'], type=data['type'], price=data['price'], user_id=data['user_id'])
        db.session.add(new_room)
        db.session.commit()

        response_dict = new_room.to_dict()
        response = make_response(response_dict, 201)
        return response

api.add_resource(Rooms, '/rooms')  

# Room by ID Resource
class RoomByID(Resource):
    def get(self, room_id):
        room = Room.query.get(room_id)
        if room:
            response_dict = room.to_dict()
            response = make_response(response_dict, 200)
        else:
            response = make_response({"message": "Room not found"}, 404)
        return response

api.add_resource(RoomByID, '/rooms/<int:room_id>')

# Amenity Resource 
class Amenities(Resource):
    def get(self):
        response_dict_list = [amenity.to_dict() for amenity in Amenity.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        data = request.get_json()
        new_amenity = Amenity(name=data['name'], type=data['type'], charges=data['charges'], user_id=data['user_id'])
        db.session.add(new_amenity)
        db.session.commit()

        response_dict = new_amenity.to_dict()
        response = make_response(response_dict, 201)
        return response

api.add_resource(Amenities, '/amenities')  # Create and get all amenities

# Amenity by ID Resource (for handling specific amenity by ID)
class AmenityByID(Resource):
    def get(self, amenity_id):
        amenity = Amenity.query.get(amenity_id)
        if amenity:
            response_dict = amenity.to_dict()
            response = make_response(response_dict, 200)
        else:
            response = make_response({"message": "Amenity not found"}, 404)
        return response

api.add_resource(AmenityByID, '/amenities/<int:amenity_id>')  # Get amenity by ID

# User Room Booking Resource (for handling room bookings by users)
class UserRoomBookings(Resource):
    def get(self):
        response_dict_list = [booking.to_dict() for booking in UserRoomBooking.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        data = request.get_json()
        new_booking = UserRoomBooking(
            user_id=data['user_id'],
            room_id=data['room_id'],
            check_in_date=data['check_in_date'],
            check_out_date=data['check_out_date']
        )
        db.session.add(new_booking)
        db.session.commit()

        response_dict = new_booking.to_dict()
        response = make_response(response_dict, 201)
        return response

api.add_resource(UserRoomBookings, '/user_room_bookings')  # Create and get all room bookings

# User Amenity Booking Resource (for handling amenity bookings by users)
class UserAmenityBookings(Resource):
    def get(self):
        response_dict_list = [booking.to_dict() for booking in UserAmenityBooking.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        data = request.get_json()
        if 'user_id' not in data or 'amenity_id' not in data or 'booking_time' not in data:
            return {"error": "User ID, Amenity ID, and Booking Time are required"}, 400

        new_booking = UserAmenityBooking(user_id=data['user_id'], amenity_id=data['amenity_id'], booking_time=data['booking_time'])
        db.session.add(new_booking)
        db.session.commit()

        response_dict = new_booking.to_dict()
        response = make_response(response_dict, 201)
        return response

    def delete(self, booking_id):
        booking = UserAmenityBooking.query.get(booking_id)
        if booking:
            db.session.delete(booking)
            db.session.commit()
            return {"message": "Booking deleted successfully"}, 200
        return {"error": "Booking not found"}, 404

api.add_resource(AmenityBookings, '/amenity_bookings', '/amenity_bookings/<int:booking_id>')

# All room bookings
class RoomBookings(Resource):
    def get(self):
        bookings = [booking.to_dict() for booking in UserRoomBooking.query.all()]
        response = make_response(bookings, 200)
        return response

    def delete(self, booking_id):
        booking = UserRoomBooking.query.get(booking_id)
        if booking:
            db.session.delete(booking)
            db.session.commit()
            return {"message": "Booking deleted successfully"}, 200
        return {"error": "Booking not found"}, 404

api.add_resource(RoomBookings, '/room_bookings', '/room_bookings/<int:booking_id>')

# Clients that have accessed a particular room
class RoomClients(Resource):
    def get(self, room_id):
        bookings = UserRoomBooking.query.filter_by(room_id=room_id).all()
        users = [booking.user.to_dict() for booking in bookings]
        response = make_response(users, 200)
        return response

api.add_resource(RoomClients, '/rooms/<int:room_id>/clients')

# Clients that have booked a particular amenity
class AmenityClients(Resource):
    def get(self, amenity_id):
        bookings = UserAmenityBooking.query.filter_by(amenity_id=amenity_id).all()
        users = [booking.user.to_dict() for booking in bookings]
        response = make_response(users, 200)
        return response

api.add_resource(AmenityClients, '/amenities/<int:amenity_id>/clients')

# User-specific bookings
class UserBookings(Resource):
    def get(self):
        user_email = request.args.get('clientEmail')
        if user_email:
            user = User.query.filter_by(email=user_email).first()
            if user:
                room_bookings = UserRoomBooking.query.filter_by(user_id=user.id).all()
                amenity_bookings = UserAmenityBooking.query.filter_by(user_id=user.id).all()
                all_bookings = []
                for booking in room_bookings:
                    all_bookings.append(booking.to_dict())
                for booking in amenity_bookings:
                    all_bookings.append(booking.to_dict())
                response = make_response(all_bookings, 200)
                return response
            return make_response({"message": "User not found"}, 404)
        return make_response({"message": "Client email is required"}, 400)

api.add_resource(UserBookings, '/bookings')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
