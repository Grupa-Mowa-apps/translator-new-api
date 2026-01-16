import { FC } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from 'primereact/button'

interface DashboardHeaderProps {
    userName: string
    userEmail: string
}

const DashboardHeader: FC<DashboardHeaderProps> = ({ userName, userEmail }) => {
    const navigate = useNavigate()

    return (
        <div style={{
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            padding: '1.5rem 2rem',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)'
        }}>
            <div>
                <h2 style={{ 
                    margin: 0, 
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text'
                }}>
                    {userName}
                </h2>
                <p style={{ margin: '0.25rem 0 0 0', color: '#64748b', fontSize: '0.875rem' }}>
                    {userEmail}
                </p>
            </div>
            <Button
                label="Zmień użytkownika"
                icon="pi pi-user"
                outlined
                onClick={() => navigate('/')}
                style={{ borderColor: '#667eea', color: '#667eea', padding: '0.75rem 1.5rem', gap: '1rem' }}
            />
        </div>
    )
}

export default DashboardHeader
