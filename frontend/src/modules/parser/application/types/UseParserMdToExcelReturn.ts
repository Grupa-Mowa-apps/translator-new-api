import {ParserMdToExcelState} from "@/modules/parser/application/types/ParserMdToExcelState";
import {ParserMdToExcelActions} from "@/modules/parser/application/types/ParserMdToExcelActions";

export interface UseParserMdToExcelReturn {
    state: ParserMdToExcelState;
    actions: ParserMdToExcelActions;
}
