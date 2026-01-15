import React, { ReactElement, useState } from "react";
import { labels } from "@/shared/messages/labels";

export interface MultiDropdownOption {
    label: string;
    value: string;
}

interface MultiSelectDropdownProps {
    options: MultiDropdownOption[];
    selected: MultiDropdownOption[];
    onChange: (selected: MultiDropdownOption[]) => void;
    placeholder?: string;
}

export const MultiSelectDropdown: React.FC<MultiSelectDropdownProps> = ({
                                                                            options = [],
                                                                            selected = [],
                                                                            onChange,
                                                                            placeholder = labels.choose,
                                                                        }: MultiSelectDropdownProps): ReactElement => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleOption = (option: MultiDropdownOption) => {
        const exists = selected.find((sel) => sel.value === option.value);
        const updated = exists
            ? selected.filter((sel) => sel.value !== option.value)
            : [...selected, option];
        onChange(updated);
    };

    const toggleAll = () => {
        if (selected.length === options.length) {
            onChange([]);
        } else {
            onChange([...options]);
        }
    };

    const isChecked = (value: string) =>
        selected.some((opt) => opt.value === value);

        const selectStyle = {
        width: "100%",
        padding: "0.5rem",
        border: "1px solid #ccc",
        backgroundColor: "#2d2d2d",
        color: "#fff",
        fontSize: ".85rem",
        lineHeight: "1.2",
        borderRadius: "2px",
        appearance: "none" as const,
        textAlign: "left" as const,
        position: "relative" as const,
        cursor: "pointer",
    };

    const optionListStyle = {
        position: "absolute" as const,
        top: "100%",
        left: 0,
        right: 0,
        border: "1px solid #ccc",
        backgroundColor: "#f5f5f5",
        color: "#000",
        zIndex: 10,
        maxHeight: "200px",
        overflowY: "auto" as const,
        fontSize: "1rem",
        lineHeight: "1.5",
        borderRadius: "4px",
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
        width: "104%"
    };

    const optionItemStyle = {
        display: "flex",
        alignItems: "center",
        padding: "0.5rem",
        cursor: "pointer",
        borderBottom: "1px solid #eee",
        backgroundColor: "#f5f5f5",
        color: "#000",
    };

    return (
        <div style={{ position: "relative", width: "95%", backgroundColor: "#2d2d2d", marginBottom: "1rem" }}>
            <div onClick={() => setIsOpen(!isOpen)} style={selectStyle}>
                <span>{placeholder}</span>
                <span style={{
                    position: "absolute",
                    right: "0.75rem",
                    top: "50%",
                    transform: "translateY(-50%)",
                    pointerEvents: "none",
                    fontSize: "0.75rem",
                    color: "#fff",
                }}>
          ▼
        </span>
            </div>

            {isOpen && (
                <div style={optionListStyle}>
                    <label style={optionItemStyle}>
                        <input
                            type="checkbox"
                            checked={selected.length === options.length}
                            onChange={toggleAll}
                            style={{ marginRight: "0.5rem" }}
                        />
                        Select all
                    </label>

                    {options.map((opt) => (
                        <label key={opt.value} style={optionItemStyle}>
                            <input
                                type="checkbox"
                                checked={isChecked(opt.value)}
                                onChange={() => toggleOption(opt)}
                                style={{ marginRight: "0.5rem" }}
                            />
                            {opt.label}
                        </label>
                    ))}
                </div>
            )}
        </div>
    );
};