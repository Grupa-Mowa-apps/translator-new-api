import type { Quote } from "@/shared/types/Quote";

export interface ParserMdToExcelState {
    file: File | null;
    quotesType: Quote;
    loading: boolean;
    error: string | null;
}
