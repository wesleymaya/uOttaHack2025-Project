import { useState } from 'react';

const axios = require('axios');

export default function Chat({ messages, addMessage }) {
    const [inputText, setInputText] = useState('');

    const sendMessage = async () => {
        if (!inputText.trim()) {
            alert("Message cannot be empty!");
            return;
        }

        // Add the user's message immediately
        addMessage('user', inputText);

        try {
            const res = await fetch('http://localhost:8000/getdata', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application.json' },
                body: JSON.stringify({ user_message: inputText }),
            });

            if (!res.ok) {
                throw new Error(`Server error: ${res.statusText}`);
            }

            const data = await res.json();

            // Add the assistant's response
            addMessage('assistant', data.assistant_response);
            setInputText('');
        } catch (error) {
            console.error("Error sending message:", error);
            alert("Failed to send message. Please try again.");
        }
    };

    return (
        <div className="mb-4">
            <div className="chat-box p-4 border rounded mb-4">
                {messages.map((msg, idx) => (
                    <p key={idx} className={msg.role === 'user' ? 'text-left bg-blue-400 text-white-500 mt-1 rounded-lg px-2' : 'text-right bg-green-400 text-white-500 mt-1 rounded-lg px-2'}>
                        <strong>{msg.role === 'user' ? 'You:' : 'Assistant:'}</strong> {msg.content}
                    </p>
                ))}
            </div>
            <textarea
                className="w-full p-2 min-h-10 border rounded text-black"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Type your expense or question..."
            />
            <button
                className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 mt-2 rounded"
                onClick={sendMessage}
            >
                Send
            </button>
        </div>
    );
}
