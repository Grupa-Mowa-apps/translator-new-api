export interface UserResponseDTO {
    id: string
    email: string
    name?: string
}

export interface CreateUserRequestDTO {
    email: string
    name?: string
}

export interface UpdateUserRequestDTO {
    email: string
    name?: string
}

export interface ListUsersParamsDTO {
    limit?: number
    offset?: number
    email_like?: string
}
