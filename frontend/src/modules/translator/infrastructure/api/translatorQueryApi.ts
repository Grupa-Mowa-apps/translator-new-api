import {errorMessages} from "@/shared/messages/error";
import {env} from "@/shared/config/apiConfig";

export async function translatorGetBookRest(bookId: string): Promise<Response> {
    const res: Response = await fetch(`${env.apiUrl}/translator/book/${bookId}`, {
        method: "GET",
    });

    if (!res.ok) {
        throw new Error(`${errorMessages.errorMsg} ${res.status}`);
    }

    return res;
}

export async function downloadTranslatedFile(taskId: string): Promise<Blob> {
    const res = await fetch(`${env.apiUrl}/translator/download/${taskId}`, {
        method: "GET",
    });

    if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Nie udało się pobrać pliku: ${res.status} — ${errorText}`);
    }

    return await res.blob();
}
