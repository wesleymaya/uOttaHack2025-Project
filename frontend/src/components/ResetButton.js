export default function ResetButton({ setMessages }) {
    const resetBudget = async () => {
        await fetch('/api/reset', { method: 'POST' });
        setMessages([]);
    };

    return (
        <button
            className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded mt-4"
            onClick={resetBudget}
        >
            Reset Budget
        </button>
    );
}
