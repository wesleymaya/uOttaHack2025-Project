import { useState } from 'react';

export default function AudioRecorder({ addMessage }) {
    const [recording, setRecording] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState(null);

    const startRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const recorder = new MediaRecorder(stream);
        let chunks = [];

        recorder.ondataavailable = (e) => chunks.push(e.data);
        recorder.onstop = async () => {
            const blob = new Blob(chunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append('audio', blob);

            try {
                // Fetch transcribed audio
                const res = await fetch('/api/audio-to-text', {
                    method: 'POST',
                    body: formData,
                });

                if (!res.ok) {
                    throw new Error(`Server error: ${res.statusText}`);
                }

                const data = await res.json();

                // Add the transcribed audio as the user's message
                const userMessage = data.transcribed_text || "Audio transcription failed.";
                addMessage('user', userMessage);

                // Fetch the assistant's response
                const assistantRes = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_message: userMessage }),
                });

                if (!assistantRes.ok) {
                    throw new Error(`Server error: ${assistantRes.statusText}`);
                }

                const assistantData = await assistantRes.json();

                // Add the assistant's response to the log
                addMessage('assistant', assistantData.assistant_response);
            } catch (error) {
                console.error("Error handling audio input:", error);
                alert("Failed to process audio. Please try again.");
            }
        };

        recorder.start();
        setMediaRecorder(recorder);
        setRecording(true);
    };

    const stopRecording = () => {
        mediaRecorder?.stop();
        setRecording(false);
    };

    return (
        <div>
            {recording ? (
                <button className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded" onClick={stopRecording}>
                    Stop Recording
                </button>
            ) : (
                <button className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded" onClick={startRecording}>
                    Start Recording
                </button>
            )}
        </div>
    );
}
