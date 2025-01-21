'use client';

import { useState, useEffect } from 'react';
import Chat from '../components/Chat';
import AudioRecorder from '../components/AudioRecorder';
import ResetButton from '../components/ResetButton';
import Dashboard from '../components/Dashboard';

export default function Page() {
    const [messages, setMessages] = useState([]);
    const [dashboardData, setDashboardData] = useState();

    const addMessage = (role, content) => {
        setMessages((prevMessages) => [...prevMessages, { role, content }]);
    };

    const refreshDashboard = (data) => {
        console.log("data to be used in refresh: ", data)
        setDashboardData(data)
        //console.log("updated data: ", dashboardData)
    }

    useEffect(() => {
        console.log("Updated dashboardData:", dashboardData);
    }, [dashboardData]);

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Budgeting Assistant</h1>
            <div className="grid grid-cols-2 gap-8">
                <div className="break-after-column">
                    <Chat messages={messages} addMessage={addMessage} refreshDashboard={refreshDashboard} />
                    <AudioRecorder addMessage={addMessage} refreshDashboard={refreshDashboard} />
                    <ResetButton setMessages={setMessages} />
                </div>

                <div className="container">
                    <Dashboard addMessage={addMessage} data={dashboardData} />
                </div>
            </div>
            
        </div>
    );
}
