import { useState } from 'react';

export default function Chat({ messages, addMessage }) {
  const [inputText, setInputText] = useState('');

    const sendMessage = async () => {
        if (!inputText.trim()) {
            alert("Message cannot be empty!");
            return;
        }

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_message: inputText }),
            });

            if (!res.ok) {
                throw new Error(`Server error: ${res.statusText}`);
            }

            const data = await res.json();
            addMessage('user', inputText);
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
          <p key={idx} className={msg.role === 'user' ? 'text-blue-500' : 'text-green-500'}>
            <strong>{msg.role === 'user' ? 'You:' : 'Assistant:'}</strong> {msg.content}
          </p>
        ))}
      </div>
      <textarea
        className="w-full p-2 border rounded text-black"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Type your expense or question..."
      />
      <button
        className="bg-blue-500 text-white px-4 py-2 mt-2 rounded"
        onClick={sendMessage}
      >
        Send
      </button>
    </div>
  );
}
