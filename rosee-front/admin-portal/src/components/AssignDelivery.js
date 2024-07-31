import React, { useState } from 'react';
import axios from 'axios';

const AssignDelivery = () => {
    const [userId, setUserId] = useState('');
    const [deliveryCost, setDeliveryCost] = useState('');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('/api/admin/assign_delivery', { user_id: userId, delivery_cost: deliveryCost });
            setMessage(response.data.message);
        } catch (error) {
            setMessage(error.response.data.error);
        }
    };

    return (
        <div>
            <h2>Assign Delivery</h2>
            <form onSubmit={handleSubmit}>
                <input type="number" value={userId} onChange={(e) => setUserId(e.target.value)} placeholder="User ID" required />
                <input type="number" value={deliveryCost} onChange={(e) => setDeliveryCost(e.target.value)} placeholder="Delivery Cost" required />
                <button type="submit">Assign</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default AssignDelivery;
