export type Chapter = {
    id: string;
    no: number;
    title: string;
    book_id: string;
    parent_id: string | null;
    content: string[];
    selected_to_translation: boolean;
};

export type Book = {
    id: string;
    title: string;
    genre: string;
    file_path: string;
    quotation_marks: string;
    chapters: Chapter[];
};
