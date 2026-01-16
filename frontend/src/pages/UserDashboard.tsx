import { FC } from 'react'
import { useParams } from 'react-router-dom'
import { useUserContext } from '../shared/context/useUserContext'
import DashboardHeader from '../shared/ui/components/DashboardHeader.component'
import BookCard from '../shared/ui/components/BookCard.component'
import Footer from '../shared/ui/components/Footer.component'

const UserDashboard: FC = () => {
    const { userId } = useParams<{ userId: string }>()
    const { users } = useUserContext()
    
    const user = users.find(u => u.id === userId)

    // Mock books data
    const mockBooks = [
        { id: '1', title: 'Harry Potter', genre: 'Fantasy', status: 'translated' },
        { id: '2', title: 'Lord of the Rings', genre: 'Fantasy', status: 'in_translation' },
        { id: '3', title: 'The Hobbit', genre: 'Adventure', status: 'ready_to_translate' },
    ]

    if (!user) {
        return <div style={{ padding: '2rem', color: 'white' }}>Użytkownik nie znaleziony</div>
    }

    return (
        <div style={{ 
            minHeight: '100vh', 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            paddingBottom: '4rem'
        }}>
            <DashboardHeader userName={user.name || 'User'} userEmail={user.email} />
            
            <div style={{ padding: '2rem', maxWidth: '1400px', margin: '0 auto' }}>
                <h2 style={{ color: 'white', marginBottom: '2rem' }}>Moje książki</h2>
                
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                    gap: '2rem'
                }}>
                    {mockBooks.map(book => (
                        <BookCard
                            key={book.id}
                            title={book.title}
                            genre={book.genre}
                            status={book.status}
                        />
                    ))}
                </div>
            </div>
            
            <Footer />
        </div>
    )
}

export default UserDashboard
