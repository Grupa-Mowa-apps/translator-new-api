import { useBooksContext } from "@/shared/context/useBooksContext";
import {DropdownOption} from "@/shared/ui/components/Dropdown.component";
import {BookSummaryDTO} from "@/shared/dto/bookSummaryDTO";

export function useBookOptions(): DropdownOption[] {
    const { books } = useBooksContext();

    return books
        // .filter((book) => book.isActive !== false) // later we can use filter to remove books in translation status
        .sort((a: BookSummaryDTO, b: BookSummaryDTO): number => a.title.localeCompare(b.title))
        .map<DropdownOption>((book: BookSummaryDTO): DropdownOption => ({
            label: book.title,
            value: book.id,
        }));
}
