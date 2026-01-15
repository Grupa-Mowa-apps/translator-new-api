import { useState, useEffect } from "react";
import { UploadBookToTranslateParamsDTO } from "@/modules/translator/application/dto/uploadBookToTranslateParamsDTO";
import { translatorUploadBookToTranslationHandler } from "@/modules/translator/application/action/handlers";
import { useTranslationContext } from "@/shared/context/useTranslationContext";
import {subscribeToProgress} from "@/modules/translator/infrastructure/api/translationApi";

export function useBookInTranslation(bookId: string, excelFile: File | null ) {
    const [taskId, setTaskId] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const { updateTranslationProgress, setIsTranslationOngoing } = useTranslationContext();

    useEffect(() => {
        const savedTaskId = localStorage.getItem("activeTranslationTaskId");
        if (savedTaskId) {
            setTaskId(savedTaskId);
        }
    }, []);

    useEffect(() => {
        if (!taskId) return;

        const source = subscribeToProgress(taskId, (data) => {
            updateTranslationProgress(taskId, data);

            if (data.progress === 100 || data.progress === -1) {
                source.close();
            }
        });

        return () => {
            source.close();
        };
    }, [taskId]);

    const handelOnTranslateBook = async () => {
        const dto: UploadBookToTranslateParamsDTO = {
            bookId,
            excelFile: excelFile as File,
        };

        setLoading(true);
        setError(null);
        setIsTranslationOngoing(false);

        try {
            setIsTranslationOngoing(true);
            const result = await translatorUploadBookToTranslationHandler(dto);
            setTaskId(result.task_id);
            localStorage.setItem("activeTranslationTaskId", result.task_id);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return {
        handelOnTranslateBook,
        taskId,
        loading,
        error,
        setTaskId
    };
}
