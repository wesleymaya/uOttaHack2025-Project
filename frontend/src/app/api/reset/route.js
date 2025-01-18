// RESET ROUTE
export async function POST() {
    return new Response(JSON.stringify({ message: 'Budget reset.' }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
    });
}


