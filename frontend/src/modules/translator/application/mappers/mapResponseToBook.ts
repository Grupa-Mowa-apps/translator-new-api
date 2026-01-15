import {Book} from "@/shared/types/Books";

export function mapResponseToBook(data: any): Book {
    return {
        id: data.id,
        title: data.title,
        genre: data.genre,
        file_path: data.file_path,
        quotation_marks: data.quotation_marks,
        chapters: data.chapters.map((chapter: any) => ({
            id: chapter.id,
            no: chapter.no,
            title: chapter.title,
            book_id: chapter.book_id,
            parent_id: chapter.parent_id,
            content: chapter.content,
            selected_to_translation: chapter.selected_to_translation,
        })),
    };
}
