import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ItemForm from './ItemForm';

const ItemList = () => {
    const [items, setItems] = useState([]);

    useEffect(() => {
        const fetchItems = async () => {
            const response = await axios.get('/api/admin/list');
            setItems(response.data);
        };
        fetchItems();
    }, []);

    const deleteItem = async (id) => {
        await axios.delete(`/api/admin/items/${id}`);
        setItems(items.filter(item => item.id !== id));
    };

    return (
        <div>
            <h2>Item List</h2>
            <ul>
                {items.map(item => (
                    <li key={item.id}>
                        {item.name} - {item.category} - ${item.price}
                        <button onClick={() => deleteItem(item.id)}>Delete</button>
                    </li>
                ))}
            </ul>
            <ItemForm setItems={setItems} />
        </div>
    );
};

export default ItemList;
