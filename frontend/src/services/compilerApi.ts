import axios from 'axios';
import { CompileResponse } from '../types/compiler';

const API_URL = 'http://localhost:8000';

export const compileCode = async (sourceCode: string): Promise<CompileResponse> => {
    try {
        const response = await axios.post<CompileResponse>(`${API_URL}/compile`, {
            sourceCode
        });
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            return error.response.data as CompileResponse;
        }
        throw new Error('Network error or server is down');
    }
};
