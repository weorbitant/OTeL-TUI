from textual import work
from textual.app import App
from textual.worker import Worker

from oteltui.main_screen import MainScreen
from oteltui.models import TraceData
from oteltui.trace_server import TraceServer
from oteltui.trace_service_servicer import TraceServiceServicer
from oteltui.trace_store import TraceStore


class OtelTUIApp(App):
    CSS_PATH = "style.css"

    trace_server: TraceServer | None = None
    server_worker: Worker | None = None
    trace_store: TraceStore = TraceStore()
    trace_servicer: TraceServiceServicer | None = None

    def on_mount(self) -> None:
        self.main_screen = MainScreen(trace_store=self.trace_store)
        self.push_screen(self.main_screen)

    @work(exclusive=True)  # type: ignore[misc]
    async def run_trace_server(self) -> None:
        if self.trace_servicer is None:
            self.trace_servicer = TraceServiceServicer(self.on_receive_trace)
        if self.trace_server is None:
            self.trace_server = TraceServer(self.trace_servicer)
        await self.trace_server.start()

    def start_server(self) -> None:
        if self.server_worker is None or self.server_worker.is_finished:
            self.server_worker = self.run_trace_server()

    def stop_server(self) -> None:
        if self.server_worker and not self.server_worker.is_finished:
            self.server_worker.cancel()

    def on_receive_trace(self, trace_data: TraceData) -> None:
        self.trace_store.add_trace_data(trace_data)
        self.main_screen.update_traces_display()


def main() -> None:
    app: OtelTUIApp = OtelTUIApp()
    app.run()


if __name__ == "__main__":
    main()
