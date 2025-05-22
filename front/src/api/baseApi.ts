import { backURL } from '../script/Values';

export async function fetchGET(token: string, routes: string): Promise<Response> {
    const response = await fetch(backURL + routes, {
        method: 'GET',
        headers: { 'Authorization': token }
    });

    if (!response?.ok) {
        alert((await response?.json()).error);
    }

    return response || new Response();
}

export async function fetchPOST(token: string, routes: string, body: string): Promise<Response> {
    const response = await fetch( backURL + routes, {
        method: 'POST',
        headers: { 'Authorization': token, 'Content-Type': 'application/json' },
        body: body
    });

    if (!response.ok) {
        alert((await response.json()).error);
    }

    return response;
}
