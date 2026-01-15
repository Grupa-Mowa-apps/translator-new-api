import { useState } from "react";
import { translatorGetBookHandler } from "@/modules/translator/application/action/handlers";
import { errorMessages } from "@/shared/messages/error";
import {Book} from "@/shared/types/Books";

export function useSimpleBook() {
    const [bookId, setBookId] = useState("");
    const [book, setBook] = useState<Book | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchBook = async () => {
        if (!bookId) {
            setError(errorMessages.addBookId);
            return;
        }

        setLoading(true);
        setError(null);
        setBook(null);

        try {
            const data = await translatorGetBookHandler(bookId);
            setBook(data);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return {
        bookId,
        setBookId,
        fetchBook,
        book,
        loading,
        error,
    };
}
