import { BookResponseDTO } from '../dto/bookDTO'

export const getUserBooksRest = async (userId: string): Promise<BookResponseDTO[]> => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/books?owner_id=${userId}`)
    
    if (!response.ok) {
        throw new Error('Nie udało się pobrać książek')
    }
    
    return response.json()
}

export const mapBookRest = async (bookId: string): Promise<BookResponseDTO> => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/books/${bookId}/map`, {
        method: 'POST'
    })
    
    if (!response.ok) {
        throw new Error('Nie udało się zmapować książki')
    }
    
    return response.json()
}

export const exportParserRest = async (bookId: string, quoteType: string): Promise<Blob> => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/books/${bookId}/parser/export-download`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ quote_type: quoteType })
    })
    
    if (!response.ok) {
        throw new Error('Nie udało się wyeksportować przypisów')
    }
    
    return response.blob()
}
