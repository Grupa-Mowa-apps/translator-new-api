import React from "react";
import "./BookFlipAnimation.css";
import {labels} from "@/shared/messages/labels";

interface Props {
    progress: number;
}

const BookFlipAnimation: React.FC<Props> = ({ progress }) => {
    if (progress === 100) {
        return <h2 className="success-message">{labels.translationCompleted} ✅</h2>;
    }

    return (
        <div className="book-animation-container">
            <div className="book">
                <div className="cover" />
                <div className="pages" />
            </div>
            <p>Trwa tłumaczenie... przewracam rozdziały 📚</p>
        </div>
    );
};

export default BookFlipAnimation;
