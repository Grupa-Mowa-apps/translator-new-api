import {ParserMdToExcelParamsDTO} from "@/modules/parser/application/dto/parserMdToExcelParamsDTO";
import {ReplaceTranslationsParamsDTO} from "@/modules/parser/application/dto/replaceTranslationsParamsDTO";
import {validationMessages} from "@/shared/messages/validation";

export function validateParserRequestMdToExcel(dto: ParserMdToExcelParamsDTO): string[] {
    const errors: string[] = [];

    if (!dto.file) {
        errors.push(validationMessages.fileIsRequired);
    }

    if (!dto.file.type.includes("markdown") && !dto.file.name.endsWith(".md")) {
        errors.push(validationMessages.fileMustBeMarkdown);
    }

    if (!dto.quotesType || dto.quotesType.trim() === "") {
        errors.push(validationMessages.quotesTypeIsRequired);
    }

    return errors;
}


export function validateReplaceTranslationsRequest(dto: ReplaceTranslationsParamsDTO): string[] {
    const errors: string[] = [];

    const isExcelMime: boolean = dto.excelFile.type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
    const hasXlsxExtension: boolean = dto.excelFile.name.toLowerCase().endsWith(".xlsx");
    const excelHasContent: boolean = dto.excelFile.size > 0;

    const isMarkdownMime: boolean = dto.mdFile.type === "text/markdown";
    const hasMdExtension: boolean = dto.mdFile.name.toLowerCase().endsWith(".md");
    const mdHasContent: boolean = dto.mdFile.size > 0;

    if (!isExcelMime && !hasXlsxExtension) {
        errors.push(validationMessages.fileMustBeExcel);
    }

    if (!excelHasContent) {
        errors.push(validationMessages.fileIsEmptyExcel);
    }

    if (!isMarkdownMime && !hasMdExtension) {
        errors.push(validationMessages.fileMustBeMarkdown);
    }

    if (!mdHasContent) {
        errors.push(validationMessages.fileIsEmptyMarkdown);
    }

    return errors;
}

