import React, { useState, useEffect } from 'react';
import API from '../api';
import { Link } from 'react-router-dom';

const ItemList = () => {
  const [items, setItems] = useState([]);

  useEffect(() => {
    API.get('/items')
      .then(response => setItems(response.data))
      .catch(error => console.error(error));
  }, []);

  const deleteItem = (id) => {
    API.delete(`/items/${id}`)
      .then(() => setItems(items.filter(item => item.id !== id)))
      .catch(error => console.error(error));
  };

  return (
    <div>
      <h1>Item List</h1>
      <ul>
        {items.map(item => (
          <li key={item.id}>
            {item.name} - {item.category} - {item.size} - {item.color} - ${item.price} - Stock: {item.stock}
            <Link to={`/edit/${item.id}`}>Edit</Link>
            <button onClick={() => deleteItem(item.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ItemList;
