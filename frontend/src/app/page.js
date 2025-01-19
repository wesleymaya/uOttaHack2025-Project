'use client';

import { useState } from 'react';
import Chat from '../components/Chat';
import AudioRecorder from '../components/AudioRecorder';
import ResetButton from '../components/ResetButton';
import Dashboard from '../components/Dashboard';

export default function Page() {
    const [messages, setMessages] = useState([]);

    const addMessage = (role, content) => {
        setMessages((prevMessages) => [...prevMessages, { role, content }]);
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Budgeting Assistant</h1>
            <div className="grid grid-cols-2 gap-8">
                <div className="break-after-column">
                    <Chat messages={messages} addMessage={addMessage} />
                    <AudioRecorder addMessage={addMessage} />
                    <ResetButton setMessages={setMessages} />
                </div>

                <div className="container">
                    <Dashboard addMessage={addMessage} />
                </div>
            </div>
            
        </div>
    );
}
