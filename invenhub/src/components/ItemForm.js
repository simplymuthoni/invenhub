import React, { useState } from 'react';

const ItemForm = ({ onAdd }) => {
  const [name, setName] = useState('');
  const [category, setCategory] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onAdd({ id: Date.now(), name, category });
    setName('');
    setCategory('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Item Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="text"
        placeholder="Category"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
      />
      <button type="submit">Add Item</button>
    </form>
  );
};

export default ItemForm;
