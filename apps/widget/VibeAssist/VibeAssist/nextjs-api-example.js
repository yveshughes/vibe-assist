// Example Next.js API Route
// This file should be placed in your Next.js project at:
// pages/api/widget-data.js (for Pages Router)
// OR
// app/api/widget-data/route.js (for App Router)

// Example for App Router (Next.js 13+):
export async function GET(request) {
  // You can add any logic here to fetch data from your database,
  // process it, or generate dynamic content
  
  const data = {
    title: "Vibe Assist",
    message: "Your custom message from Next.js!",
    timestamp: new Date().toISOString()
  };
  
  return Response.json(data, {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
      // Allow the iOS widget to access this endpoint
      'Access-Control-Allow-Origin': '*',
    },
  });
}

// Example for Pages Router (older Next.js):
/*
export default function handler(req, res) {
  if (req.method === 'GET') {
    const data = {
      title: "Vibe Assist",
      message: "Your custom message from Next.js!",
      timestamp: new Date().toISOString()
    };
    
    res.status(200).json(data);
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
*/
