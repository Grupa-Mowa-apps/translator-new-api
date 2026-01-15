import React from 'react';

export interface ParserMdToExcelActions {
    handleFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    handleQuotesTypeChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
    handleSubmit: () => Promise<void>;
}
