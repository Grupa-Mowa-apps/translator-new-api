import {UploadBookParamsDTO} from "@/modules/translator/application/dto/translatorRequestDTO";
import {validationMessages as VM} from "@/shared/messages/validation";

export function validateUploadBookRequest(data: UploadBookParamsDTO): boolean {
    const isMarkdown: boolean = data.file.type === "text/markdown";
    const hasMdExtension: boolean = data.file.name.toLowerCase().endsWith(".md");
    const hasContent: boolean = data.file.size > 0;

    if (!isMarkdown && !hasMdExtension) {
        alert(VM.fileMustBeMarkdown);
        return false;
    }

    if (!hasContent) {
        alert(VM.fileIsEmpty);
        return false;
    }

    if (!data.quoteType) {
        alert(VM.quoteTypeRequired);
        return false;
    }

    if (!data.title || data.title.trim().length === 0) {
        alert(VM.titleRequired);
        return false;
    }

    if (!data.genre || data.genre.trim().length === 0) {
        alert(VM.genreRequired);
        return false;
    }

    return true;
}