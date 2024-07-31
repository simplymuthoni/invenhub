import React, { useState } from 'react';
import axios from 'axios';

const ItemForm = ({ setItems }) => {
    const [name, setName] = useState('');
    const [category, setCategory] = useState('');
    const [size, setSize] = useState('');
    const [color, setColor] = useState('');
    const [price, setPrice] = useState('');
    const [stock, setStock] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const newItem = { name, category, size, color, price, stock };
        const response = await axios.post('/api/admin/items', newItem);
        setItems(prevItems => [...prevItems, response.data]);
        setName(''); setCategory(''); setSize(''); setColor(''); setPrice(''); setStock('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" required />
            <input type="text" value={category} onChange={(e) => setCategory(e.target.value)} placeholder="Category" required />
            <input type="text" value={size} onChange={(e) => setSize(e.target.value)} placeholder="Size" required />
            <input type="text" value={color} onChange={(e) => setColor(e.target.value)} placeholder="Color" required />
            <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} placeholder="Price" required />
            <input type="number" value={stock} onChange={(e) => setStock(e.target.value)} placeholder="Stock" required />
            <button type="submit">Add Item</button>
        </form>
    );
};

export default ItemForm;
