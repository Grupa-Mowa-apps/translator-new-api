import React, {ReactElement} from "react";
import {Container} from "@/shared/ui/components/Container.component";
import {ParserForm} from "@/modules/parser/ui/components/ParserMarkdownUploaderForm.component";
import {ReplaceTranslationsForm} from "@/modules/parser/ui/components/ReplaceTranslationsForm.component";
import {parser} from "typescript-eslint";

export const ParserComponent: React.FC = (): ReactElement =>
    <Container className={"parser-container"}>
        <ParserForm />
        <ReplaceTranslationsForm />
    </Container>;