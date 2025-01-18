import { useState } from 'react';

export default function Chat({ messages, addMessage }) {
    const [inputText, setInputText] = useState('');

    const sendMessage = async () => {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_message: inputText }),
        });
        const data = await res.json();
        addMessage('user', inputText);
        addMessage('assistant', data.assistant_response);
        setInputText('');
    };

    return (
        <div>
            <div>
                {messages.map((msg, idx) => (
                    <p key={idx} className={msg.role}>
                        {msg.role === 'user' ? 'You: ' : 'Assistant: '}
                        {msg.content}
                    </p>
                ))}
            </div>
            <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Type your expense or question..."
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
}
