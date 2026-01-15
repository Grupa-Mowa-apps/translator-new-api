import {useGlobalContext} from "@/shared/context/useGlobalContext";

export const useTranslationContext = () => {
    const { translationProgress, updateTranslationProgress, isTranslationOngoing, setIsTranslationOngoing } = useGlobalContext();
    return { translationProgress, updateTranslationProgress, isTranslationOngoing, setIsTranslationOngoing };
};