import React from "react";
import { useTranslationContext } from "@/shared/context/useTranslationContext";
import {cleanupTranslatedFile} from "@/modules/translator/infrastructure/api/translatorCommandApi";
import {downloadTranslatedFile} from "@/modules/translator/infrastructure/api/translatorQueryApi";
import {labels} from "@/shared/messages/labels";
import {errorMessages} from "@/shared/messages/error";

interface Props {
    taskId: string;
    onReset: () => void;
}

const TranslationDownload: React.FC<Props> = ({ taskId, onReset }) => {
    const { updateTranslationProgress } = useTranslationContext();

    const handleDownload = async () => {
        try {
            const blob = await downloadTranslatedFile(taskId);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "translated.md";
            a.click();
            window.URL.revokeObjectURL(url);

            const confirmed: boolean = window.confirm(labels.beforeDeleteFileAlert);
            if (confirmed) {
                await cleanupTranslatedFile(taskId);
                localStorage.removeItem("activeTranslationTaskId");
                updateTranslationProgress(taskId, { progress: -1, message: labels.fileDeleted });
                onReset();
            }
        } catch (err) {
            alert({errorMessages: errorMessages.errorDuringFileDownload});
            console.error(err);
        }
    };

    return (
        <div style={{ marginTop: "1.5rem", textAlign: "center" }}>
            <button
                onClick={handleDownload}
                style={{
                    padding: "0.6rem 1.2rem",
                    backgroundColor: "#007bff",
                    color: "#fff",
                    border: "none",
                    borderRadius: "4px",
                    cursor: "pointer",
                    fontSize: "1rem",
                }}
            >
                📥 {labels.downloadTranslatedBook}
            </button>
        </div>
    );
};

export default TranslationDownload;

