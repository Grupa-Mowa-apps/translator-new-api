import { useContext } from 'react'
import { UserContext, UserState } from './UserContext'

export const useUserContext = (): UserState => {
    const context = useContext(UserContext)
    if (!context) {
        throw new Error('useUserContext must be used within <UserProvider>')
    }
    return context
}
