import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PurchaseOrders = () => {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        const fetchOrders = async () => {
            const response = await axios.get('/api/admin/purchase_order');
            setOrders(response.data);
        };
        fetchOrders();
    }, []);

    return (
        <div>
            <h2>Purchase Orders</h2>
            <ul>
                {orders.map(order => (
                    <li key={order.id}>
                        {order.supplier} - {order.order_date} - ${order.total_amount}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default PurchaseOrders;
