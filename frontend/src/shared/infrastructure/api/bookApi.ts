import { BookResponseDTO } from '../dto/bookDTO'

export const getUserBooksRest = async (userId: string): Promise<BookResponseDTO[]> => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/books?owner_id=${userId}`)
    
    if (!response.ok) {
        throw new Error('Nie udało się pobrać książek')
    }
    
    return response.json()
}
