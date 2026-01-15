import React, { ReactElement, useState } from "react";
import { TabItem } from "@/shared/types/TabItem";

type TabsProps = {
    tabs: TabItem[];
    defaultIndex?: number;
    containerStyle?: React.CSSProperties;
    tabButtonStyle?: React.CSSProperties;
    activeTabStyle?: React.CSSProperties;
};

export const Tabs: React.FC<TabsProps> = ({
                                              tabs,
                                              defaultIndex = 0,
                                              containerStyle = {},
                                              tabButtonStyle = {},
                                              activeTabStyle = {},
                                          }: TabsProps): ReactElement => {
    const [activeIndex, setActiveIndex] = useState<number>(defaultIndex);

    return (
        <div style={{ ...containerStyle }}>
            <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
                {tabs.map((tab: TabItem, index: number): ReactElement => {
                    const isActive: boolean = index === activeIndex;

                    return (
                        <button
                            key={tab.label}
                            onClick={() => setActiveIndex(index)}
                            style={{
                                padding: "0.5rem 1rem",
                                backgroundColor: isActive ? "#007bff" : "#e0e0e0",
                                color: isActive ? "#fff" : "#000",
                                border: "none",
                                borderRadius: "4px",
                                cursor: "pointer",
                                fontWeight: isActive ? "bold" : "normal",
                                ...tabButtonStyle,
                                ...(isActive ? activeTabStyle : {}),
                            }}
                        >
                            {tab.label}
                        </button>
                    );
                })}
            </div>

            <div>{tabs[activeIndex]?.content}</div>
        </div>
    );
};
