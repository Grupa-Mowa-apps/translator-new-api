import asyncio
from collections import defaultdict
from typing import Any, Dict
from app.domain.ports.progress_tracker_port import ProgressTrackerPort


class ProgressTrackerAdapter(ProgressTrackerPort):
    def __init__(self):
        self.progress: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self._subscribers = defaultdict(set)

    def has_task(self, task_id: str) -> bool:
        return task_id in self.progress
    
    async def start(self, task_id: str, initial_message = "Started") -> None:
        self.progress[task_id] = {"progress": 0, "message": initial_message}

        if task_id in self._subscribers:
            for queue in self._subscribers[task_id]:
                await queue.put(self.progress[task_id])

    async def update(self, task_id: str, progress: int, message: str) -> None:
        progress_update = {"progress": progress, "message": message}
        self.progress[task_id] = progress_update

        if task_id in self._subscribers:
            for queue in self._subscribers[task_id]:
                await queue.put(progress_update)

    async def complete(self, task_id: str, message: str = "Complete") -> None:
        await self.update(task_id=task_id, progress=100, message=message)

    async def fail(self, task_id: str, message: str = "Failed") -> None:
        await self.update(task_id=task_id, progress=max(self.progress.get(task_id, {}).get("progress", 0), 0), message=message)

    async def subscribe(self, task_id: str) -> asyncio.Queue:
        queue = asyncio.Queue()
        self._subscribers[task_id].add(queue)

        if task_id in self.progress:
            await queue.put(self.progress[task_id])

        return queue

    async def unsubscribe(self, task_id: str, queue: asyncio.Queue) -> None:
        if task_id in self._subscribers:
            self._subscribers[task_id].discard(queue)
            if not self._subscribers[task_id]:
                del self._subscribers[task_id]