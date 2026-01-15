import React from "react";
import {labels} from "@/shared/messages/labels";
import {Dropdown, DropdownOption} from "@/shared/ui/components/Dropdown.component";
import {useBookOptions} from "@/shared/ui/hooks/useBookOptions";
import {useBookToTranslation} from "@/modules/translator/ui/hooks/useBookToTranslation";
import {MultiSelectDropdown} from "@/shared/ui/components/MultiSelectDropdown.component";
import {Button} from "@/shared/ui/components/Button.component";
import {UploadExcelToTranslationForm} from "@/modules/translator/ui/components/UploadExcelToTranslationForm.component";
import {useTranslationContext} from "@/shared/context/useTranslationContext";
import {useBookInTranslation} from "@/modules/translator/ui/hooks/useBookInTranslation";
import TranslationProgress from "@/modules/translator/ui/components/TranslationProgress.component";
import TranslationDownload from "@/modules/translator/ui/components/TranslationDownload.component";

export function BookToTranslation(): React.ReactElement {
    const bookOptions: DropdownOption[] = useBookOptions();

    const {
        bookId,
        setBookId,
        book,
        loading,
        chapterOptions,
        selectedChapterOptions,
        handleChapterSelection,
        handleSubmitOnChaptersSelected,
        setExcelFile,
        excelFile,
        selectedChapters,
        setSelectedChapters,
        setAreChaptersSelectedAnConfirmed,
        areChaptersSelectedAnConfirmed
    } = useBookToTranslation();

    const {
        handelOnTranslateBook,
        taskId,
        setTaskId
    } = useBookInTranslation(bookId, excelFile);

    const { translationProgress, isTranslationOngoing, setIsTranslationOngoing} = useTranslationContext();
    const progress: number | null = taskId ? translationProgress[taskId]?.progress : null;


    const handleReset = () => {
        setIsTranslationOngoing(false);
        setBookId("");
        setExcelFile(null);
        setSelectedChapters([]);
        setTaskId("");
        setAreChaptersSelectedAnConfirmed(false);
    };

    return (
        <div style={{ backgroundColor: "slategrey", padding: "1rem", maxWidth: "500px", margin: "0 auto" }}>
            <h3 style={{ marginBottom: "1rem" }}>{!isTranslationOngoing || progress !== 100 ? book?.title : labels.bookAndChaptersSelectionToTranslationTitle}</h3>

            {isTranslationOngoing || progress !== 100 && (
                <>
                    <Dropdown
                        options={bookOptions}
                        value={bookId}
                        onChange={setBookId}
                        placeholder={labels.chooseBookTitle}
                        disabled={isTranslationOngoing || areChaptersSelectedAnConfirmed}
                    />

                    {loading && (
                        <p style={{ marginTop: "1rem", color: "#fff" }}>
                            {labels.loadingBook}
                        </p>
                    )}

                    {!areChaptersSelectedAnConfirmed && (
                        <div>
                            {!loading && book && (
                                <MultiSelectDropdown
                                    options={chapterOptions}
                                    selected={selectedChapterOptions}
                                    onChange={handleChapterSelection}
                                    placeholder={labels.chooseChapterTitle}
                                />
                            )}

                            {selectedChapterOptions.length > 0 && (
                                <Button onClick={handleSubmitOnChaptersSelected} className="app-button">
                                    {loading ? labels.processing : labels.confirmChaptersSelection}
                                </Button>
                            )}
                        </div>
                    )}

                    {areChaptersSelectedAnConfirmed && (
                        <div style={{ marginTop: "1rem" }}>
                            <p style={{ fontWeight: "bold", marginBottom: "0.5rem" }}>Chapters selected and confirmed:</p>
                            <div style={{ display: "flex", flexDirection: "column", gap: "0.25rem", color: "#fff" }}>
                                {selectedChapters.map((chapter) => (
                                    <div key={chapter.id}>
                                        {chapter.no}. {chapter.title}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {areChaptersSelectedAnConfirmed && (
                        <UploadExcelToTranslationForm setExcelFile={setExcelFile} />
                    )}
                    {excelFile !== null &&
                        <Button onClick={() => {
                            handelOnTranslateBook();
                        }}>
                            {loading ? labels.bookUploading : labels.sendBookToTranslation}
                        </Button>
                    }
                </>
            )}
            {taskId && <TranslationProgress taskId={taskId} />}
            {taskId && progress===100 && <TranslationDownload taskId={taskId} onReset={handleReset} />}
        </div>
    );
}