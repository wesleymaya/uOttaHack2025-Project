export default function ResetButton({ setMessages }) {
    const resetBudget = async () => {
        await fetch('/api/reset', { method: 'POST' });
        setMessages([]);
    };

    return <button onClick={resetBudget}>Reset Budget</button>;
}