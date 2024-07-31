import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Invoice = ({ invoiceId }) => {
    const [invoice, setInvoice] = useState(null);

    useEffect(() => {
        const fetchInvoice = async () => {
            const response = await axios.get(`/api/admin/invoice/${invoiceId}`);
            setInvoice(response.data);
        };
        fetchInvoice();
    }, [invoiceId]);

    return (
        <div>
            <h2>Invoice</h2>
            {invoice && (
                <div>
                    <p>User ID: {invoice.user_id}</p>
                    <p>Amount: {invoice.amount}</p>
                    <p>Invoice Date: {invoice.invoice_date}</p>
                </div>
            )}
        </div>
    );
};

export default Invoice;
