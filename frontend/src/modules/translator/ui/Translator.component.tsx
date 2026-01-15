import React, {ReactElement} from "react";
import {Container} from "@/shared/ui/components/Container.component";
import {UploadBookForm} from "@/modules/translator/ui/components/UploadBookForm.component";
import {BookToTranslation} from "@/modules/translator/ui/components/BookToTranslation.component";
import BookList from "@/modules/translator/ui/components/BookList.component";

export const TranslatorComponent: React.FC = (): ReactElement => <Container className={"translator-container"}>
    <UploadBookForm />
    <BookList />
    <BookToTranslation />
</Container>;