import {
    SelectChaptersParamsDTO,
    SelectChaptersResponseDTO,
    UploadBookParamsDTO,
    UploadBookResponseDTO
} from "@/modules/translator/application/dto/translatorRequestDTO";
import {
    translatorSelectChaptersRest,
    translatorUploadBookRest, translatorUploadBookToTranslationRest
} from "@/modules/translator/infrastructure/api/translatorCommandApi";
import {validateUploadBookRequest} from "@/modules/translator/application/validation/validateTranslatorRequest";
import {validateSelectChaptersRequest} from "@/modules/translator/application/validation/validateSelectChaptersRequest";
import {translatorGetBookRest} from "@/modules/translator/infrastructure/api/translatorQueryApi";
import {mapResponseToBook} from "@/modules/translator/application/mappers/mapResponseToBook";
import {mapUploadBookDTOToFormData} from "@/modules/translator/application/mappers/uploadBookToTranslateFormMapper";
import {validateUploadBookToTranslation} from "@/modules/translator/application/validation/requestValidation";
import {UploadBookToTranslateParamsDTO} from "@/modules/translator/application/dto/uploadBookToTranslateParamsDTO";
import {errorMessages} from "@/shared/messages/error";

export async function translatorUploadBookHandler(
    params: UploadBookParamsDTO
): Promise<UploadBookResponseDTO> {
    validateUploadBookRequest(params);

    const formData = new FormData();
    formData.append("file", params.file);
    formData.append("quote_type", params.quoteType);
    formData.append("title", params.title);
    formData.append("genre", params.genre);

    const res = await translatorUploadBookRest(formData);
    const data = await res.json();

    return data as UploadBookResponseDTO;
}

export async function translatorSelectChaptersHandler(
    bookId: string,
    params: SelectChaptersParamsDTO
): Promise<SelectChaptersResponseDTO> {
    if (!validateSelectChaptersRequest(params)) {
        throw new Error(errorMessages.incorrectChapterSelection);
    }

    const res = await translatorSelectChaptersRest(bookId, {
        all: params.all ?? false,
        chapter_ids: params.chapterIds ?? [],
    });

    const data = await res.json();
    return data as SelectChaptersResponseDTO;
}

export async function translatorGetBookHandler(bookId: string) {
    const response = await translatorGetBookRest(bookId);
    const data = await response.json();

    if (data.error) {
        throw new Error(data.error);
    }

    return mapResponseToBook(data);
}

export async function translatorUploadBookToTranslationHandler(
    dto: UploadBookToTranslateParamsDTO
): Promise<{ task_id: string }> {
    const errors = validateUploadBookToTranslation(dto);
    if (errors.length > 0) {
        throw new Error(errors.join("\n"));
    }

    const formData: FormData = mapUploadBookDTOToFormData(dto);
    return await translatorUploadBookToTranslationRest(dto.bookId, formData);
}