import React from "react";

type ContainerProps = {
    children: React.ReactNode;
    background?: string;
    className?: string;
    title?: string;
};

export const Container: React.FC<ContainerProps> = ({children, className = "", background, title}: ContainerProps): React.ReactElement => {
    return (
        <div className={className} style={{background}}>
            <h3>{title}</h3>
            {children}
        </div>
    );
};
