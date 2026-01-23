import { FC, useRef } from 'react'
import { Dialog } from 'primereact/dialog'
import { Button } from 'primereact/button'
import { Toast } from 'primereact/toast'
import { UserResponseDTO } from '../../dto/userDTO'
import styles from './DeleteUserDialog.module.css'

interface DeleteUserDialogProps {
    visible: boolean
    onHide: () => void
    user: UserResponseDTO | null
    onConfirm: () => void
    loading?: boolean
}

const DeleteUserDialog: FC<DeleteUserDialogProps> = ({ visible, onHide, user, onConfirm, loading = false }) => {
    const toast = useRef<Toast>(null)
    return (
        <>
            <Toast
                ref={toast}
                className={styles.toastTopRight}
                appendTo={document.body}
            />
            <Dialog
            visible={visible}
            onHide={onHide}
            header="Usuń użytkownika"
            style={{ width: '450px', borderRadius: '20px', overflow: 'hidden' }}
            contentStyle={{ padding: '2rem' }}
            headerStyle={{ 
                background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
                color: 'white',
                padding: '1.5rem',
                borderRadius: '20px 20px 0 0'
            }}
        >
            <div className="flex flex-column gap-4">
                <div style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: '1rem',
                    padding: '1rem',
                    background: '#fef2f2',
                    borderRadius: '8px',
                    border: '2px solid #fecaca'
                }}>
                    <i className="pi pi-exclamation-triangle" style={{ fontSize: '2rem', color: '#ef4444' }}></i>
                    <div>
                        <p style={{ margin: 0, fontWeight: '600', color: '#1f2937' }}>
                            Czy na pewno chcesz usunąć użytkownika?
                        </p>
                        {user && (
                            <div style={{ marginTop: '0.5rem', color: '#64748b' }}>
                                <div style={{ fontWeight: '600' }}>{user.name}</div>
                                <div style={{ fontSize: '0.875rem' }}>{user.email}</div>
                            </div>
                        )}
                    </div>
                </div>

                <p style={{ color: '#64748b', fontSize: '0.875rem', margin: 0 }}>
                    Ta operacja jest nieodwracalna. Wszystkie dane powiązane z tym użytkownikiem zostaną usunięte.
                </p>

                <div className="flex gap-2 justify-content-end mt-2">
                    <Button
                        label="Anuluj"
                        severity="secondary"
                        outlined
                        onClick={onHide}
                        disabled={loading}
                        style={{ padding: '0.75rem 1.5rem' }}
                    />
                    <Button
                        label="Usuń"
                        icon="pi pi-trash"
                        severity="danger"
                        onClick={onConfirm}
                        disabled={loading}
                        loading={loading}
                        style={{ padding: '0.75rem 1.5rem' }}
                    />
                </div>
            </div>
        </Dialog>
        </>
    )
}

export default DeleteUserDialog
