import React, {ReactElement} from "react";
import { labels } from "@/shared/messages/labels";

interface UploadExcelToTranslationFormProps {
    setExcelFile: (file: File | null) => void;
}

export const UploadExcelToTranslationForm: React.FC<UploadExcelToTranslationFormProps> = ({setExcelFile}: UploadExcelToTranslationFormProps): ReactElement => {
    return (
        <div style={{ maxWidth: "600px", margin: "2rem auto", padding: "1rem", border: "1px solid #ccc", borderRadius: "8px" }}>
            <p style={{ marginBottom: "1rem", fontSize: "1rem", textAlign: "center" }}>
                {labels.uploadExcelFileWithQuoteToTranslationTitle}
                </p>
                <input
                    type="file"
                    accept=".xlsx"
                    onChange={(e) => setExcelFile(e.target.files?.[0] || null)}
                    style={{ marginBottom: "1rem" }}
                />
            </div>
    );
};
