import { NextRequest, NextResponse } from 'next/server'; // Use this for server-side responses
import { getToken } from 'next-auth/jwt'; // For token retrieval
import { cookies } from 'next/headers'; // To access cookies
import { toast } from 'sonner';
export async function middleware(request: NextRequest) {
    // Get the token from cookies
    const token = await getToken({ req: request, secret: process.env.NEXTAUTH_SECRET });

    console.log('Access Token:', token?.access_token);  // Log token for debugging

    // If there's no token, redirect to the sign-in page
    if (!token) {
        return NextResponse.redirect(new URL('/api/auth/signin', request.url));
    }

    // If the token exists, send it to the backend Flask API (as an example)
    const response = await fetch('http://127.0.0.1:5000/api/receive-token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token.access_token}`, // Send token as Bearer token
        },
        body: JSON.stringify({ data: 'someData' }),
    });

    const data = await response.json();

    // Optionally handle the response
    if (response.ok) {
        toast.success('API Response:', data);
        // Proceed to the dashboard or desired route
        return NextResponse.redirect(new URL('/dashboard', request.url));
    } else {
        console.error('Error from Flask API', data);
        return NextResponse.redirect(new URL('/error', request.url)); // Handle error
    }
}
