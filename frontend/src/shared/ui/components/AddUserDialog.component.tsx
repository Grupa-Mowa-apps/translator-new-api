import { FC, useState, useRef, useEffect } from 'react'
import { Dialog } from 'primereact/dialog'
import { InputText } from 'primereact/inputtext'
import { Button } from 'primereact/button'
import { Toast } from 'primereact/toast'
import { createUserRest, updateUserRest } from '../../infrastructure/api/userApi'
import { useUserContext } from '../../context/useUserContext'
import { UserResponseDTO } from '../../dto/userDTO'

interface AddUserDialogProps {
    visible: boolean
    onHide: () => void
    user?: UserResponseDTO | null
    mode?: 'add' | 'edit'
}

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const MAX_NAME_LENGTH = 100

const AddUserDialog: FC<AddUserDialogProps> = ({ visible, onHide, user, mode = 'add' }) => {
    const { addUser, updateUser } = useUserContext()
    const toast = useRef<Toast>(null)
    const [email, setEmail] = useState(user?.email || '')
    const [name, setName] = useState(user?.name || '')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [emailError, setEmailError] = useState<string | null>(null)
    const [nameError, setNameError] = useState<string | null>(null)

    const isEditMode = mode === 'edit'

    useEffect(() => {
        if (visible && user) {
            setEmail(user.email)
            setName(user.name || '')
        } else if (visible && !user) {
            setEmail('')
            setName('')
        }
    }, [visible, user, mode])

    const validateEmail = (value: string): boolean => {
        if (!value.trim()) {
            setEmailError('Email jest wymagany')
            return false
        }
        if (!EMAIL_REGEX.test(value)) {
            setEmailError('Nieprawid\u0142owy format email')
            return false
        }
        setEmailError(null)
        return true
    }

    const validateName = (value: string): boolean => {
        if (value && value.length > MAX_NAME_LENGTH) {
            setNameError(`Imi\u0119 nie mo\u017ce przekracza\u0107 ${MAX_NAME_LENGTH} znak\u00f3w`)
            return false
        }
        setNameError(null)
        return true
    }

    const handleSubmit = async () => {
        const isEmailValid = validateEmail(email)
        const isNameValid = validateName(name)

        if (!isEmailValid || !isNameValid) {
            return
        }

        setError(null)
        setLoading(true)

        try {
            const trimmedEmail = email.trim()
            const trimmedName = name.trim()
            
            if (isEditMode && user) {
                const updatedUser = await updateUserRest(user.id, { 
                    email: trimmedEmail, 
                    name: trimmedName || undefined 
                })
                updateUser(updatedUser)
                toast.current?.show({
                    severity: 'success',
                    summary: 'Sukces',
                    detail: 'U\u017cytkownik zosta\u0142 zaktualizowany',
                    life: 3000
                })
            } else {
                const newUser = await createUserRest({ 
                    email: trimmedEmail, 
                    name: trimmedName || undefined 
                })
                addUser(newUser)
                toast.current?.show({
                    severity: 'success',
                    summary: 'Sukces',
                    detail: 'U\u017cytkownik zosta\u0142 dodany',
                    life: 3000
                })
            }
            setEmail('')
            setName('')
            setEmailError(null)
            setNameError(null)
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
        setEmailError(null)
        setNameError(null)
        onHide()
    }

    return (
        <>
            <Toast ref={toast} />
            <Dialog
                visible={visible}
                onHide={handleClose}
                header={isEditMode ? "Edytuj użytkownika" : "Dodaj użytkownika"}
                style={{ width: '450px', borderRadius: '20px', overflow: 'hidden' }}
                contentStyle={{ padding: '2rem' }}
                headerStyle={{ 
                    background: isEditMode 
                        ? 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
                        : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
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
                        onBlur={() => validateEmail(email)}
                        placeholder="user@example.com"
                        required
                        style={{
                            padding: '0.75rem',
                            borderColor: emailError ? '#ef4444' : '#667eea',
                            borderWidth: '2px'
                        }}
                    />
                    {emailError && (
                        <small style={{ color: '#ef4444' }}>{emailError}</small>
                    )}
                </div>

                <div className="flex flex-column gap-2">
                    <label htmlFor="name" style={{ fontWeight: '600', color: '#64748b' }}>
                        Imię
                    </label>
                    <InputText
                        id="name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        onBlur={() => validateName(name)}
                        placeholder="Jan Kowalski"
                        maxLength={MAX_NAME_LENGTH}
                        style={{
                            padding: '0.75rem',
                            borderColor: nameError ? '#ef4444' : '#667eea',
                            borderWidth: '2px'
                        }}
                    />
                    {nameError && (
                        <small style={{ color: '#ef4444' }}>{nameError}</small>
                    )}
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
                        label={isEditMode ? "Zapisz" : "Dodaj"}
                        icon={isEditMode ? "pi pi-check" : "pi pi-check"}
                        onClick={handleSubmit}
                        disabled={!email || loading}
                        loading={loading}
                        style={{ padding: '0.75rem 1.5rem' }}
                    />
                </div>
            </div>
        </Dialog>
        </>
    )
}

export default AddUserDialog
