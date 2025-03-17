import config from '../modules/config/config';
import { ApiError } from '../modules/error/errorHandler';

export async function calculateRoute(parcelData) {
    try {
        const response = await fetch(`${config.api.baseUrl}${config.api.endpoints.route}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(parcelData)
        });

        if (!response.ok) {
            throw new ApiError('Failed to calculate route', response.status);
        }

        return response.json();
    } catch (error) {
        if (error instanceof ApiError) {
            throw error;
        }
        throw new ApiError('Network error', 500);
    }
}
