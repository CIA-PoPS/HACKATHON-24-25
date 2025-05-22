import { fetchGET, fetchPOST } from "./baseApi";
import { User } from "../models/userModels";

export async function registerUser(email: string, nickname: string, password: string): Promise<string> {
    const response: Response = await fetchPOST('', '/users/register', JSON.stringify({ email, nickname, password }));
    if (response.ok) alert('User registered');
    return response.ok ? (await response.json()).token : '';
}

export async function loginUser(email: string, nickname: string, password: string): Promise<string> {
    const response: Response = await fetchPOST('', '/users/login', JSON.stringify({ email, nickname, password }));
    return response.ok ? (await response.json()).token : '';
}

export async function getUser(token: string): Promise<User> {
    const response: Response = await fetchGET(token, '/users/get');
    return new User(response.ok ? await response.json() : {});
}
