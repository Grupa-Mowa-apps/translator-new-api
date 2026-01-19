import { FC, useState } from 'react'
import { Button } from 'primereact/button'
import { Badge } from 'primereact/badge'
import { FileUpload, FileUploadHandlerEvent } from 'primereact/fileupload'
import { mapBookRest, exportParserRest, getAnnotationsRest, downloadAnnotationRest } from '../../infrastructure/api/bookApi'

interface BookCardProps {
    bookId: string
    title: string
    genre: string
    status: string
    quotationMarks: string
    onBookUpdated?: () => void
}

const BookCard: FC<BookCardProps> = ({ bookId, title, genre, status, quotationMarks, onBookUpdated }) => {
    const [loading, setLoading] = useState(false)
    const [translatedFile, setTranslatedFile] = useState<File | null>(null)
    const getStatusColor = (status: string) => {
        switch (status) {
            case 'translated': return 'success'
            case 'in_translation': return 'info'
            case 'ready_to_translate': return 'warning'
            case 'mapped': return 'warning'
            case 'parsed': return 'warning'
            default: return 'secondary'
        }
    }

    const getStatusLabel = (status: string) => {
        switch (status) {
            case 'translated': return 'Przetłumaczona'
            case 'in_translation': return 'W trakcie'
            case 'ready_to_translate': return 'Gotowa'
            case 'uploaded': return 'Wgrana'
            case 'mapped': return 'Czeka na przypisy'
            case 'parsed': return 'Przypisy do tłumaczenia'
            default: return status
        }
    }

    const handleParser = async () => {
        setLoading(true)
        try {
            await mapBookRest(bookId)
            await exportParserRest(bookId, quotationMarks)
            
            if (onBookUpdated) {
                onBookUpdated()
            }
        } catch (err) {
            console.error('Parser error:', err)
        } finally {
            setLoading(false)
        }
    }

    const handleDownloadAnnotations = async () => {
        setLoading(true)
        try {
            const annotations = await getAnnotationsRest(bookId)
            if (annotations.length === 0) {
                console.error('No annotations found')
                return
            }
            
            const latestAnnotation = annotations[0]
            const blob = await downloadAnnotationRest(bookId, latestAnnotation.id)
            
            const url = window.URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `${title}_przypisy.xlsx`
            document.body.appendChild(a)
            a.click()
            window.URL.revokeObjectURL(url)
            document.body.removeChild(a)
        } catch (err) {
            console.error('Download error:', err)
        } finally {
            setLoading(false)
        }
    }

    const handleFileSelect = (event: FileUploadHandlerEvent) => {
        const selectedFile = event.files[0]
        setTranslatedFile(selectedFile)
    }

    const handleApplyTranslations = async () => {
        console.log('Apply translations:', translatedFile)
        // TODO: Implement upload and apply logic
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
                        onClick={handleParser}
                        loading={loading}
                        disabled={loading}
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

            {['mapped', 'parsed'].includes(status) && (
                <div style={{
                    background: 'rgba(102, 126, 234, 0.05)',
                    border: '1px solid #e2e8f0',
                    borderRadius: '12px',
                    padding: '1rem',
                    marginTop: '1rem',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '0.75rem'
                }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                        <i className="pi pi-file-excel" style={{ color: '#667eea', fontSize: '1.25rem' }}></i>
                        <span style={{ fontWeight: '600', color: '#64748b', fontSize: '0.875rem' }}>Sekcja tłumaczeń</span>
                    </div>

                    <Button
                        label="Pobierz przypisy"
                        icon="pi pi-download"
                        severity="info"
                        size="small"
                        onClick={handleDownloadAnnotations}
                        loading={loading}
                        disabled={loading}
                        style={{ width: '100%', padding: '0.5rem 1rem' }}
                    />

                    <div style={{ height: '1px', background: '#e2e8f0', margin: '0.25rem 0' }}></div>

                    <label style={{ fontWeight: '600', color: '#64748b', fontSize: '0.875rem' }}>
                        Wgraj przetłumaczony plik:
                    </label>

                    <FileUpload
                        mode="basic"
                        name="translatedFile"
                        accept=".xlsx"
                        maxFileSize={10000000}
                        customUpload
                        uploadHandler={handleFileSelect}
                        chooseLabel={translatedFile ? translatedFile.name : "Wybierz plik .xlsx"}
                        auto
                        style={{ width: '100%' }}
                        chooseOptions={{
                            style: { padding: '0.5rem 1rem', fontSize: '0.875rem', width: '100%' }
                        }}
                    />

                    <Button
                        label="Zastosuj tłumaczenia"
                        icon="pi pi-check"
                        severity="success"
                        size="small"
                        onClick={handleApplyTranslations}
                        disabled={!translatedFile || loading}
                        loading={loading}
                        style={{ width: '100%', padding: '0.5rem 1rem' }}
                    />
                </div>
            )}
        </div>
    )
}

export default BookCard
