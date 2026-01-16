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

export const exportParserRest = async (bookId: string, quoteType: string): Promise<{ annotation_set_id: string }> => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/books/${bookId}/parser/export`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ quote_type: quoteType })
    })
    
    if (!response.ok) {
        throw new Error('Nie udało się wyeksportować przypisów')
    }
    
    return response.json()
}

export const getAnnotationsRest = async (bookId: string): Promise<any[]> => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/books/${bookId}/annotations`)
    
    if (!response.ok) {
        throw new Error('Nie udało się pobrać adnotacji')
    }
    
    return response.json()
}

export const downloadAnnotationRest = async (bookId: string, annotationSetId: string): Promise<Blob> => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/books/${bookId}/annotations/${annotationSetId}/download`)
    
    if (!response.ok) {
        throw new Error('Nie udało się pobrać pliku')
    }
    
    return response.blob()
}
