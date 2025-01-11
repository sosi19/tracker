const { v4: uuidv4 } = require('uuid');
const faunadb = require('faunadb');
const q = faunadb.query;

const client = new faunadb.Client({
    secret: process.env.FAUNA_SECRET_KEY
});

exports.handler = async (event) => {
    if (event.httpMethod !== 'POST') {
        return { statusCode: 405, body: 'Method Not Allowed' };
    }

    try {
        const data = JSON.parse(event.body);
        const linkId = uuidv4().slice(0, 8);
        
        const linkData = {
            target_url: data.target_url,
            description: data.description,
            created_at: new Date().toISOString(),
            visits: 0
        };

        await client.query(
            q.Create(
                q.Collection('links'),
                { data: { id: linkId, ...linkData } }
            )
        );

        return {
            statusCode: 200,
            body: JSON.stringify({ id: linkId, ...linkData })
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Failed to create link' })
        };
    }
}; 