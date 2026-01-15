import { FC } from 'react'

const Footer: FC = () => {
    return (
        <div style={{ 
            position: 'fixed', 
            bottom: '1rem', 
            width: '100%', 
            textAlign: 'center',
            fontSize: '12px',
            color: 'white'
        }}>
            © Grupa Mowa 2026
        </div>
    )
}

export default Footer
