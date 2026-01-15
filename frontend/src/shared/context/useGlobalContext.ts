import { useContext } from "react";
import {GlobalContext, GlobalState} from "./GlobalContext";
import {errorMessages} from "@/shared/messages/error";

export const useGlobalContext = () => {
    const context: GlobalState | undefined = useContext(GlobalContext);
    if (!context) {
        throw new Error(`${errorMessages.useGlobalContext} <GlobalProvider>`);
    }
    return context;
};
