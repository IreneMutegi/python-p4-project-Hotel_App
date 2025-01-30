import React, { useState, useEffect } from "react";
import './Profile.css';

function Profile() {
  const [user, setUser] = useState(null);
  const [roomBookings, setRoomBookings] = useState([]);
  const [amenityBookings, setAmenityBookings] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [editingRoomBooking, setEditingRoomBooking] = useState(null);
  const [editingAmenityBooking, setEditingAmenityBooking] = useState(null);
  const [updatedRoomBooking, setUpdatedRoomBooking] = useState({
    bookingTime: "",
  });
  const [updatedAmenityBooking, setUpdatedAmenityBooking] = useState({
    bookingTime: "",
  });

  useEffect(() => {
    // Retrieve user details from localStorage
    const userName = localStorage.getItem("clientName");
    const userEmail = localStorage.getItem("clientUsername");

    if (userName && userEmail) {
      // Set user details
      setUser({ name: userName, email: userEmail });

      // Fetch user-specific room bookings
      fetch(`http://localhost:5555/bookings?clientEmail=${userEmail}`)
        .then((response) => response.json())
        .then((data) => {
          const roomBookings = data.filter((booking) => booking.room);
          const amenityBookings = data.filter((booking) => booking.amenity);
          setRoomBookings(roomBookings);
          setAmenityBookings(amenityBookings);
        })
        .catch((error) => {
          console.error("Error fetching bookings:", error);
          setErrorMessage("An error occurred while fetching bookings.");
        });
    } else {
      setErrorMessage("No user logged in.");
    }
  }, []);

  const handleEditRoomBooking = (booking) => {
    setEditingRoomBooking(booking);
    setUpdatedRoomBooking({
      bookingTime: booking.bookingTime,
    });
  };

  const handleEditAmenityBooking = (booking) => {
    setEditingAmenityBooking(booking);
    setUpdatedAmenityBooking({
      bookingTime: booking.bookingTime,
    });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (editingRoomBooking) {
      setUpdatedRoomBooking((prevState) => ({
        ...prevState,
        [name]: value,
      }));
    } else {
      setUpdatedAmenityBooking((prevState) => ({
        ...prevState,
        [name]: value,
      }));
    }
  };

  const handleSaveRoomEdit = (id) => {
    fetch(`http://localhost:5555/room_bookings/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedRoomBooking),
    })
      .then((response) => response.json())
      .then((data) => {
        setRoomBookings((prevBookings) =>
          prevBookings.map((booking) =>
            booking.id === id ? { ...booking, ...updatedRoomBooking } : booking
          )
        );
        setEditingRoomBooking(null); // Close the edit form
      })
      .catch((error) => {
        console.error("Error saving edited room booking:", error);
        setErrorMessage("An error occurred while saving the booking.");
      });
  };

  const handleSaveAmenityEdit = (id) => {
    fetch(`http://localhost:5555/amenity_bookings/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedAmenityBooking),
    })
      .then((response) => response.json())
      .then((data) => {
        setAmenityBookings((prevBookings) =>
          prevBookings.map((booking) =>
            booking.id === id ? { ...booking, ...updatedAmenityBooking } : booking
          )
        );
        setEditingAmenityBooking(null); // Close the edit form
      })
      .catch((error) => {
        console.error("Error saving edited amenity booking:", error);
        setErrorMessage("An error occurred while saving the booking.");
      });
  };

  const handleDeleteRoomBooking = (id) => {
    fetch(`http://localhost:5555/room_bookings/${id}`, {
      method: "DELETE",
    })
      .then(() => {
        setRoomBookings((prevBookings) =>
          prevBookings.filter((booking) => booking.id !== id)
        );
      })
      .catch((error) => {
        console.error("Error deleting room booking:", error);
        setErrorMessage("An error occurred while deleting the booking.");
      });
  };

  const handleDeleteAmenityBooking = (id) => {
    fetch(`http://localhost:5555/amenity_bookings/${id}`, {
      method: "DELETE",
    })
      .then(() => {
        setAmenityBookings((prevBookings) =>
          prevBookings.filter((booking) => booking.id !== id)
        );
      })
      .catch((error) => {
        console.error("Error deleting amenity booking:", error);
        setErrorMessage("An error occurred while deleting the booking.");
      });
  };

  if (errorMessage) return <p className="error-message">{errorMessage}</p>;
  if (!user) return <p>Loading...</p>;

  return (
    <div className="profile-container">
      <h1 className="profile-title">Welcome, {user.name}!</h1>
      <h2>Your Room Bookings</h2>
      <ul className="bookings-list">
        {roomBookings.map((booking) => (
          <li key={booking.id} className="booking-item">
            {editingRoomBooking && editingRoomBooking.id === booking.id ? (
              <div>
                <h3>Edit Room Booking</h3>
                <div className="edit-form">
                  <label>
                    Time:
                    <input
                      type="time"
                      name="bookingTime"
                      value={updatedRoomBooking.bookingTime}
                      onChange={handleInputChange}
                    />
                  </label>
                  <div className="button-container">
                    <button
                      className="save-btn"
                      type="button"
                      onClick={() => handleSaveRoomEdit(booking.id)}
                    >
                      Save
                    </button>
                    <button
                      className="cancel-btn"
                      type="button"
                      onClick={() => setEditingRoomBooking(null)}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="booking-info">
                <h3>{booking.room.name}</h3>
                <p>{booking.room.description}</p>
                <p>Cost: {booking.room.price}</p>
                <p>Time: {booking.bookingTime}</p>
                <div className="button-container">
                  <button
                    className="edit-btn"
                    onClick={() => handleEditRoomBooking(booking)}
                  >
                    Edit
                  </button>
                  <button
                    className="delete-btn"
                    onClick={() => handleDeleteRoomBooking(booking.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            )}
          </li>
        ))}
      </ul>

      <h2>Your Amenity Bookings</h2>
      <ul className="bookings-list">
        {amenityBookings.map((booking) => (
          <li key={booking.id} className="booking-item">
            {editingAmenityBooking && editingAmenityBooking.id === booking.id ? (
              <div>
                <h3>Edit Amenity Booking</h3>
                <div className="edit-form">
                  <label>
                    Time:
                    <input
                      type="time"
                      name="bookingTime"
                      value={updatedAmenityBooking.bookingTime}
                      onChange={handleInputChange}
                    />
                  </label>
                  <div className="button-container">
                    <button
                      className="save-btn"
                      type="button"
                      onClick={() => handleSaveAmenityEdit(booking.id)}
                    >
                      Save
                    </button>
                    <button
                      className="cancel-btn"
                      type="button"
                      onClick={() => setEditingAmenityBooking(null)}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="booking-info">
                <h3>{booking.amenity.name}</h3>
                <p>{booking.amenity.description}</p>
                <p>Cost: {booking.amenity.charges}</p>
                <p>Time: {booking.bookingTime}</p>
                <div className="button-container">
                  <button
                    className="edit-btn"
                    onClick={() => handleEditAmenityBooking(booking)}
                  >
                    Edit
                  </button>
                  <button
                    className="delete-btn"
                    onClick={() => handleDeleteAmenityBooking(booking.id)}
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
