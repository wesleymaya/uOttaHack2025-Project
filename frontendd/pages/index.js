import { useState } from 'react';
import Chat from '../components/Chat';
import AudioRecorder from '../components/AudioRecorder';
import ResetButton from '../components/ResetButton';

export default function Home() {
    const [messages, setMessages] = useState([]);

    const addMessage = (role, content) => {
        setMessages([...messages, { role, content }]);
    };

    return (
        <div>
            <h1>Budgeting Assistant</h1>
            <Chat messages={messages} addMessage={addMessage} />
            <AudioRecorder addMessage={addMessage} />
            <ResetButton setMessages={setMessages} />
        </div>
    );
}
