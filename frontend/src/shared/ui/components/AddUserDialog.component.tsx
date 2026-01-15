import { FC, useState } from 'react'
import { Dialog } from 'primereact/dialog'
import { InputText } from 'primereact/inputtext'
import { Button } from 'primereact/button'
import { createUserRest } from '../../infrastructure/api/userApi'
import { useUserContext } from '../../context/useUserContext'

interface AddUserDialogProps {
    visible: boolean
    onHide: () => void
}

const AddUserDialog: FC<AddUserDialogProps> = ({ visible, onHide }) => {
    const { addUser } = useUserContext()
    const [email, setEmail] = useState('')
    const [name, setName] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const handleSubmit = async () => {
        setError(null)
        setLoading(true)

        try {
            const newUser = await createUserRest({ email, name: name || undefined })
            addUser(newUser)
            setEmail('')
            setName('')
            onHide()
        } catch (err: any) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const handleClose = () => {
        setEmail('')
        setName('')
        setError(null)
        onHide()
    }

    return (
        <Dialog
            visible={visible}
            onHide={handleClose}
            header="Dodaj użytkownika"
            style={{ width: '450px', borderRadius: '20px', overflow: 'hidden' }}
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
                    <label htmlFor="email" style={{ fontWeight: '600', color: '#64748b' }}>
                        Email *
                    </label>
                    <InputText
                        id="email"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="user@example.com"
                        required
                        style={{
                            padding: '0.75rem',
                            borderColor: '#667eea',
                            borderWidth: '2px'
                        }}
                    />
                </div>

                <div className="flex flex-column gap-2">
                    <label htmlFor="name" style={{ fontWeight: '600', color: '#64748b' }}>
                        Imię
                    </label>
                    <InputText
                        id="name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Jan Kowalski"
                        style={{
                            padding: '0.75rem',
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
                        label="Dodaj"
                        icon="pi pi-check"
                        onClick={handleSubmit}
                        disabled={!email || loading}
                        loading={loading}
                        style={{ padding: '0.75rem 1.5rem' }}
                    />
                </div>
            </div>
        </Dialog>
    )
}

export default AddUserDialog
