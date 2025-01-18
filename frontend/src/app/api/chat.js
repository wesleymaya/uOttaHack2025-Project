export default function handler(req, res) {
    const { user_message } = req.body;
    res.status(200).json({
        assistant_response: `Got it! I will add "${user_message}" to your budget.`,
    });
}
