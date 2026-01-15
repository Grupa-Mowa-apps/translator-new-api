export function downloadBlobAsFile(blob: Blob, filename: string, mimeType: string): void {
    const url = URL.createObjectURL(
        new Blob([blob], { type: mimeType })
    );

    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();

    URL.revokeObjectURL(url);
}
