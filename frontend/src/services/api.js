import config from '../modules/config/config';
import { ApiError } from '../modules/error/errorHandler';

export class ApiResponseError extends Error {
    constructor(message, data) {
        super(message);
        this.name = 'ApiResponseError';
        this.data = data;
    }
}

export async function calculateRoute(parcelData) {
    try {
        const response = await fetch(`${config.api.baseUrl}${config.api.endpoints.route}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ...parcelData,
                category: 'standard'  // Add default category
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new ApiResponseError(errorData.message || 'Failed to calculate route', errorData);
        }

        return response.json();
    } catch (error) {
        if (error instanceof ApiResponseError) {
            throw error;
        }
        throw new ApiResponseError('Network error', { status: 500 });
    }
}
