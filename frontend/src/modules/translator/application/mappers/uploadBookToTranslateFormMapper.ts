import { UploadBookToTranslateParamsDTO } from "@/modules/translator/application/dto/uploadBookToTranslateParamsDTO";

export function mapUploadBookDTOToFormData(dto: UploadBookToTranslateParamsDTO): FormData {
    const formData = new FormData();
    formData.append("excel_file", dto.excelFile);
    return formData;
}
