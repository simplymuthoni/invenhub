import React, { useState, useEffect } from 'react';
import axios from 'axios';
import IncomeStatement from './IncomeStatement';
import BalanceSheet from './BalanceSheet';

const Reports = () => {
    const [reports, setReports] = useState(null);

    useEffect(() => {
        const fetchReports = async () => {
            const response = await axios.get('/api/admin/reports');
            setReports(response.data);
        };
        fetchReports();
    }, []);

    return (
        <div>
            <h2>Reports</h2>
            {reports && (
                <div>
                    <p>Total Purchases: {reports.purchases}</p>
                    <p>Total Profit: {reports.total_profit}</p>
                </div>
            )}
            <IncomeStatement />
            <BalanceSheet />
        </div>
    );
};

export default Reports;
