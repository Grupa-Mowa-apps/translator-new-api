import type {Quote} from "@/shared/types/Quote";

export interface UploadBookParamsDTO {
    file: File;
    quoteType: Quote;
    title: string;
    genre: string;
}

export interface UploadBookResponseDTO {
    message: string;
    book_id: string;
    title: string;
    chapters_count: number;
}

export interface SelectChaptersParamsDTO {
    all?: boolean;
    chapterIds?: string[];
}

export interface SelectChaptersResponseDTO {
    message: string;
}