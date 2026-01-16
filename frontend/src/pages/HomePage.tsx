import { FC } from 'react'
import { useNavigate } from 'react-router-dom'
import UserSelector from '../shared/ui/components/UserSelector.component'
import Footer from '../shared/ui/components/Footer.component'
import { useUserContext } from '../shared/context/useUserContext'
import { Button } from 'primereact/button'

const HomePage: FC = () => {
    const { selectedUser } = useUserContext()
    const navigate = useNavigate()

    const handleStart = () => {
        if (selectedUser) {
            navigate(`/user/${selectedUser.id}`)
        }
    }

    return (
        <div className="app-container">
            <div className="app-card">
                <h1>Parse And Translate</h1>
                <UserSelector />
                <Button 
                    label="Rozpocznij" 
                    icon="pi pi-arrow-right" 
                    iconPos="right"
                    size="large"
                    onClick={handleStart}
                    disabled={!selectedUser}
                />
            </div>
            <Footer />
        </div>
    )
}

export default HomePage
