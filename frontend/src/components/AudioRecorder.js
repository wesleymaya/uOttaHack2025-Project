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

            const res = await fetch('/api/audio-to-text', {
                method: 'POST',
                body: formData,
            });
            const data = await res.json();
            addMessage('user', data.transcribed_text);
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
                <button className="bg-red-500 text-white px-4 py-2 rounded" onClick={stopRecording}>
                    Stop Recording
                </button>
            ) : (
                <button className="bg-green-500 text-white px-4 py-2 rounded" onClick={startRecording}>
                    Start Recording
                </button>
            )}
        </div>
    );
}
