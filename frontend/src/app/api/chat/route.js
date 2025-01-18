// CHAT ROUTE
export async function POST(req) {
    try {
        const { user_message } = await req.json();

        if (!user_message) {
            return new Response(JSON.stringify({ error: 'User message is required.' }), {
                status: 400,
                headers: { 'Content-Type': 'application/json' },
            });
        }

        const assistantResponse = `Got it! I will add "${user_message}" to your budget.`;

        return new Response(
            JSON.stringify({ assistant_response: assistantResponse }),
            {
                status: 200,
                headers: { 'Content-Type': 'application/json' },
            }
        );
    } catch (error) {
        console.error(error);
        return new Response(JSON.stringify({ error: 'Internal Server Error' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' },
        });
    }
}


