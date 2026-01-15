import React from "react"
import { useState } from "react";
import {submitParserRequestMdToExcel} from "@/modules/parser/application/actions/handlers";
import {errorMessages} from "@/shared/messages/error";
import type {Quote} from "@/shared/types/Quote";
import {downloadBlobAsFile} from "@/shared/utils/downloadBlobAsFile";
import {ParserMdToExcelResultDTO} from "@/modules/parser/application/dto/parserMdToExcelResultDTO";
import {UseParserMdToExcelReturn} from "@/modules/parser/application/types/UseParserMdToExcelReturn";

export function useParserMdToExcel(): UseParserMdToExcelReturn  {
    const [file, setFile] = useState<File | null>(null);
    const [quotesType, setQuotesType] = useState<Quote>('fr');
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile: File | undefined = e.target.files?.[0];
        if (selectedFile) setFile(selectedFile);
    };

    const handleQuotesTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setQuotesType(e.target.value as Quote);
    };

    const handleSubmit = async () => {
        if (!file) {
            setError(errorMessages.fileIsRequired);
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const parserMdToExcelResultDTO: ParserMdToExcelResultDTO = await submitParserRequestMdToExcel({file, quotesType});
            downloadBlobAsFile(parserMdToExcelResultDTO.file, "quotes_output.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
        } catch (err) {
            setError((err as Error).message);
        } finally {
            setLoading(false);
        }
    };

    return {
        state: {
            file,
            quotesType,
            loading,
            error,
        },
        actions: {
            handleFileChange,
            handleQuotesTypeChange,
            handleSubmit,
        },
    };
}
