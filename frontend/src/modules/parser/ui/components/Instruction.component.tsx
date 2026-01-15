import React, {ReactElement} from "react";
import {Container} from "@/shared/ui/components/Container.component";
import {labels} from "@/shared/messages/labels";

export const InstructionComponent: React.FC = (): ReactElement =>
    <Container>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-start",}}>
            <div style={{marginBottom:20}}>{labels.instructionDescription}</div>
                <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-start", marginTop: 20 }}>
                    <div style={{marginBottom:10}}>{labels.parserStep1}</div>
                    <div style={{marginBottom:10}}>{labels.parserStep2}</div>
                </div>
                <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-start", marginTop: 20 }}>
                    <div style={{marginBottom:10}}>{labels.translatorStep1}</div>
                    <div style={{marginBottom:10}}>{labels.translatorStep2}</div>
                    <div style={{marginBottom:10}}>{labels.translatorStep3}</div>
                    <div style={{marginBottom:10}}>{labels.translatorStep4}</div>
                    <div style={{marginBottom:10}}>{labels.translatorStep5}</div>
                </div>
        </div>
    </Container>;