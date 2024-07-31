import React, { useState, useEffect } from 'react';
import axios from 'axios';

const GoodsReceivedNote = ({ grnId }) => {
    const [note, setNote] = useState(null);

    useEffect(() => {
        const fetchNote = async () => {
            const response = await axios.get(`/api/admin/goods_received_note/${grnId}`);
            setNote(response.data);
        };
        fetchNote();
    }, [grnId]);

    return (
        <div>
            <h2>Goods Received Note</h2>
            {note && (
                <div>
                    <p>Purchase Order ID: {note.purchase_order_id}</p>
                    <p>Received Date: {note.received_date}</p>
                    <p>Items Received: {note.items_received}</p>
                </div>
            )}
        </div>
    );
};

export default GoodsReceivedNote;
