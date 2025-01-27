from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User, Room, Amenity, UserRoomBooking, UserAmenityBooking  # Your models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.json.compact = False 

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Booking API",
        }
        response = make_response(response_dict, 200)
        return response

api.add_resource(Home, '/')  # Home route


class Users(Resource):
    def get(self):

        response_dict_list = [user.to_dict() for user in User.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        
        data = request.get_json()  # Assuming the request sends JSON
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()

        response_dict = new_user.to_dict()
        response = make_response(response_dict, 201)
        return response

api.add_resource(Users, '/users')  # Create and get all users


class UserByID(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            response_dict = user.to_dict()
            response = make_response(response_dict, 200)
        else:
            response = make_response({"message": "User not found"}, 404)
        return response

api.add_resource(UserByID, '/users/<int:user_id>')  # Get a user by ID


class Rooms(Resource):
    def get(self):
        response_dict_list = [room.to_dict() for room in Room.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        data = request.get_json()
        new_room = Room(name=data['name'], type=data['type'], price=data['price'])
        db.session.add(new_room)
        db.session.commit()

        response_dict = new_room.to_dict()
        response = make_response(response_dict, 201)
        return response

api.add_resource(Rooms, '/rooms')  # Create and get all rooms

# Room by ID Resource (for handling specific room by ID)
class RoomByID(Resource):
    def get(self, room_id):
        room = Room.query.get(room_id)
        if room:
            response_dict = room.to_dict()
            response = make_response(response_dict, 200)
        else:
            response = make_response({"message": "Room not found"}, 404)
        return response

api.add_resource(RoomByID, '/rooms/<int:room_id>')  # Get a room by ID

# Amenity Resource (for handling amenities)
class Amenities(Resource):
    def get(self):
        response_dict_list = [amenity.to_dict() for amenity in Amenity.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        data = request.get_json()
        new_amenity = Amenity(name=data['name'], type=data['type'], charges=data['charges'])
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
        new_booking = UserAmenityBooking(
            user_id=data['user_id'],
            amenity_id=data['amenity_id'],
            booking_time=data['booking_time']
        )
        db.session.add(new_booking)
        db.session.commit()

        response_dict = new_booking.to_dict()
        response = make_response(response_dict, 201)
        return response

api.add_resource(UserAmenityBookings, '/user_amenity_bookings')  # Create and get all amenity bookings

if __name__ == '__main__':
    app.run(port=5555, debug=True)
