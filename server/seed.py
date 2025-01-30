#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc
from faker import Faker

# Remote library imports
from app import app
from models import db, User, Room, Amenity, UserType

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():  # Ensure the app context is available
        print("Starting seed...")

        # Clear out the existing data
        db.drop_all()
        db.create_all()

        # Seed UserTypes
        # Seeding UserType data
        admin_type = UserType(type="Admin")
        client_type = UserType(type="Client")

        db.session.add_all([admin_type, client_type])
        db.session.commit()

        # Seed Users
        for _ in range(100):
            password = fake.password()  # Generate a random password
            user_type = rc([admin_type, client_type])  # Randomly choose between Admin and Client types

            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password=password,  # Store plain password (consider hashing in a real application)
                user_type_id=user_type.id  # Set the foreign key reference
            )
            db.session.add(user)

        db.session.commit()

        # Seed Rooms
        for _ in range(100):  
            room = Room(
                name=fake.word(),
                type=rc(['Single', 'Double', 'Suite']),
                price=round(randint(100, 500) + randint(0, 99) / 100, 2),
                user_id=rc([user.id for user in User.query.all()]),  # Assign room to a random user
            )
            db.session.add(room)

        db.session.commit()

        # Seed Amenities
        amenities_data = [
            {'name': 'Wi-Fi', 'type': 'Wi-Fi', 'charges': 0},
            {'name': 'Outdoor Pool', 'type': 'Pool', 'charges': round(randint(10, 50) + randint(0, 99) / 100, 2)},
            {'name': 'Fine Dining Restaurant', 'type': 'Restaurant', 'charges': round(randint(30, 150) + randint(0, 99) / 100, 2)},
            {'name': 'Spa Services', 'type': 'Spa', 'charges': round(randint(50, 200) + randint(0, 99) / 100, 2)},
            {'name': 'Fitness Center', 'type': 'Gym', 'charges': round(randint(15, 75) + randint(0, 99) / 100, 2)},
            {'name': 'Canoeing', 'type': 'Water Sports', 'charges': round(randint(20, 100) + randint(0, 99) / 100, 2)}
        ]

        for amenity in amenities_data:
            amenity_instance = Amenity(
                name=amenity['name'],
                type=amenity['type'],
                charges=amenity['charges'],
                user_id=rc([user.id for user in User.query.all()])  # Assign to random user
            )
            db.session.add(amenity_instance)

        db.session.commit()

        print("Seed completed!")
