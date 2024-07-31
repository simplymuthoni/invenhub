import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BalanceSheet = () => {
    const [sheet, setSheet] = useState(null);

    useEffect(() => {
        const fetchSheet = async () => {
            const response = await axios.get('/api/admin/balance_sheet');
            setSheet(response.data);
        };
        fetchSheet();
    }, []);

    return (
        <div>
            <h3>Balance Sheet</h3>
            {sheet && (
                <div>
                    <p>Total Assets: {sheet.total_assets}</p>
                    <p>Total Liabilities: {sheet.total_liabilities}</p>
                    <p>Equity: {sheet.equity}</p>
                </div>
            )}
        </div>
    );
};

export default BalanceSheet;
