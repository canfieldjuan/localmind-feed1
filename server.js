const express = require('express');
const fetch = require('node-fetch');
require('dotenv').config();
const app = express();
app.use(express.json());
app.use(express.static('.'));

app.post('/agent', async (req, res) => {
  const prompt = req.body.prompt;
  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'gpt-3.5-turbo',
        messages: [{ role: 'user', content: prompt }]
      })
    });
    const data = await response.json();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: 'Agent unreachable.' });
  }
});

app.listen(3000, () => console.log('Agent is listening on port 3000'));
