import './App.css'
import { FC } from 'react'
import { UserProvider } from './shared/context/UserContext'
import HomePage from './pages/HomePage'

const App: FC = () => {
    return (
        <UserProvider>
            <HomePage />
        </UserProvider>
    )
}

export default App

