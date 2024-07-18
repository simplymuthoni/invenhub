import React, { useEffect, useState } from 'react';
import API from '../api';

const InventoryList = () => {
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    API.get('/items')
      .then(response => {
        setInventory(response.data);
      })
      .catch(error => console.error(error));
  }, []);

  return (
    <div>
      <h2>Inventory List</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Category</th>
            <th>Size</th>
            <th>Color</th>
            <th>Price</th>
            <th>Stock</th>
          </tr>
        </thead>
        <tbody>
          {inventory.map(item => (
            <tr key={item.id}>
              <td>{item.name}</td>
              <td>{item.category}</td>
              <td>{item.size}</td>
              <td>{item.color}</td>
              <td>{item.price}</td>
              <td>{item.stock}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default InventoryList;
