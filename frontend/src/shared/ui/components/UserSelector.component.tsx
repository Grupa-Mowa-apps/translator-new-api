import { FC, useState } from 'react'
import { Dropdown, DropdownChangeEvent } from 'primereact/dropdown'
import { Button } from 'primereact/button'
import { useUserContext } from '../../context/useUserContext'
import AddUserDialog from './AddUserDialog.component'
import DeleteUserDialog from './DeleteUserDialog.component'

const UserSelector: FC = () => {
    const { users, selectedUser, setSelectedUser } = useUserContext();
    const [dialogVisible, setDialogVisible] = useState(false)
    const [deleteDialogVisible, setDeleteDialogVisible] = useState(false)

    return (
        <>
            <div className="flex flex-column gap-3 mb-4">
                <label htmlFor="user-dropdown" style={{ fontWeight: '600', color: '#64748b' }}>
                    Wybierz swoje konto (lub dodaj jeśli jeszcze tego nie zrobiłaś/eś):
                </label>
                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                    <Dropdown
                    id="user-dropdown"
                    value={selectedUser}
                    onChange={(e: DropdownChangeEvent) => setSelectedUser(e.value)}
                    options={users}
                    optionLabel="name"
                    placeholder="Wybierz użytkownika"
                    style={{ 
                        flex: 1,
                        padding: '0.5rem',
                        borderColor: '#667eea',
                        borderWidth: '2px'
                    }}
                    panelStyle={{
                        padding: '0.5rem'
                    }}
                    itemTemplate={(option) => (
                        <div style={{ padding: '0.75rem' }}>
                            <div style={{ fontWeight: '600' }}>{option.name}</div>
                            <div style={{ fontSize: '0.875rem', color: '#64748b' }}>{option.email}</div>
                        </div>
                    )}
                    />
                    <Button
                        icon="pi pi-trash"
                        severity="danger"
                        outlined
                        disabled={!selectedUser}
                        onClick={() => setDeleteDialogVisible(true)}
                        style={{ padding: '0.75rem' }}
                        tooltip="Usuń użytkownika"
                        tooltipOptions={{ 
                            position: 'top',
                            className: 'custom-tooltip',
                            style: { 
                                backgroundColor: '#778887',
                                color: 'white',
                                padding: '1rem 0.75rem',
                                borderRadius: '6px',
                                fontSize: '0.875rem'
                            }
                        }}
                    />
                </div>
                <div style={{ display: 'flex', justifyContent: 'center' }}>
                    <Button
                        icon="pi pi-user-plus"
                        label="Dodaj użytkownika"
                        severity="info"
                        style={{ width: '66%', padding: '0.75rem' }}
                        onClick={() => setDialogVisible(true)}
                    />
                </div>
            </div>
            <AddUserDialog visible={dialogVisible} onHide={() => setDialogVisible(false)} />
            <DeleteUserDialog 
                visible={deleteDialogVisible} 
                onHide={() => setDeleteDialogVisible(false)}
                user={selectedUser}
                onConfirm={() => {
                    // TODO: implement delete logic
                    console.log('Delete user:', selectedUser)
                    setDeleteDialogVisible(false)
                }}
            />
        </>
    )
}

export default UserSelector
