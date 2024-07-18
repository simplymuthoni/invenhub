import React, { useState } from 'react';
import API from '../api';

const AddItem = () => {
  const [form, setForm] = useState({
    name: '',
    category: '',
    size: '',
    color: '',
    price: '',
    stock: ''
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    API.post('/items', form)
      .then(response => {
        console.log(response.data);
        setForm({
          name: '',
          category: '',
          size: '',
          color: '',
          price: '',
          stock: ''
        });
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
      <button type="submit">Add Item</button>
    </form>
  );
};

export default AddItem;
