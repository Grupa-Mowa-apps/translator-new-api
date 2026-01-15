import React, {ReactElement} from "react";
import {ButtonType} from "@/shared/ui/types/ButtonType";

interface ButtonProps {
    onClick: () => void;
    disabled?: boolean;
    children: React.ReactNode;
    type?: ButtonType;
    className?: string;
}

export const Button: React.FC<ButtonProps> = ({
                                                  onClick,
                                                  disabled = false,
                                                  children,
                                                  type = "button",
                                                  className = "",
                                              }: ButtonProps): ReactElement => {
    return (
        <button
            type={type}
            onClick={onClick}
            disabled={disabled}
            className={`app-button ${className}`}>
            {children}
        </button>
    );
};
