import React from "react";
import { useUploadBook } from "@/modules/translator/ui/hooks/useUploadBook";
import { labels } from "@/shared/messages/labels";
import {Container} from "@/shared/ui/components/Container.component";

export const UploadBookForm: React.FC = (): React.ReactElement => {
    const {
        state: { file, quoteType, title, genre, loading, error, response },
        actions: {
            handleFileChange,
            handleQuoteTypeChange,
            handleTitleChange,
            handleGenreChange,
            handleSubmit,
        },
    } = useUploadBook();

    return (
        <Container className={"upload-form-container"}>
            <div style={{ maxWidth: 500, margin: "0 auto", fontFamily: "sans-serif", backgroundColor: "darkslategrey", padding: "1.5rem"}}>
                <h2>📚 Upload Book (MD → Memory)</h2>

                <div className={"upload-form-container"} style={{ marginBottom: "1rem" }}>
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

                <div className={"upload-form-container"} style={{ marginBottom: "1rem" }}>
                    <label>
                        {labels.quoteType}
                        <select
                            value={quoteType}
                            onChange={handleQuoteTypeChange}
                            disabled={loading}
                        >
                            <option value="fr">fr</option>
                            <option value="ge">ge</option>
                        </select>
                    </label>
                </div>

                <div className={"upload-form-container"} style={{ marginBottom: "1rem" }}>
                    <label>
                        {labels.title}
                        <input
                            type="text"
                            value={title}
                            onChange={handleTitleChange}
                            disabled={loading}
                        />
                    </label>
                </div>

                <div className={"upload-form-container"} style={{ marginBottom: "1rem" }}>
                    <label>
                        {labels.bookGenre}
                        <input
                            type="text"
                            value={genre}
                            onChange={handleGenreChange}
                            disabled={loading}
                        />
                    </label>
                </div>

                <div style={{ marginBottom: "1rem" }}>
                    <button onClick={handleSubmit} disabled={loading || !file}>
                        {loading ? `${labels.loadingBook}` : `${labels.sendSelection}`}
                    </button>
                </div>

                {error && <p style={{ color: "red" }}>❌ {error}</p>}
                {response && (
                    <div style={{ marginTop: "1rem", color: "green" }}>
                        ✅ {response.message}<br />
                        📖 {labels.id}: {response.book_id}<br />
                        📘 {labels.title} {response.title}<br />
                        📑 {labels.bookGenre} {response.chapters_count}
                    </div>
                )}
            </div>
        </Container>
    );
};
