import React, { useEffect } from "react";
import {useTranslationContext} from "@/shared/context/useTranslationContext";
import {subscribeToProgress} from "@/modules/translator/infrastructure/api/translationApi";
import BookFlipAnimation from "@/modules/translator/ui/components/BookFlipAnimation.component";


interface Props {
    taskId: string;
    onDone?: () => void;
}

const TranslationProgress: React.FC<Props> = ({ taskId, onDone }) => {
    const { translationProgress, updateTranslationProgress } = useTranslationContext();
    const progressData = translationProgress[taskId];

    useEffect(() => {
        const source = subscribeToProgress(taskId, (data) => {
            updateTranslationProgress(taskId, data);
            if (data.progress === 100 && onDone) {
                onDone();
            }
        });

        return () => {
            source.close();
        };
    }, [taskId]);

    useEffect(() => {
        const savedTaskId = localStorage.getItem("activeTranslationTaskId");
        if (!savedTaskId) return;

        const source = subscribeToProgress(savedTaskId, (data) => {
            updateTranslationProgress(savedTaskId, data);

            if (data.progress === 100 || data.progress === -1) {
                source.close();
            }
        });

        return () => {
            source.close();
        };
    }, []);

    if (!progressData) return <p>Oczekiwanie na postęp...</p>;

    return (
        <div>
            <p>{progressData.message}</p>
            <progress value={progressData.progress} max={100} />
            <BookFlipAnimation progress={progressData.progress} />
        </div>
    );
};

export default TranslationProgress;
