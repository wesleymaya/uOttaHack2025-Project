// AUDIO TO TEXT ROUTE
export async function POST(req) {
    const assistantResponse = `Got it! I will add that to your budget`;

    return new Response(
        JSON.stringify({ transcribed_text: 'Sample transcribed text.' }),
        {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
        }
    );
}
