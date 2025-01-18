// AUDIO TO TEXT ROUTE
export async function POST(req) {
    return new Response(
        JSON.stringify({ transcribed_text: 'Sample transcribed text.' }),
        {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
        }
    );
}
