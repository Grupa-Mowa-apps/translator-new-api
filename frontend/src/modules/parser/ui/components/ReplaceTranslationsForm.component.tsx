import React from "react";
import {useReplaceTranslations} from "@/modules/parser/ui/hooks/useReplaceTranslations";
import {labels} from "@/shared/messages/labels";

export const ReplaceTranslationsForm: React.FC = (): React.ReactElement => {
    const {state, actions} = useReplaceTranslations();
    const {excelFile, mdFile, loading, error,} = state;
    const {handleExcelFileChange, handleMdFileChange, handleSubmit,} = actions;

    return (
        <div style={{ maxWidth: 400, margin: "0 auto", fontFamily: "sans-serif",  border: '1px solid #ccc' }}>
            <h2>Replace Translations → MD</h2>
            <div style={{ marginBottom: "1rem", padding: 10, border: '1px solid grey' }}>
                <label>
                    {labels.chooseExcelFile}
                    <input
                        type="file"
                        accept=".xlsx"
                        onChange={handleExcelFileChange}
                        disabled={loading}
                    />
                </label>
                {excelFile && <p>📊 {labels.choose} {excelFile.name}</p>}
            </div>

            <div style={{ marginBottom: "1rem", padding: 10, border: '1px solid grey' }}>
                <label>
                    {labels.chooseMarkdownFile}
                    <input
                        type="file"
                        accept=".md"
                        onChange={handleMdFileChange}
                        disabled={loading}
                    />
                </label>
                {mdFile && <p>📄 {labels.choose} {mdFile.name}</p>}
            </div>

            <div style={{ marginBottom: "1rem" }}>
                <button onClick={handleSubmit} disabled={loading || !excelFile || !mdFile}>
                    {loading ? `${labels.processing}` : `${labels.sendMDAndExcelReceivedMD}`}
                </button>
            </div>

            {error && <p style={{ color: "red" }}>❌ {error}</p>}
        </div>
    );
};