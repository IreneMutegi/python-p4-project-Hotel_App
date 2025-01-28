import React, { useState, useEffect } from "react";
import './Profile.css';

function Profile() {
  const [user, setUser] = useState(null);
  const [bookings, setBookings] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [editingBooking, setEditingBooking] = useState(null);
  const [updatedBooking, setUpdatedBooking] = useState({ bookingDate: "", bookingTime: "" });

  useEffect(() => {
    // Retrieve user details from localStorage
    const userName = localStorage.getItem("clientName");
    const userEmail = localStorage.getItem("clientUsername");

    if (userName && userEmail) {
      // Set user details
      setUser({ name: userName, email: userEmail });

      // Fetch bookings related to this user
      fetch(`https://hotel-app-75bj.onrender.com/bookings?clientEmail=${userEmail}`)
        .then((response) => response.json())
        .then((data) => {
          setBookings(data);
        })
        .catch((error) => {
          console.error("Error fetching bookings:", error);
          setErrorMessage("An error occurred while fetching bookings.");
        });
    } else {
      setErrorMessage("No user logged in.");
    }
  }, []);

  const handleEdit = (booking) => {
    setEditingBooking(booking);
    setUpdatedBooking({
      bookingDate: booking.bookingDate,
      bookingTime: booking.bookingTime,
    });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUpdatedBooking((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSaveEdit = (id) => {
    fetch(`https://hotel-app-75bj.onrender.com/bookings/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedBooking),
    })
      .then((response) => response.json())
      .then((data) => {
        setBookings((prevBookings) =>
          prevBookings.map((booking) =>
            booking.id === id ? { ...booking, ...updatedBooking } : booking
          )
        );
        setEditingBooking(null); // Close the edit form
      })
      .catch((error) => {
        console.error("Error saving edited booking:", error);
        setErrorMessage("An error occurred while saving the booking.");
      });
  };

  const handleDelete = (id) => {
    fetch(`https://hotel-app-75bj.onrender.com/bookings/${id}`, {
      method: "DELETE",
    })
      .then(() => {
        setBookings((prevBookings) =>
          prevBookings.filter((booking) => booking.id !== id)
        );
      })
      .catch((error) => {
        console.error("Error deleting booking:", error);
        setErrorMessage("An error occurred while deleting the booking.");
      });
  };

  if (errorMessage) return <p className="error-message">{errorMessage}</p>;
  if (!user) return <p>Loading...</p>;

  return (
    <div className="profile-container">
      <h1 className="profile-title">Welcome, {user.name}!</h1>
      <h2>Your Bookings</h2>
      <ul className="bookings-list">
        {bookings.map((booking) => (
          <li key={booking.id} className="booking-item">
            {editingBooking && editingBooking.id === booking.id ? (
              <div>
                <h3>Edit Booking</h3>
                <div className="edit-form">
                  <label>
                    Date:
                    <input
                      type="date"
                      name="bookingDate"
                      value={updatedBooking.bookingDate}
                      onChange={handleInputChange}
                    />
                  </label>
                  <label>
                    Time:
                    <input
                      type="time"
                      name="bookingTime"
                      value={updatedBooking.bookingTime}
                      onChange={handleInputChange}
                    />
                  </label>
                  <div className="button-container">
                    <button
                      className="save-btn"
                      type="button"
                      onClick={() => handleSaveEdit(booking.id)}
                    >
                      Save
                    </button>
                    <button
                      className="cancel-btn"
                      type="button"
                      onClick={() => setEditingBooking(null)}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="booking-info">
                <h3>{booking.room || booking.amenity}</h3>
                <p>{booking.description}</p>
                <p>Cost: {booking.cost}</p>
                <p>Date: {booking.bookingDate}</p>
                <p>Time: {booking.bookingTime}</p>
                <div className="button-container">
                  <button
                    className="edit-btn"
                    onClick={() => handleEdit(booking)}
                  >
                    Edit
                  </button>
                  <button
                    className="delete-btn"
                    onClick={() => handleDelete(booking.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Profile;
