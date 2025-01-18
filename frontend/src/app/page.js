'use client';

import { useState } from 'react';
import Chat from '../components/Chat';
import AudioRecorder from '../components/AudioRecorder';
import ResetButton from '../components/ResetButton';

export default function Page() {
    const [messages, setMessages] = useState([]);

    const addMessage = (role, content) => {
        setMessages([...messages, { role, content }]);
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Budgeting Assistant</h1>
            <Chat messages={messages} addMessage={addMessage} />
            <AudioRecorder addMessage={addMessage} />
            <ResetButton setMessages={setMessages} />
        </div>
    );
}
