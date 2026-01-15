import {errorMessages} from "@/shared/messages/error";
import {env} from "@/shared/config/apiConfig";

export async function parserExtractMdToExcelRest(formData: FormData): Promise<Blob> {
    const res: Response = await fetch(`${env.apiUrl}/parser/extract/`, {
        method: 'POST',
        body: formData,
    });

    if (!res.ok) {
        throw new Error(`${errorMessages.errorMsg} ${res.status}`);
    }

    return await res.blob();
}

export async function parserReplaceTranslationsRest(formData: FormData): Promise<Blob> {
    const res: Response = await fetch(`${env.apiUrl}/parser/replace_tranlsations/`, {
        method: "POST",
        body: formData,
    });

    if (!res.ok) {
        throw new Error(`${errorMessages.errorMsg} ${res.status}`);
    }

    return await res.blob();
}