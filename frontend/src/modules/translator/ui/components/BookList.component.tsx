import React, {ReactElement, useContext} from "react";
import {labels} from "@/shared/messages/labels";
import {BookSummaryDTO} from "@/shared/dto/bookSummaryDTO";
import {useBooksContext} from "@/shared/context/useBooksContext";


const BookList: React.FC = ():ReactElement => {
    const { books } = useBooksContext();

    return (
        <div style={{ backgroundColor: "darkolivegreen", padding: ".5em", marginTop: "1rem" }}>
            <h2>📚 {labels.bookList}</h2>
            {books.length === 0 ? (
                <p>{labels.emptyBookList}</p>
            ) : (
                <div>
                    {books.map((book: BookSummaryDTO) => (
                        <div key={book.id} style={{ marginBottom: "8px" }}>
                            <strong>{labels.id}</strong> {book.id} — <strong>{labels.title}</strong> {book.title}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default BookList;
