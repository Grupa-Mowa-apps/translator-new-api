import React from 'react';
import {useParserMdToExcel} from "@/modules/parser/ui/hooks/useParserMdToExcel";
import {labels} from "@/shared/messages/labels";

export const ParserForm: React.FC = (): React.ReactElement => {
    const { state, actions } = useParserMdToExcel();
    const { file, quotesType, loading, error } = state;
    const { handleFileChange, handleQuotesTypeChange, handleSubmit } = actions;

    return (
        <div style={{ maxWidth: 400, margin: '0 auto', fontFamily: 'sans-serif', border: '1px solid #ccc' }}>
            <h2>Parser MD → Excel</h2>

            <div style={{ marginBottom: '1rem', padding: 10, border: '1px solid grey' }}>
                <label>
                    {labels.chooseFile}
                    <input
                        type="file"
                        accept=".md,.txt"
                        onChange={handleFileChange}
                        disabled={loading}
                    />
                </label>
                {file && <p>📄 {labels.choose} {file.name}</p>}
            </div>

            <div style={{ marginBottom: '1rem' }}>
                <label>
                    {labels.quoteType}
                    <select
                        value={quotesType}
                        onChange={handleQuotesTypeChange}
                        disabled={loading}
                    >
                        <option value="fr">fr</option>
                        <option value="ge">ge</option>
                    </select>
                </label>
            </div>

            <div style={{ marginBottom: '1rem' }}>
                <button onClick={handleSubmit} disabled={loading || !file}>
                    {loading ? `${labels.processing}` : `${labels.sendMDAndReceivedExcel}`}
                </button>
            </div>
            {error && <p style={{ color: 'red' }}>❌ {error}</p>}
        </div>
    );
};
