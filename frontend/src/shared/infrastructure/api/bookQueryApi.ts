import {BookSummaryDTO} from "@/shared/dto/bookSummaryDTO";
import {env} from "@/shared/config/apiConfig";
import {errorMessages} from "@/shared/messages/error";

export async function getBooksSummaryRest(): Promise<BookSummaryDTO[]> {
    const res: Response = await fetch(`${env.apiUrl}/translator/books`, {
        method: "GET",
    });

    if (!res.ok) {
        throw new Error(`${errorMessages.errorMsg} ${res.status}`);
    }

    const data: BookSummaryDTO[] = await res.json();
    return data;
}