import { FC } from 'react'
import UserSelector from '../shared/ui/components/UserSelector.component'
import Footer from '../shared/ui/components/Footer.component'

const HomePage: FC = () => {
    return (
        <div className="app-container">
            <div className="app-card">
                <h1>P And Translate</h1>
                <UserSelector />
            </div>
            <Footer />arse
        </div>
    )
}

export default HomePage
