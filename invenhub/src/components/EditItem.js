import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import API from '../api';

const EditItem = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: '',
    category: '',
    size: '',
    color: '',
    price: '',
    stock: ''
  });

  useEffect(() => {
    API.get(`/items/${id}`)
      .then(response => {
        setForm(response.data);
      })
      .catch(error => console.error(error));
  }, [id]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    API.put(`/items/${id}`, form)
      .then(response => {
        console.log(response.data);
        navigate.push('/inventory'); // Redirect to the inventory list after successful update
      })
      .catch(error => console.error(error));
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" placeholder="Name" value={form.name} onChange={handleChange} required />
      <input name="category" placeholder="Category" value={form.category} onChange={handleChange} required />
      <input name="size" placeholder="Size" value={form.size} onChange={handleChange} required />
      <input name="color" placeholder="Color" value={form.color} onChange={handleChange} required />
      <input name="price" placeholder="Price" type="number" value={form.price} onChange={handleChange} required />
      <input name="stock" placeholder="Stock" type="number" value={form.stock} onChange={handleChange} required />
      <button type="submit">Save Changes</button>
    </form>
  );
};

export default EditItem;
