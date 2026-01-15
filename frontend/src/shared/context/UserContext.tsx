import { createContext, useState, FC, ReactNode } from 'react'
import { UserResponseDTO } from '../dto/userDTO'

export interface UserState {
    users: UserResponseDTO[]
    selectedUser: UserResponseDTO | null
    setSelectedUser: (user: UserResponseDTO | null) => void
    addUser: (user: UserResponseDTO) => void
}

export const UserContext = createContext<UserState | undefined>(undefined)

export const UserProvider: FC<{ children: ReactNode }> = ({ children }) => {
    const [users, setUsers] = useState<UserResponseDTO[]>([
        { id: '1', email: 'user1@example.com', name: 'User 1' },
        { id: '2', email: 'user2@example.com', name: 'User 2' },
        { id: '3', email: 'user3@example.com', name: 'User 3' }
    ])
    const [selectedUser, setSelectedUser] = useState<UserResponseDTO | null>(null)

    const addUser = (user: UserResponseDTO) => {
        setUsers((prev) => [...prev, user])
    }

    return (
        <UserContext.Provider value={{ users, selectedUser, setSelectedUser, addUser }}>
            {children}
        </UserContext.Provider>
    )
}
