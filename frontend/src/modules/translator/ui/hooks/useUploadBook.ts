import React from "react";
import { useState } from "react";
import { errorMessages } from "@/shared/messages/error";
import type { Quote } from "@/shared/types/Quote";
import type {
    UploadBookParamsDTO,
    UploadBookResponseDTO
} from "@/modules/translator/application/dto/translatorRequestDTO";
import {UploadBookResult} from "@/modules/translator/application/type/UploadBookResult";
import {translatorUploadBookHandler} from "@/modules/translator/application/action/handlers";
import {useBooksContext} from "@/shared/context/useBooksContext";

export function useUploadBook(): UploadBookResult {
    const [file, setFile] = useState<File | null>(null);
    const [quoteType, setQuoteType] = useState<Quote>("fr");
    const [title, setTitle] = useState<string>("");
    const [genre, setGenre] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [response, setResponse] = useState<UploadBookResponseDTO | null>(null);

    const { refreshBooks } = useBooksContext();

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (selectedFile) setFile(selectedFile);
    };

    const handleQuoteTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setQuoteType(e.target.value as Quote);
    };

    const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setTitle(e.target.value);
    };

    const handleGenreChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setGenre(e.target.value);
    };

    const handleSubmit = async () => {
        if (!file) {
            setError(errorMessages.fileIsRequired);
            return;
        }

        const params: UploadBookParamsDTO = {
            file,
            quoteType,
            title,
            genre,
        };

        setLoading(true);
        setError(null);
        setResponse(null);

        try {
            const result = await translatorUploadBookHandler(params);
            setResponse(result);
            await refreshBooks();
        } catch (err) {
            setError((err as Error).message);
        } finally {
            setLoading(false);
        }

    };

    return {
        state: {
            file,
            quoteType,
            title,
            genre,
            loading,
            error,
            response,
        },
        actions: {
            handleFileChange,
            handleQuoteTypeChange,
            handleTitleChange,
            handleGenreChange,
            handleSubmit,
        },
    };
}
