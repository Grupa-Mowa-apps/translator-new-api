import {ReplaceTranslationsState} from "@/modules/parser/application/types/ReplaceTranslationsState";
import {ReplaceTranslationsActions} from "@/modules/parser/application/types/ReplaceTranslationsActions";

export interface UseReplaceTranslationsReturn {
    state: ReplaceTranslationsState;
    actions: ReplaceTranslationsActions;
}
