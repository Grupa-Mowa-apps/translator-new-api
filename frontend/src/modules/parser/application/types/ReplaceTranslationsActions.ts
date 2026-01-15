export interface ReplaceTranslationsActions {
    handleExcelFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    handleMdFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    handleSubmit: () => Promise<void>;
}
