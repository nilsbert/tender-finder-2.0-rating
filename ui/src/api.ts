import axios from 'axios';

// The new orchestrator uses /ms/rating/ as base path for the UI.
// API calls should be relative to that or stick to the /api prefix.
const API_URL = 'api';

export interface Keyword {
    id: string
    term: string
    weight: number
    type: string // "Service" | "Sector" | "Exclusion"
    sub_type?: string
    sub_category?: string
    category?: string 
    created_at: string;
}

export interface KeywordCreate {
    term: string
    weight: number
    type: string
    sub_type?: string
    sub_category?: string
    category?: string
}

export const api = {
    getKeywords: async () => {
        const response = await axios.get<Keyword[]>(`${API_URL}/keywords`);
        return response.data;
    },
    createKeyword: async (keyword: KeywordCreate) => {
        const response = await axios.post<Keyword>(`${API_URL}/keywords`, keyword);
        return response.data;
    },
    updateKeyword: async (id: string, keyword: KeywordCreate) => {
        const response = await axios.put<Keyword>(`${API_URL}/keywords/${id}`, keyword);
        return response.data;
    },
    deleteKeyword: async (id: string) => {
        await axios.delete(`${API_URL}/keywords/${id}`);
    },
    getCategories: async () => {
        const response = await axios.get<string[]>(`${API_URL}/keywords/categories`);
        return response.data;
    },
    getKeywordTree: async () => {
        const response = await axios.get<Record<string, string[]>>(`${API_URL}/keywords/tree`);
        return response.data;
    },
    exportKeywords: () => {
        const link = document.createElement('a');
        link.href = `${API_URL}/keywords/export`;
        link.download = 'rating_keywords.yaml';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    },
    importKeywords: async (file: File, dryRun: boolean, deleteMissing: boolean) => {
        const formData = new FormData();
        formData.append('file', file);
        const params = new URLSearchParams();
        params.append('dry_run', dryRun.toString());
        params.append('delete_missing', deleteMissing.toString());

        const response = await axios.post(`${API_URL}/keywords/import?${params.toString()}`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        return response.data;
    }
};
