import {Quote} from "@/shared/types/Quote";
import {UploadBookResponseDTO} from "@/modules/translator/application/dto/translatorRequestDTO";

export interface UploadBookResult {
    state: {
        file: File | null;
        quoteType: Quote;
        title: string;
        genre: string;
        loading: boolean;
        error: string | null;
        response: UploadBookResponseDTO | null;
    };
    actions: {
        handleFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
        handleQuoteTypeChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
        handleTitleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
        handleGenreChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
        handleSubmit: () => Promise<void>;
    };
}