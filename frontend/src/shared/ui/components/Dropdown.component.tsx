import React, {ReactElement} from "react";
import {labels} from "@/shared/messages/labels";

export interface DropdownOption {
    label: string;
    value: string;
}

interface DropdownProps {
    options: DropdownOption[];
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
    disabled?: boolean;
}

export const Dropdown: React.FC<DropdownProps> = ({options, value, onChange, placeholder = `${labels.choose}`, disabled = false}: DropdownProps):
    ReactElement => {
    return (
        <select
            value={value}
            onChange={(e) => onChange(e.target.value)}
            style={{ width: "100%", padding: "0.5rem", marginBottom: "1rem" }}
            disabled={disabled}>
            <option value="">{placeholder}</option>
            {options.map((opt: DropdownOption): ReactElement => (
                <option key={opt.value} value={opt.value}>
                    {opt.label}
                </option>
            ))}
        </select>
    );
};