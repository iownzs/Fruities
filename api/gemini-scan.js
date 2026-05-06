export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    res.status(500).json({ error: 'Missing GEMINI_API_KEY environment variable.' });
    return;
  }

  // TODO: Add the Gemini Vision request here.
  // Keep this server-side so the API key never appears in browser code.
  res.status(501).json({ error: 'Gemini scan endpoint scaffolded but not implemented yet.' });
}
