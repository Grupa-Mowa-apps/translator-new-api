import { createContext, useState, FC, ReactNode, useEffect } from 'react'
import { UserResponseDTO } from '../dto/userDTO'
import { fetchAllUsersRest } from '../infrastructure/api/userApi'

export interface UserState {
    users: UserResponseDTO[]
    selectedUser: UserResponseDTO | null
    setSelectedUser: (user: UserResponseDTO | null) => void
    addUser: (user: UserResponseDTO) => void
    removeUser: (userId: string) => void
    isLoading: boolean
}

export const UserContext = createContext<UserState | undefined>(undefined)

export const UserProvider: FC<{ children: ReactNode }> = ({ children }) => {
    const [users, setUsers] = useState<UserResponseDTO[]>([])
    const [selectedUser, setSelectedUser] = useState<UserResponseDTO | null>(null)
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        fetchAllUsersRest()
            .then(setUsers)
            .catch(console.error)
            .finally(() => setIsLoading(false))
    }, [])

    const addUser = (user: UserResponseDTO) => {
        setUsers((prev) => [...prev, user])
    }

    const removeUser = (userId: string) => {
        setUsers((prev) => prev.filter(u => u.id !== userId))
        if (selectedUser?.id === userId) {
            setSelectedUser(null)
        }
    }

    return (
        <UserContext.Provider value={{ users, selectedUser, setSelectedUser, addUser, removeUser, isLoading }}>
            {children}
        </UserContext.Provider>
    )
}
