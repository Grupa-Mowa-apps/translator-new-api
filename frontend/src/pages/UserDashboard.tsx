import { FC, useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { useUserContext } from '../shared/context/useUserContext'
import DashboardHeader from '../shared/ui/components/DashboardHeader.component'
import BookCard from '../shared/ui/components/BookCard.component'
import AddBookDialog from '../shared/ui/components/AddBookDialog.component'
import Footer from '../shared/ui/components/Footer.component'
import { Button } from 'primereact/button'
import { BookResponseDTO } from '../shared/dto/bookDTO'
import { getUserBooksRest } from '../shared/infrastructure/api/bookApi'

const UserDashboard: FC = () => {
    const { userId } = useParams<{ userId: string }>()
    const { users } = useUserContext()
    const [addBookVisible, setAddBookVisible] = useState(false)
    const [books, setBooks] = useState<BookResponseDTO[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    
    const user = users.find(u => u.id === userId)

    const fetchBooks = async () => {
        if (!userId) return
        
        setLoading(true)
        setError(null)
        try {
            const data = await getUserBooksRest(userId)
            setBooks(data)
        } catch (err) {
            setError('Nie udało się pobrać książek')
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchBooks()
    }, [userId])

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
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                    <h2 style={{ color: 'white', margin: 0 }}>Moje książki</h2>
                    <Button
                        label="Dodaj książkę"
                        icon="pi pi-plus"
                        onClick={() => setAddBookVisible(true)}
                        style={{ padding: '0.75rem 1.5rem', gap: '1rem' }}
                    />
                </div>
                
                {loading && (
                    <div style={{ color: 'white', textAlign: 'center', padding: '2rem' }}>
                        Ładowanie książek...
                    </div>
                )}

                {error && (
                    <div style={{ color: '#fee2e2', textAlign: 'center', padding: '2rem' }}>
                        {error}
                    </div>
                )}

                {!loading && !error && books.length === 0 && (
                    <div style={{ color: 'white', textAlign: 'center', padding: '2rem' }}>
                        Nie masz jeszcze żadnych książek. Dodaj pierwszą!
                    </div>
                )}

                {!loading && !error && books.length > 0 && (
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
                        gap: '2rem'
                    }}>
                        {books.map(book => (
                            <BookCard
                                key={book.id}
                                bookId={book.id}
                                title={book.title}
                                genre={book.genre}
                                status={book.status}
                                quotationMarks={book.quotation_marks}
                                ownerId={userId || ''}
                                onBookUpdated={fetchBooks}
                            />
                        ))}
                    </div>
                )}
            </div>
            
            <AddBookDialog 
                visible={addBookVisible} 
                onHide={() => setAddBookVisible(false)}
                userId={userId || ''}
                onBookAdded={fetchBooks}
            />
            
            <Footer />
        </div>
    )
}

export default UserDashboard
