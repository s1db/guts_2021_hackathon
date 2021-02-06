import Axios from "axios";

export const api = Axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
});
