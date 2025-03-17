export class ApiError extends Error {
    constructor(message, status) {
        super(message);
        this.status = status;
        this.name = 'ApiError';
    }
}

export const handleError = (error) => {
    if (error instanceof ApiError) {
        alert(`Error (${error.status}): ${error.message}`);
    } else {
        console.error('Unexpected error:', error);
        alert('An unexpected error occurred. Please try again.');
    }
};

export default handleError;
