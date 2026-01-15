import {TabItem} from "@/shared/types/TabItem";
import {labels} from "@/shared/messages/labels";

import {ParserComponent} from "@/modules/parser/ui/Parser.component";
import {TranslatorComponent} from "@/modules/translator/ui/Translator.component";
import {Tabs} from "@/shared/ui/components/TabsContainer.component";
import {InstructionComponent} from "@/modules/parser/ui/components/Instruction.component";
import {ReactElement} from "react";

export const Dashboard: React.FC = (): ReactElement => {
    const tabItems: TabItem [] = [
        { label: labels.instruction, content: <InstructionComponent />},
        { label: labels.parser, content: <ParserComponent />},
        { label: labels.translator, content: <TranslatorComponent />}
    ];
    return (
        <Tabs tabs={tabItems} defaultIndex={0}/>
    );
};
