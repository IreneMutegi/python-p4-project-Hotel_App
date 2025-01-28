import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import pool from "../assets/images/outdoorpool.jpeg";  // Example image
import spa from "../assets/images/spaservice.jpeg";   // Example image
import gym from "../assets/images/fitness.jpeg";     // Example image
import canoeing from "../assets/images/canoeing.jpeg"; // Example image
import finedining from "../assets/images/finedining.jpeg"; // Example image
import './Amenities.css'; 

const amenitiesData = [
  {
    emoji: '🌐',
    title: 'Free Wi-Fi',
    description: 'Enjoy high-speed internet access throughout the hotel for all your work and entertainment needs.',
    image: null,
    buttonText: 'Access Now',
    password: 'WiFi1234',
  },
  {
    emoji: '🏊‍♂️',
    title: 'Outdoor Pool',
    description: 'Relax by our outdoor pool, offering a perfect spot for a refreshing swim and sunbathing.',
    image: pool,
    buttonText: 'Book Now',
  },
  {
    emoji: '🍽',
    title: 'Fine Dining Restaurant',
    description: 'Indulge in gourmet dishes prepared by world-class chefs in a luxurious dining setting.',
    image: finedining,
    buttonText: 'Book Now',
  },
  {
    emoji: '💆',
    title: 'Spa Services',
    description: 'Relax and rejuvenate with our variety of spa treatments designed to provide ultimate relaxation.',
    image: spa,
    buttonText: 'Book Now',
  },
  {
    emoji: '🏋️‍♀️',
    title: 'Fitness Center',
    description: 'Stay fit and healthy in our fully equipped fitness center, featuring the latest workout equipment.',
    image: gym,
    buttonText: 'Book Now',
  },
  {
    emoji: '🚣‍♀️',
    title: 'Canoeing',
    description: 'Explore the waters with our exciting canoeing experience.',
    image: canoeing,
    buttonText: 'Book Now',
  },
];

const Amenities = ({ setBookingInfo, userInfo }) => {
  const [selectedAmenity, setSelectedAmenity] = useState(null);
  const [bookingDate, setBookingDate] = useState("");
  const [bookingTime, setBookingTime] = useState("");
  const [clientName, setClientName] = useState(userInfo?.name || ""); // Prefill name from userInfo
  const [clientEmail, setClientEmail] = useState(userInfo?.email || ""); // Prefill email from userInfo
  const [wifiPassword, setWifiPassword] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Update clientName and clientEmail when userInfo changes
  useEffect(() => {
    if (userInfo) {
      setClientName(userInfo.name);
      setClientEmail(userInfo.email);
    }
  }, [userInfo]);

  const handleBookingClick = (amenity) => {
    setSelectedAmenity(amenity);
    setError(""); // Reset error message
  };

  const handleAccessNowClick = () => {
    setWifiPassword('WiFi1234');
  };

  const handleBookingSubmit = async (e) => {
    e.preventDefault();

    if (selectedAmenity && bookingDate && bookingTime && clientName && clientEmail) {
      const bookingDetails = {
        amenity: selectedAmenity.title,
        bookingDate,
        bookingTime,
        clientName,
        clientEmail,
      };

      // POST request to save booking details
      try {
        const response = await fetch("https://hotel-app-75bj.onrender.com/bookings", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(bookingDetails),
        });

        if (!response.ok) {
          setError("Failed to submit booking");
        } else {
          const data = await response.json();  // Assuming the API sends back the saved data
          setBookingInfo(data); // Pass the saved data to the parent component (if needed)
          alert(`Booking confirmed for ${selectedAmenity.title} on ${bookingDate} at ${bookingTime}`);
          navigate("/profile");
        }
      } catch (error) {
        setError("Error submitting booking");
      }
    } else {
      setError("Please fill all fields and select an amenity.");
    }
  };

  return (
    <div className="amenities-container">
      <h2>Our Amenities</h2>
      <div className="amenities-list">
        {amenitiesData.map((amenity, index) => (
          <div key={index} className="amenity">
            <div className="amenity-header">
              <span className="emoji">{amenity.emoji}</span>
              <h3>{amenity.title}</h3>
            </div>
            {amenity.image && <img src={amenity.image} alt={amenity.title} className="amenity-image" />}
            <div className="amenity-content">
              <p className="amenity-description">{amenity.description}</p>
              <div className="button-container">
                {amenity.title === 'Free Wi-Fi' ? (
                  <button 
                    className="book-now-btn" 
                    onClick={handleAccessNowClick}
                  >
                    {amenity.buttonText}
                  </button>
                ) : (
                  <button 
                    className="book-now-btn" 
                    onClick={() => handleBookingClick(amenity)}
                  >
                    {amenity.buttonText}
                  </button>
                )}
                {wifiPassword && amenity.title === 'Free Wi-Fi' && (
                  <div className="wifi-password">
                    <p><strong> Wi-Fi Password:</strong> {wifiPassword}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
      {selectedAmenity && (
        <div className="booking-form">
          <h3>Booking {selectedAmenity.title}</h3>
          <form onSubmit={handleBookingSubmit}>
            <label>
              Client Name:
              <input 
                type="text" 
                value={clientName} 
                onChange={(e) => setClientName(e.target.value)} 
                required 
              />
            </label>
            <label>
              Client Email:
              <input 
                type="email" 
                value={clientEmail} 
                onChange={(e) => setClientEmail(e.target.value)} 
                required 
              />
            </label>
            <label>
              Select Date:
              <input 
                type="date" 
                value={bookingDate} 
                onChange={(e) => setBookingDate(e.target.value)} 
                required 
              />
            </label>
            <label>
              Select Time:
              <input 
                type="time" 
                value={bookingTime} 
                onChange={(e) => setBookingTime(e.target.value)} 
                required 
              />
            </label>
            <button type="submit" className="confirm-booking-btn">Confirm Booking</button>
            {error && <p className="error-message">{error}</p>}
          </form>
        </div>
      )}
    </div>
  );
};

export default Amenities;