import { useState, useEffect } from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

export default function Dashboard({ addMessage, dashboardData }) {
    const [budgetData, setBudgetData] = useState(null);

    useEffect(() => {
        // Update budgetData when dashboardData changes
        if (dashboardData) {
            console.log("Received dashboardData:", dashboardData);
            try {
                // Parse or use dashboardData as is, depending on its format
                const parsedData = typeof dashboardData === "string"
                    ? JSON.parse(dashboardData)
                    : dashboardData;
                setBudgetData(parsedData.Budget);
            } catch (error) {
                console.error('Error parsing dashboardData:', error);
            }
        }
    }, [dashboardData]);

    if (!budgetData) {
        return (
            <div className="p-4 border rounded mb-4">
                No data available. Start by telling the Assistant your income!
            </div>
        );
    }

    // Calculate leftover budget
    const totalExpenses = budgetData.items.reduce((sum, item) => sum + item.amount, 0);
    const leftoverBudget = budgetData.budget_limit - totalExpenses;

    // Prepare data for the pie chart
    const pieData = {
        labels: [...budgetData.items.map(item => item.item_name), "Leftover Budget"],
        datasets: [
            {
                label: 'Expenses',
                data: [...budgetData.items.map(item => item.amount), leftoverBudget > 0 ? leftoverBudget : 0],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                ],
                borderWidth: 1,
            },
        ],
    };

    return (
        <div className="p-4 border border-orange-500 rounded mb-4">
            <div>
                <h3>Dashboard Data:</h3>
                {dashboardData ? <p>Data: {JSON.stringify(dashboardData)}</p> : <p>No data yet</p>}
            </div>

            <h1 className="font-bold underline">Dashboard</h1>
            <h2>Budget Limit: ${budgetData.budget_limit.toFixed(2)}</h2>

            <h3>Expenses:</h3>
            <div className="mb-4">
                <table className="table-auto">
                    <thead>
                        <tr className="bg-orange-500">
                            <th className="border px-4 py-2">Item</th>
                            <th className="border px-4 py-2">Amount</th>
                            <th className="border px-4 py-2">Category</th>
                            <th className="border px-4 py-2">Recurrence Schedule</th>
                            <th className="border px-4 py-2">Due Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {budgetData.items.map((item, index) => (
                            <tr className="bg-orange-600" key={index}>
                                <td className="border px-4 py-2">{item.item_name}</td>
                                <td className="border px-4 py-2">${item.amount.toFixed(2)}</td>
                                <td className="border px-4 py-2">{item.category}</td>
                                <td className="border px-4 py-2">{item.recurrence_schedule}</td>
                                <td className="border px-4 py-2">{item.due_date ? item.due_date : "N/A"}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <h3 className="text-center">Expense Distribution (Pie Chart):</h3>
            <div className="w-1/2 mx-auto">
                <Pie data={pieData} />
            </div>
        </div>
    );
}
