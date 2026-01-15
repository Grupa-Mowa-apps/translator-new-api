import { FC, useState } from 'react'
import { Dropdown, DropdownChangeEvent } from 'primereact/dropdown'
import { Button } from 'primereact/button'

const UserSelector: FC = () => {
    const [selectedUser, setSelectedUser] = useState<string | null>(null)
    const users: string[] = ['User 1', 'User 2', 'User 3']

    return (
        <div className="flex flex-column gap-3 mb-4">
            <label htmlFor="user-dropdown" style={{ fontWeight: '600', color: '#64748b' }}>
                Wybierz swoje konto (lub dodaj jeśli jeszcze tego nie zrobiłaś/eś):
            </label>
            <Dropdown
                id="user-dropdown"
                value={selectedUser}
                onChange={(e: DropdownChangeEvent) => setSelectedUser(e.value)}
                options={users}
                placeholder="Wybierz użytkownika"
                style={{ 
                    width: '100%',
                    padding: '0.5rem',
                    borderColor: '#667eea',
                    borderWidth: '2px'
                }}
                panelStyle={{
                    padding: '0.5rem'
                }}
                itemTemplate={(option) => (
                    <div style={{ padding: '0.75rem' }}>{option}</div>
                )}
            />
            <div style={{ display: 'flex', justifyContent: 'center' }}>
                <Button
                    icon="pi pi-user-plus"
                    label="Dodaj użytkownika"
                    severity="info"
                    style={{ width: '66%', padding: '0.75rem' }}
                />
            </div>
        </div>
    )
}

export default UserSelector
