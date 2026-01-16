import './App.css'
import { FC } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { UserProvider } from './shared/context/UserContext'
import HomePage from './pages/HomePage'
import UserDashboard from './pages/UserDashboard'

const App: FC = () => {
    return (
        <BrowserRouter>
            <UserProvider>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/user/:userId" element={<UserDashboard />} />
                </Routes>
            </UserProvider>
        </BrowserRouter>
    )
}

export default App

