import { useState, useEffect } from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

export default function Dashboard() {
    // Simulate fetching data from the backend
    const [budgetData, setBudgetData] = useState(null);

    useEffect(() => {
        // Mock data (replace this with actual API call later)
        const mockData = {
            "Budget": {
                "budget_limit": 2000.0,
                "items": [
                    {
                        "item_name": "Rent",
                        "amount": 1200.0,
                        "category": "Recurring",
                        "importance_rank": 1,
                        "recurrence_schedule": "monthly",
                        "due_date": 1
                    },
                    {
                        "item_name": "Groceries",
                        "amount": 350.0,
                        "category": "Regular",
                        "importance_rank": 2,
                        "recurrence_schedule": "weekly",
                        "due_date": null
                    },
                    {
                        "item_name": "Utilities",
                        "amount": 400.0,
                        "category": "Recurring",
                        "importance_rank": 3,
                        "recurrence_schedule": "monthly",
                        "due_date": 15
                    }
                ]
            }
        };

        // var realdata = POST(req) how do i connect api??????????

        // Simulate delay and set data
        setTimeout(() => {
            setBudgetData(mockData.Budget);
        }, 1000);
    }, []);

    if (!budgetData) {
        return <div className="p-4 border rounded mb-4">Loading...</div>;
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
