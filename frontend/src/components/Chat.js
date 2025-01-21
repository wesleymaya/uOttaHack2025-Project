import { useState } from 'react';

const axios = require('axios');

export default function Chat({ messages, addMessage, refreshDashboard }) {
    const [inputText, setInputText] = useState('');

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!inputText.trim()) {
            alert("Message cannot be empty!");
            return;
        }

        // Add the user's message immediately
        addMessage('user', inputText);

        // Clear the input field  
        setInputText('');

        try {
            const res = await axios.post('http://localhost:8000/getdata', {
                message: inputText,
            });

            // Extract the "conversation" part of the response JSON and add it as an assistant message
            const conversation = res.data?.conversation;
            if (conversation) {
                addMessage('assistant', conversation);
            } else {
                console.error('Invalid response format:', res.data);
                addMessage('assistant', 'Sorry, I couldn\'t process your message.');
            }

            // Send data to parent in order to update Dashboard.js
            refreshDashboard(res.data)

        } catch (error) {
            console.error('Error sending message:', error);
            addMessage('assistant', 'An error occurred while processing your request.');
        }
    };

    const onEnterPress = (e) => {
        console.log("here")
        if (e.keyCode == 13 && e.shiftKey == false) {
            sendMessage
        }
    }

    return (
        <div className="mb-4">
            <div className="chat-box p-4 border rounded mb-4">
                {messages.map((msg, idx) => (
                    <p
                        key={idx}
                        className={msg.role === 'user' ? 'text-left bg-blue-400 text-white-500 mt-1 rounded-lg px-2' : 'text-right bg-green-400 text-white-500 mt-1 rounded-lg px-2'
                        }>
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
