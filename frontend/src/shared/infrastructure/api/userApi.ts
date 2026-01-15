import { CreateUserRequestDTO, UserResponseDTO } from '../../dto/userDTO'
import { env } from '../../config/apiConfig'
import { errorMessages } from '../../messages/error'
import { handleApiError } from './apiErrorHandler'

export async function createUserRest(data: CreateUserRequestDTO): Promise<UserResponseDTO> {
    try {
        const res = await fetch(`${env.apiUrl}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })

        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}))
            const error = {
                response: {
                    status: res.status,
                    data: errorData,
                },
            }
            handleApiError(error, errorMessages.createUserFailed)
        }

        const user: UserResponseDTO = await res.json()
        return user
    } catch (error: any) {
        if (error.message === errorMessages.userAlreadyExists) {
            throw error
        }
        throw new Error(errorMessages.createUserFailed)
    }
}
