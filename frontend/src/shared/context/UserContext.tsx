import { createContext, useState, FC, ReactNode } from 'react'

export interface UserState {
    users: string[]
    selectedUser: string | null
    setSelectedUser: (user: string | null) => void
    addUser: (user: string) => void
}

export const UserContext = createContext<UserState | undefined>(undefined)

export const UserProvider: FC<{ children: ReactNode }> = ({ children }) => {
    const [users, setUsers] = useState<string[]>(['User 1', 'User 2', 'User 3'])
    const [selectedUser, setSelectedUser] = useState<string | null>(null)

    const addUser = (user: string) => {
        setUsers((prev) => [...prev, user])
    }

    return (
        <UserContext.Provider value={{ users, selectedUser, setSelectedUser, addUser }}>
            {children}
        </UserContext.Provider>
    )
}
