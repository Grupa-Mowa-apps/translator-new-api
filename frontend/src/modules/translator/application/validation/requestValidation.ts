import {UploadBookToTranslateParamsDTO} from "@/modules/translator/application/dto/uploadBookToTranslateParamsDTO";
import {validationMessages} from "@/shared/messages/validation";

export function validateUploadBookToTranslation(dto: UploadBookToTranslateParamsDTO): string[] {
    const errors: string[] = [];

    if (!dto.bookId || dto.bookId.trim() === "") {
        errors.push(validationMessages.bookIdIsRequired);
    }

    if (!dto.excelFile) {
        errors.push(validationMessages.excelFileRequired);
    } else if (dto.excelFile.type !== "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") {
        errors.push(validationMessages.fileMustBeExcel);
    }

    return errors;
}
