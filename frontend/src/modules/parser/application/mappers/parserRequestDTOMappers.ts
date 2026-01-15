import {ParserMdToExcelParamsDTO} from "@/modules/parser/application/dto/parserMdToExcelParamsDTO";
import {ReplaceTranslationsParamsDTO} from "@/modules/parser/application/dto/replaceTranslationsParamsDTO";

export function mapMDExcelDTOToFormData(dto: ParserMdToExcelParamsDTO): FormData {
    const formData: FormData = new FormData();
    formData.append("file", dto.file);
    formData.append("quotes_type", dto.quotesType);
    return formData;
}

export function mapReplaceTranslationsDTOToFormData(dto: ReplaceTranslationsParamsDTO): FormData {
    const formData: FormData = new FormData();
    formData.append("excel_file", dto.excelFile);
    formData.append("md_file", dto.mdFile);
    return formData;
}