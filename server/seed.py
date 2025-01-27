#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Room, Amenity

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():  # Ensure the app context is available
        print("Starting seed...")

        # Clear out the existing data (optional, if you want to start fresh)
        db.drop_all()
        db.create_all()

        # Seed Users
        for _ in range(100): 
            user = User(
                username=fake.user_name(),
                email=fake.email(),
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
        for _ in range(10): 
            amenity = Amenity(
                name=fake.word(),
                type=rc(['Pool', 'Gym', 'Spa', 'Parking', 'Wi-Fi']),
                charges=round(randint(10, 100) + randint(0, 99) / 100, 2),
                user_id=rc([user.id for user in User.query.all()]),  
            )
            db.session.add(amenity)

        db.session.commit()

        print("Seed completed!")
