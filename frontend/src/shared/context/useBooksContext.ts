import { useGlobalContext } from "./useGlobalContext";

export const useBooksContext = () => {
    const { books, refreshBooks } = useGlobalContext();
    return { books, refreshBooks };
};
