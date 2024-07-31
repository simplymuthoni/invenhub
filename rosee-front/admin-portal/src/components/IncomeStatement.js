import React, { useState, useEffect } from 'react';
import axios from 'axios';

const IncomeStatement = () => {
    const [statement, setStatement] = useState(null);

    useEffect(() => {
        const fetchStatement = async () => {
            const response = await axios.get('/api/admin/income_statement');
            setStatement(response.data);
        };
        fetchStatement();
    }, []);

    return (
        <div>
            <h3>Income Statement</h3>
            {statement && (
                <div>
                    <p>Total Sales: {statement.total_sales}</p>
                    <p>Delivery Costs: {statement.delivery_costs}</p>
                    <p>Total Profit: {statement.total_profit}</p>
                </div>
            )}
        </div>
    );
};

export default IncomeStatement;
