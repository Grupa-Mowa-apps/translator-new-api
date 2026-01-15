import React, { createContext, useState, useEffect } from "react";
import {BookSummaryDTO} from "@/shared/dto/bookSummaryDTO";
import {getBooksSummaryRest} from "@/shared/infrastructure/api/bookQueryApi";
import {errorMessages} from "@/shared/messages/error";

export interface TranslationProgress {
    [taskId: string]: {
        progress: number;
        message: string;
    };
}

export interface GlobalState {
    books: BookSummaryDTO[];
    refreshBooks: () => Promise<void>;
    translationProgress: TranslationProgress;
    updateTranslationProgress: (taskId: string, data: { progress: number; message: string }) => void;
    isTranslationOngoing: boolean;
    setIsTranslationOngoing: (value: boolean) => void;
}

export const GlobalContext = createContext<GlobalState | undefined>(undefined);

export const GlobalProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [books, setBooks] = useState<BookSummaryDTO[]>([]);
    const [translationProgress, setTranslationProgress] = useState<TranslationProgress>({});
    const [isTranslationOngoing, setIsTranslationOngoing] = useState<boolean>(false);

    const refreshBooks = async () => {
        try {
            const data: BookSummaryDTO[] = await getBooksSummaryRest();
            setBooks(data);
        } catch (err) {
            console.error(errorMessages.errorMsg, err);
        }
    };

    const updateTranslationProgress = (taskId: string, data: { progress: number; message: string }) => {
        setTranslationProgress((prev) => ({
            ...prev,
            [taskId]: data,
        }));
    };

    useEffect(() => {
        refreshBooks();
    }, []);

    return (
        <GlobalContext.Provider value={{ books, refreshBooks, translationProgress, updateTranslationProgress, isTranslationOngoing, setIsTranslationOngoing }}>
            {children}
        </GlobalContext.Provider>
    );
};
