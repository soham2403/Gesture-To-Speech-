import React, { useState } from "react";
import axios from "axios";

const SignupPage = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/signup",
        JSON.stringify(formData), // Convert formData to JSON
        { headers: { "Content-Type": "application/json" } } // Specify JSON content type
      );
      console.log("Signup successful!", response.data);
      window.location.href = response.data.redirect_url;

      // Handle successful signup, e.g., redirect to another page
    } catch (error) {
      if (error.response) {
        // Server responded with an error status code
        console.error("Signup failed!", error.response.data);
        // Handle signup error, e.g., display error message to the user
      } else {
        // Something went wrong with the request (e.g., network error)
        console.error("Signup failed!", error.message);
        // Handle network error, e.g., display a generic error message to the user
      }
    }
  };

  return (
    <div class="flex flex-col items-center justify-center min-h-screen bg-gray-900">
      <form
        onSubmit={handleSubmit}
        className="bg-gray-800 shadow-md rounded px-8 pt-6 pb-8 mb-4"
      >
        <div class="mb-4">
          <label
            class="block text-gray-300 text-sm font-bold mb-2"
            htmlFor="username"
          >
            Username
          </label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            class="px-4 py-2 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 w-full bg-gray-700 text-gray-200"
            placeholder="Username"
            required
          />
        </div>
        <div class="mb-4">
          <label
            class="block text-gray-300 text-sm font-bold mb-2"
            htmlFor="email"
          >
            Email
          </label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className="px-4 py-2 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 w-full bg-gray-700 text-gray-200"
            placeholder="Email"
            required
          />
        </div>
        <div class="mb-4">
          <label
            class="block text-gray-300 text-sm font-bold mb-2"
            htmlFor="password"
          >
            Password
          </label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="px-4 py-2 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 w-full bg-gray-700 text-gray-200"
            placeholder="Password"
            required
          />
        </div>
        <div class="mb-6">
          <label
            className="block text-gray-300 text-sm font-bold mb-2"
            htmlFor="confirmPassword"
          >
            Confirm Password
          </label>
          <input
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            class="px-4 py-2 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 w-full bg-gray-700 text-gray-200"
            placeholder="Confirm Password"
            required
          />
        </div>
        <button
          type="submit"
          class="bg-teal-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          Sign Up
        </button>
      </form>
    </div>
  );
};

export default SignupPage;
