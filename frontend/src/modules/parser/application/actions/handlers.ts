import {
    validateParserRequestMdToExcel,
    validateReplaceTranslationsRequest
} from "@/modules/parser/application/validation/validateParserRequest";
import {ParserMdToExcelParamsDTO} from "@/modules/parser/application/dto/parserMdToExcelParamsDTO";
import {
    mapMDExcelDTOToFormData,
    mapReplaceTranslationsDTOToFormData
} from "@/modules/parser/application/mappers/parserRequestDTOMappers";
import {
    parserExtractMdToExcelRest,
    parserReplaceTranslationsRest
} from "@/modules/parser/infrastructure/api/parserCommandApi";
import {ReplaceTranslationsParamsDTO} from "@/modules/parser/application/dto/replaceTranslationsParamsDTO";
import {ParserMdToExcelResultDTO} from "@/modules/parser/application/dto/parserMdToExcelResultDTO";
import {ReplaceTranslationsResultDTO} from "@/modules/parser/application/dto/replaceTranslationsResultDTO";

export async function submitParserRequestMdToExcel(dto: ParserMdToExcelParamsDTO): Promise<ParserMdToExcelResultDTO> {
    const errors: string[] = validateParserRequestMdToExcel(dto);
    if (errors.length > 0) {
        throw new Error(errors.join("\n"));
    }

    const formData: FormData = mapMDExcelDTOToFormData(dto);
    const response: Blob = await parserExtractMdToExcelRest(formData);
    return {file : response};
}

export async function submitParserRequestReplaceTranslations(dto: ReplaceTranslationsParamsDTO): Promise<ReplaceTranslationsResultDTO> {

    const errors: string[] = validateReplaceTranslationsRequest(dto);
    if (errors.length > 0) {
        throw new Error(errors.join("\n"));
    }

    const formData: FormData = mapReplaceTranslationsDTOToFormData(dto);
    const response: Blob = await parserReplaceTranslationsRest(formData);
    return {file : response};
}