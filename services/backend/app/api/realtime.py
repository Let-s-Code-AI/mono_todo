"""In-memory registry of open WebSocket connections, keyed by user."""

from collections.abc import Iterable

from fastapi import Request, WebSocket, WebSocketDisconnect


class ConnectionManager:
    """Tracks every open socket of every user and fans messages out to them."""

    def __init__(self) -> None:
        self._sockets: dict[int, set[WebSocket]] = {}

    def register(self, user_id: int, websocket: WebSocket) -> None:
        """Remember an accepted socket as belonging to `user_id`."""
        self._sockets.setdefault(user_id, set()).add(websocket)

    def unregister(self, user_id: int, websocket: WebSocket) -> None:
        """Forget a socket; a no-op when it was never registered."""
        sockets = self._sockets.get(user_id)
        if sockets is None:
            return
        sockets.discard(websocket)
        if not sockets:
            del self._sockets[user_id]

    def connection_count(self, user_id: int) -> int:
        """Number of open sockets for the user."""
        return len(self._sockets.get(user_id, ()))

    async def send_to_users(self, user_ids: Iterable[int], message: dict) -> None:
        """Send a JSON message to every open socket of the given users; dead sockets are dropped."""
        for user_id in set(user_ids):
            for websocket in list(self._sockets.get(user_id, ())):
                try:
                    await websocket.send_json(message)
                except (WebSocketDisconnect, RuntimeError):
                    self.unregister(user_id, websocket)


def get_connection_manager(websocket: WebSocket) -> ConnectionManager:
    """Dependency returning the application-wide connection registry (WebSocket routes)."""
    return websocket.app.state.connection_manager


def get_http_connection_manager(request: Request) -> ConnectionManager:
    """Dependency returning the application-wide connection registry (HTTP routes)."""
    return request.app.state.connection_manager
