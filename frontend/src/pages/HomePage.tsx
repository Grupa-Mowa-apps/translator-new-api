import { FC } from 'react'
import UserSelector from '../shared/ui/components/UserSelector.component'
import Footer from '../shared/ui/components/Footer.component'

const HomePage: FC = () => {
    return (
        <div className="app-container">
            <div className="app-card">
                <h1>Parse And Translate</h1>
                <p style={{ color: '#64748b', marginBottom: '2rem' }}>
                    Nowoczesna aplikacja do tłumaczeń
                </p>
                <UserSelector />
            </div>
            <Footer />
        </div>
    )
}

export default HomePage
