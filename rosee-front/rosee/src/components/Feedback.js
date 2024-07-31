import React, { useState } from 'react';
import { submitFeedback } from '../api';

function Feedback() {
  const [form, setForm] = useState({
    user_id: '',
    rating: '',
    comment: '',
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await submitFeedback(form);
      alert(response.data.message);
    } catch (error) {
      alert('Error submitting feedback');
    }
  };

  return (
    <div>
      <h2>Feedback</h2>
      <form onSubmit={handleSubmit}>
        <input type="number" name="user_id" placeholder="User ID" onChange={handleChange} />
        <input type="number" name="rating" placeholder="Rating" onChange={handleChange} />
        <textarea name="comment" placeholder="Comment" onChange={handleChange}></textarea>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default Feedback;
