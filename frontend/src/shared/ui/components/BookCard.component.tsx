import { FC } from 'react'
import { Button } from 'primereact/button'
import { Badge } from 'primereact/badge'

interface BookCardProps {
    title: string
    genre: string
    status: string
}

const BookCard: FC<BookCardProps> = ({ title, genre, status }) => {
    const getStatusColor = (status: string) => {
        switch (status) {
            case 'translated': return 'success'
            case 'in_translation': return 'info'
            case 'ready_to_translate': return 'warning'
            default: return 'secondary'
        }
    }

    const getStatusLabel = (status: string) => {
        switch (status) {
            case 'translated': return 'Przetłumaczona'
            case 'in_translation': return 'W trakcie'
            case 'ready_to_translate': return 'Gotowa'
            case 'uploaded': return 'Wgrana'
            default: return status
        }
    }

    return (
        <div style={{
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            borderRadius: '20px',
            padding: '2rem',
            boxShadow: '0 10px 30px rgba(0, 0, 0, 0.2)',
            transition: 'transform 0.3s ease, box-shadow 0.3s ease',
            cursor: 'pointer',
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem'
        }}
        onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-8px)'
            e.currentTarget.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.3)'
        }}
        onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)'
            e.currentTarget.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.2)'
        }}
        >
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <i className="pi pi-book" style={{ 
                    fontSize: '2.5rem',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text'
                }}></i>
                <div style={{ flex: 1 }}>
                    <h3 style={{ margin: 0, color: '#1f2937', fontSize: '1.25rem' }}>{title}</h3>
                    <p style={{ margin: '0.25rem 0 0 0', color: '#64748b', fontSize: '0.875rem' }}>{genre}</p>
                </div>
            </div>

            <Badge 
                value={getStatusLabel(status)} 
                severity={getStatusColor(status)}
                style={{ alignSelf: 'flex-start', padding: '0.5rem 1rem', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
            />

            <div style={{ display: 'flex', gap: '0.5rem', marginTop: 'auto' }}>
                {status === 'uploaded' && (
                    <Button
                        label="Parser"
                        icon="pi pi-file-edit"
                        severity="secondary"
                        outlined
                        size="small"
                        style={{ flex: 1, padding: '0.5rem 1rem' }}
                    />
                )}
                {['ready_to_translate', 'in_translation', 'translated'].includes(status) && (
                    <>
                        <Button
                            label="Tłumacz"
                            icon="pi pi-language"
                            size="small"
                            style={{ flex: 1, padding: '0.5rem 1rem' }}
                        />
                        <Button
                            label="Parser"
                            icon="pi pi-file-edit"
                            severity="secondary"
                            outlined
                            size="small"
                            style={{ flex: 1, padding: '0.5rem 1rem' }}
                        />
                    </>
                )}
            </div>
        </div>
    )
}

export default BookCard
