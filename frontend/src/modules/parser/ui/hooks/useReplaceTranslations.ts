import { useState } from "react";
import { errorMessages } from "@/shared/messages/error";
import {submitParserRequestReplaceTranslations} from "@/modules/parser/application/actions/handlers";
import {ReplaceTranslationsResultDTO} from "@/modules/parser/application/dto/replaceTranslationsResultDTO";
import {downloadBlobAsFile} from "@/shared/utils/downloadBlobAsFile";
import {UseReplaceTranslationsReturn} from "@/modules/parser/application/types/UseReplaceTranslationsReturn";

export function useReplaceTranslations(): UseReplaceTranslationsReturn {
    const [excelFile, setExcelFile] = useState<File | null>(null);
    const [mdFile, setMdFile] = useState<File | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const handleExcelFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (selectedFile) setExcelFile(selectedFile);
    };

    const handleMdFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (selectedFile) setMdFile(selectedFile);
    };

    const handleSubmit = async () => {
        if (!excelFile || !mdFile) {
            setError(errorMessages.fileIsRequired);
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const replaceTranslationsResultDTO: ReplaceTranslationsResultDTO = await submitParserRequestReplaceTranslations({
                excelFile,
                mdFile,
            });
            downloadBlobAsFile(replaceTranslationsResultDTO.file, "quotes_output.md", "text/markdown");
        } catch (err) {
            setError((err as Error).message);
        } finally {
            setLoading(false);
        }
    };

    return {
        state: {
            excelFile,
            mdFile,
            loading,
            error,
        },
        actions: {
            handleExcelFileChange,
            handleMdFileChange,
            handleSubmit,
        },
    };
}
