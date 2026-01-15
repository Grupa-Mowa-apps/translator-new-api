import { errorMessages } from '../../messages/error'

export const handleApiError = (error: any, defaultMsg: string): never => {
    if (error.response?.status === 409) {
        throw new Error(errorMessages.userAlreadyExists)
    }
    if (error.response?.status === 404) {
        throw new Error(errorMessages.userNotFound)
    }
    const detail = error.response?.data?.detail
    throw new Error(detail || defaultMsg)
}
