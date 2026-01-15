import {env} from "@/shared/config/apiConfig";
import {labels} from "@/shared/messages/labels";
import {errorMessages} from "@/shared/messages/error";

export function subscribeToProgress(
    taskId: string,
    onUpdate: (data: { progress: number; message: string }) => void,
    onError?: () => void
): EventSource {
    const source = new EventSource(`${env.apiUrl}/translator/progress/${taskId}`);
    console.log(labels.eventSource, source);
    source.onmessage = (event) => {
        const data = JSON.parse(event.data);
        onUpdate(data);
    };

    source.addEventListener("done", () => {
        source.close();
    });

    source.addEventListener("error", (e) => {
        console.error(errorMessages.sseError, e);
        if (onError) onError();
        source.close();
    });

    source.addEventListener("timeout", () => {
        onUpdate({ progress: -1, message: labels.translationCompleted });
        source.close();
    });

    return source;
}