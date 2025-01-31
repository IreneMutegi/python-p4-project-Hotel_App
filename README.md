Hotel Booking API
This is a RESTful API built with Flask that allows for the management of hotel room bookings and amenity reservations. It provides functionality for managing users, rooms, amenities, bookings, and handling user-specific data, such as their bookings for rooms and amenities.

Features
User Management: Create, retrieve, and delete users.
Room Management: Add new rooms, retrieve all rooms.
Amenity Management: Add new amenities, retrieve all amenities.
Bookings: Create and manage bookings for both rooms and amenities.
User-specific Bookings: Retrieve all bookings for a specific user, including room and amenity bookings.
CORS Support: API supports cross-origin requests for development with a React frontend (configured for http://localhost:3000).
Technologies Used
Flask: Web framework for building the API.
Flask-SQLAlchemy: ORM for database management.
Flask-Migrate: Database migration tool for managing schema changes.
Flask-RESTful: For creating REST APIs.
Flask-CORS: To enable cross-origin resource sharing.
SQLite: Database used for storing user, room, amenity, and booking data.
Setup
Clone the Repository

bash
Copy
Edit
git clone <repository-url>
cd <project-directory>
Install Dependencies You can create a virtual environment and install the necessary dependencies using:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
pip install -r requirements.txt
Configure the Database The database used is SQLite. You can configure the database URI by updating the SQLALCHEMY_DATABASE_URI in app.config if necessary. To create the initial database and tables, run:

bash
Copy
Edit
flask db init
flask db migrate
flask db upgrade
Run the Application To run the application locally:

bash
Copy
Edit
flask run
The API will be available at http://localhost:5000.

Endpoints
1. Users
GET /users: Retrieves a list of all users.

POST /users: Creates a new user. Requires username, email, and password.

GET /users/int:user_id: Retrieves a specific user by ID.

DELETE /users/int:user_id: Deletes a specific user by ID.

2. Rooms
GET /rooms: Retrieves a list of all rooms.
POST /rooms: Adds a new room. Requires room data like name, description, and price.
3. Amenities
GET /amenities: Retrieves a list of all amenities.
POST /amenities: Adds a new amenity. Requires amenity data like name, description, and cost.
4. Bookings
GET /user_room_bookings: Retrieves all room bookings.

POST /user_room_bookings: Creates a new room booking. Requires user data and booking details.

GET /user_amenity_bookings: Retrieves all amenity bookings. Requires clientEmail query parameter to filter bookings by user.

POST /user_amenity_bookings: Creates a new amenity booking. Requires username, email, amenity_name, booking_date, and booking_time.

5. Room Users
GET /rooms/int:room_id/users: Retrieves all users who have booked a specific room.
6. Amenity Users
GET /amenities/int:amenity_id/users: Retrieves all users who have booked a specific amenity.
7. User Bookings
GET /bookings: Retrieves all bookings (room and amenity).
GET /bookings?clientEmail=<email>: Retrieves bookings for a specific user based on their email.
POST /bookings: Creates a new booking (either room or amenity). Requires username, email, bookingDate, and bookingTime. Optionally, roomId or amenityId for the type of booking.
DELETE /bookings/int:booking_id: Deletes a booking by ID.
CORS Configuration
The API allows requests from http://localhost:3000 (default React development server) to enable communication with a React frontend. To adjust this configuration, modify the CORS setup in the code.
