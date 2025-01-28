from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User, Room, Amenity, UserRoomBooking, UserAmenityBooking  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.json.compact = False 

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


# Home Route (Root of the API)
class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Booking API",
        }
        response = make_response(response_dict, 200)
        return response

api.add_resource(Home, '/')  


# Users Resource (for handling users)
class Users(Resource):
    def get(self):
        response_dict_list = [user.to_dict() for user in User.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        data = request.get_json()

        if 'username' not in data or 'email' not in data or 'password' not in data:
            return {"error": "Username, email, and password are required"}, 400

        user_type_id = data.get('user_type_id', 1)

        # Create a new user and hash the password
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],  
            user_type_id=user_type_id
        )
        new_user.set_password(data['password'])  

        db.session.add(new_user)
        db.session.commit()

        response_dict = new_user.to_dict()
        response = make_response(response_dict, 201)
        return response

api.add_resource(Users, '/users')  


# User by ID Resource (Get a specific user by ID)
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


# Rooms Resource (for handling rooms)
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


# Amenity Resource (for handling amenities)
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

api.add_resource(Amenities, '/amenities')  


# User Amenity Booking Resource (for handling amenity bookings by users)
class UserAmenityBookings(Resource):
    def get(self):
        response_dict_list = [booking.to_dict() for booking in UserAmenityBooking.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        data = request.get_json()

        # Validate required fields
        if 'user_id' not in data or 'amenity_id' not in data or 'booking_time' not in data:
            return {"error": "User ID, Amenity ID, and Booking Time are required"}, 400

        # Create a new amenity booking
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
