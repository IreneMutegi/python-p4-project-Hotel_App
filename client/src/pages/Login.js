import React, { useState, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGoogle, faFacebook, faApple } from "@fortawesome/free-brands-svg-icons";
import { useNavigate } from "react-router-dom";
import "./Login.css";
import slide1 from "../assets/images/slide1.jpeg";
import slide2 from "../assets/images/slide2.jpeg";
import slide3 from "../assets/images/slide3.jpeg";

function Login({ onLogin }) {
  const [name, setName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [currentSlide, setCurrentSlide] = useState(0);
  const slides = [slide1, slide2, slide3];
  const navigate = useNavigate();

  const API_URL = "http://127.0.0.1:5555";

  const handleLogin = async (e) => {
    e.preventDefault();
    
    if (!username || !email || !password) {
      setError("Please fill out all fields.");
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError("Please enter a valid email.");
      return;
    }

    setError(null); // Reset error when user starts submitting
    const loginData = {
      username,
      email,
      password
    };

    try {
      const response = await fetch(`${API_URL}/users`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loginData),
      });

      if (response.ok) {
        const user = await response.json();
        const { access_token } = user; // Get the JWT token

        localStorage.setItem("clientName", user.name);
        localStorage.setItem("clientUsername", user.username);
        localStorage.setItem("access_token", access_token); // Store the token
        onLogin(user); // Pass user data to parent
        setUsername("");
        setEmail("");
        setPassword("");
        navigate("/profile"); // Redirect to profile page
      } else {
        const errorData = await response.json();
        setError(errorData.error || "Login failed. Please check your credentials.");
      }
    } catch (error) {
      console.error("Error during login:", error);
      setError("There was an error during login.");
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSlide((prevSlide) => (prevSlide + 1) % slides.length);
    }, 3000);
    return () => clearInterval(interval); // Cleanup on component unmount
  }, [slides.length]);

  return (
    <div className="login-container">
      <div className="slideshow-container">
        <img src={slides[currentSlide]} alt="Hotel Slideshow" className="slideshow-image" />
        <div className="caption">We hope you enjoy your vacation</div>
      </div>

      <div className="login-form-container">
        <h2>Welcome to the Luxury Hotel login page</h2>
        <p>
          Keep up with all your activities. Are you new here? <a href="/register">Create an Account</a>
        </p>

        <form onSubmit={handleLogin}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="login-input"
            aria-label="Username"
            onFocus={() => setError(null)} // Reset error on focus
          />
          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="login-input"
            aria-label="Email Address"
            onFocus={() => setError(null)} // Reset error on focus
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="login-input"
            aria-label="Password"
            onFocus={() => setError(null)} // Reset error on focus
          />
          <a href="#" className="forgot-password">Forgot password?</a>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="login-button">Login</button>
        </form>

        <div className="social-login">
          <p>Or sign in with</p>
          <div className="social-icons">
            <button className="social-button google">
              <FontAwesomeIcon icon={faGoogle} /> Google
            </button>
            <button className="social-button facebook">
              <FontAwesomeIcon icon={faFacebook} /> Facebook
            </button>
            <button className="social-button apple">
              <FontAwesomeIcon icon={faApple} /> Apple
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
