import { errorMessages } from "@/shared/messages/error";
import {env} from "@/shared/config/apiConfig";

export async function translatorUploadBookRest(formData: FormData): Promise<Response> {
    const res: Response = await fetch(`${env.apiUrl}/translator/upload_book/`, {
        method: "POST",
        body: formData,
    });

    if (!res.ok) {
        throw new Error(`${errorMessages.errorMsg} ${res.status}`);
    }

    return res;
}

export async function translatorSelectChaptersRest(
    bookId: string,
    payload: { all: boolean; chapter_ids: string[] }
): Promise<Response> {
    const res: Response = await fetch(`${env.apiUrl}/translator/book/${bookId}/select_chapters/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    if (!res.ok) {
        throw new Error(`${errorMessages.errorMsg} ${res.status}`);
    }

    return res;
}

export async function translatorUploadBookToTranslationRest(
    bookId: string,
    formData: FormData
): Promise<{ task_id: string }> {
    const res = await fetch(`${env.apiUrl}/translator/translate_book/${bookId}/async`, {
        method: "POST",
        body: formData,
    });

    if (!res.ok) {
        throw new Error(`${errorMessages.translationError} ${res.status}`);
    }

    return await res.json();
}

export async function cleanupTranslatedFile(taskId: string): Promise<void> {
    const res = await fetch(`${env.apiUrl}/translator/download/${taskId}`, {
        method: "DELETE",
    });

    if (!res.ok) {
        throw new Error(`${errorMessages.errorWhenFileDeleting} ${res.status}`);
    }
}


