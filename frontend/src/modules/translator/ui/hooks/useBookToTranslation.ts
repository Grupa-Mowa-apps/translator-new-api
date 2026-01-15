import { useEffect, useMemo, useState } from "react";
import { Book, Chapter } from "@/shared/types/Books";
import {
    translatorGetBookHandler,
    translatorSelectChaptersHandler
} from "@/modules/translator/application/action/handlers";
import { errorMessages } from "@/shared/messages/error";
import { MultiDropdownOption } from "@/shared/ui/components/MultiSelectDropdown.component";
import {SelectChaptersResponseDTO} from "@/modules/translator/application/dto/translatorRequestDTO";

export function useBookToTranslation() {
    const [bookId, setBookId] = useState<string>("");
    const [error, setError] = useState<string | null>(null);
    const [book, setBook] = useState<Book | null>(null);
    const [loading, setLoading] = useState(false);
    const [selectedChapters, setSelectedChapters] = useState<Chapter[]>([]);
    const [selectedChaptersResponse, setSelectedChaptersResponse] = useState<SelectChaptersResponseDTO | null>(null);
    const [areChaptersSelectedAnConfirmed, setAreChaptersSelectedAnConfirmed] = useState<boolean>(false);

    const [excelFile, setExcelFile] = useState<File | null>(null);

    useEffect(() => {
        if (!bookId) {
            setBook(null);
            setSelectedChapters([]);
            return;
        }

        const fetchBook = async () => {
            setLoading(true);
            setError(null);
            setBook(null);
            setSelectedChapters([]);

            try {
                const data = await translatorGetBookHandler(bookId);
                setBook(data);
            } catch (err: any) {
                setError(err.message || errorMessages.addBookId);
            } finally {
                setLoading(false);
            }
        };

        fetchBook();
    }, [bookId]);

    const chapterOptions: MultiDropdownOption[] = useMemo(() => {
        if (!book) return [];
        return book.chapters.map((chapter: Chapter) => ({
            label: `${chapter.no}. ${chapter.title}`,
            value: chapter.id,
        }));
    }, [book]);

    const selectedChapterOptions: MultiDropdownOption[] = useMemo(() => {
        return selectedChapters.map((ch) => ({
            label: `${ch.no}. ${ch.title}`,
            value: ch.id,
        }));
    }, [selectedChapters]);

    const handleChapterSelection = (selectedOptions: MultiDropdownOption[]) => {
        if (!book) return;
        const selected = book.chapters.filter((ch) =>
            selectedOptions.some((opt) => opt.value === ch.id)
        );
        setSelectedChapters(selected);
    };

    const handleSubmitOnChaptersSelected = async () => {
        if (!bookId || selectedChapters.length === 0) {
            setError(errorMessages.noChaptersSelected);
            return;
        }

        setLoading(true);
        setError(null);
        setSelectedChaptersResponse(null);

        try {
            const dto = {
                all: false,
                chapterIds: selectedChapters.map((ch) => ch.id),
            };

            const res = await translatorSelectChaptersHandler(bookId, dto);
            setSelectedChaptersResponse(res);
            setAreChaptersSelectedAnConfirmed(true);
        } catch (err: any) {
            setError(err.message || errorMessages.submitFailed);
        } finally {
            setLoading(false);
        }
    };

    return {
        bookId,
        setBookId,
        book,
        error,
        loading,
        chapterOptions,
        selectedChapterOptions,
        handleChapterSelection,
        handleSubmitOnChaptersSelected,
        selectedChaptersResponse,
        excelFile,
        setExcelFile,
        selectedChapters,
        setSelectedChapters,
        setAreChaptersSelectedAnConfirmed,
        areChaptersSelectedAnConfirmed
    };
}