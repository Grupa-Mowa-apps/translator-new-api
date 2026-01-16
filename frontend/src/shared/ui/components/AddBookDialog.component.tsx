import { FC, useState } from 'react'
import { Dialog } from 'primereact/dialog'
import { InputText } from 'primereact/inputtext'
import { Dropdown } from 'primereact/dropdown'
import { FileUpload, FileUploadHandlerEvent } from 'primereact/fileupload'
import { Button } from 'primereact/button'

interface AddBookDialogProps {
    visible: boolean
    onHide: () => void
    userId: string
}

const AddBookDialog: FC<AddBookDialogProps> = ({ visible, onHide, userId }) => {
    const [title, setTitle] = useState('')
    const [genre, setGenre] = useState('')
    const [quotationType, setQuotationType] = useState<string>('french')
    const [file, setFile] = useState<File | null>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const quotationTypes = [
        { label: 'Podwójne (")', value: 'double' },
        { label: 'Pojedyncze (\')', value: 'single' },
        { label: 'Francuskie («»)', value: 'french' },
        { label: 'Niemieckie („")', value: 'german' }
    ]

    const handleFileSelect = (event: FileUploadHandlerEvent) => {
        const selectedFile = event.files[0]
        setFile(selectedFile)
        setError(null)
    }

    const handleSubmit = async () => {
        if (!file || !title || !genre || !quotationType) {
            setError('Wszystkie pola są wymagane')
            return
        }

        setLoading(true)
        // TODO: Logika uploadu
        console.log({ file, title, genre, quotationType, userId })
        
        setTimeout(() => {
            setLoading(false)
            handleClose()
        }, 1000)
    }

    const handleClose = () => {
        setTitle('')
        setGenre('')
        setQuotationType('')
        setFile(null)
        setError(null)
        onHide()
    }

    return (
        <Dialog
            visible={visible}
            onHide={handleClose}
            header="Dodaj książkę"
            style={{ width: '550px', borderRadius: '20px', overflow: 'hidden' }}
            contentStyle={{ padding: '2rem' }}
            headerStyle={{ 
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                padding: '1.5rem',
                borderRadius: '20px 20px 0 0'
            }}
        >
            <div className="flex flex-column gap-4">
                <div className="flex flex-column gap-2">
                    <label htmlFor="file" style={{ fontWeight: '600', color: '#64748b' }}>
                        Plik książki (.md) *
                    </label>
                    <FileUpload
                        mode="basic"
                        name="file"
                        accept=".md"
                        maxFileSize={10000000}
                        customUpload
                        uploadHandler={handleFileSelect}
                        chooseLabel={file ? file.name : "Wybierz plik"}
                        auto
                        style={{ width: '100%' }}
                        chooseOptions={{
                            style: { padding: '0.75rem 1.5rem', gap: '0.5rem' }
                        }}
                    />
                </div>

                <div className="flex flex-column gap-2">
                    <label htmlFor="title" style={{ fontWeight: '600', color: '#64748b' }}>
                        Tytuł książki *
                    </label>
                    <InputText
                        id="title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        placeholder="Harry Potter"
                        style={{
                            padding: '0.75rem',
                            borderColor: '#667eea',
                            borderWidth: '2px'
                        }}
                    />
                </div>

                <div className="flex flex-column gap-2">
                    <label htmlFor="genre" style={{ fontWeight: '600', color: '#64748b' }}>
                        Gatunek *
                    </label>
                    <InputText
                        id="genre"
                        value={genre}
                        onChange={(e) => setGenre(e.target.value)}
                        placeholder="Fantasy"
                        style={{
                            padding: '0.75rem',
                            borderColor: '#667eea',
                            borderWidth: '2px'
                        }}
                    />
                </div>

                <div className="flex flex-column gap-2">
                    <label htmlFor="quotation" style={{ fontWeight: '600', color: '#64748b' }}>
                        Typ cudzysłowów *
                    </label>
                    <Dropdown
                        id="quotation"
                        value={quotationType}
                        onChange={(e) => setQuotationType(e.value)}
                        options={quotationTypes}
                        placeholder="Wybierz typ"
                        style={{
                            width: '100%',
                            padding: '0.5rem',
                            borderColor: '#667eea',
                            borderWidth: '2px'
                        }}
                    />
                </div>

                {error && (
                    <div style={{ 
                        color: '#ef4444', 
                        fontSize: '0.875rem',
                        padding: '0.75rem',
                        background: '#fee2e2',
                        borderRadius: '8px'
                    }}>
                        {error}
                    </div>
                )}

                <div className="flex gap-2 justify-content-end mt-2">
                    <Button
                        label="Anuluj"
                        severity="secondary"
                        outlined
                        onClick={handleClose}
                        disabled={loading}
                        style={{ padding: '0.75rem 1.5rem' }}
                    />
                    <Button
                        label="Dodaj książkę"
                        icon="pi pi-check"
                        onClick={handleSubmit}
                        disabled={loading}
                        loading={loading}
                        style={{ padding: '0.75rem 1.5rem', gap: '0.5rem' }}
                    />
                </div>
            </div>
        </Dialog>
    )
}

export default AddBookDialog
