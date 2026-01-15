import './App.css'
import { FC } from 'react'
import { Button } from 'primereact/button'

const App: FC = () => {
    return (
        <div className="app-container">
            <div className="app-card">
                <h1>Parse And Translate</h1>
                <p style={{ color: '#64748b', marginBottom: '2rem' }}>
                    Nowoczesna aplikacja do tłumaczeń
                </p>
                <Button 
                    label="Rozpocznij" 
                    icon="pi pi-arrow-right" 
                    iconPos="right"
                    size="large"
                />
            </div>
        </div>
    )
}

export default App

