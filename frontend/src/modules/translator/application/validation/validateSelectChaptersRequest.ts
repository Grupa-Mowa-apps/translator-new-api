import { validationMessages as VM } from "@/shared/messages/validation";
import {SelectChaptersParamsDTO} from "@/modules/translator/application/dto/translatorRequestDTO";

export function validateSelectChaptersRequest(data: SelectChaptersParamsDTO): boolean {
    const selectingAll: boolean = data.all === true;
    const selectingSome: boolean = Array.isArray(data.chapterIds) && data.chapterIds.length > 0;

    if (!selectingAll && !selectingSome) {
        alert(VM.chaptersSelectionRequired);
        return false;
    }

    if (selectingSome) {
        const hasEmptyId = data.chapterIds!.some(id => !id || id.trim().length === 0);
        if (hasEmptyId) {
            alert(VM.invalidChapterId);
            return false;
        }
    }

    return true;
}
