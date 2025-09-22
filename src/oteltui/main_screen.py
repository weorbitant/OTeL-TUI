from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Static, Tree

from oteltui.span_utils import get_span_kind_emoji
from oteltui.trace_detail_modal import TraceDetailModal
from oteltui.trace_store import TraceStore


class MainScreen(Screen):
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]

    server_status = reactive("stopped")
    trace_store: TraceStore

    def __init__(
        self,
        trace_store: TraceStore,
    ):
        super().__init__()
        self.trace_store = trace_store

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Vertical(
                Container(
                    Label("OpenTelemetry TUI", id="title"),
                    Static(
                        f"Server: {self.server_status} | Traces: {sum(len(traces) for traces in self.trace_store.values())}",
                        id="stats",
                    ),
                    Horizontal(
                        Button("Start Monitoring", id="start-btn", variant="success"),
                        Button("Stop Monitoring", id="stop-btn", variant="error"),
                        Button("Clear Data", id="clear-btn", variant="warning"),
                        classes="button-row",
                    ),
                    Static("😪 Ready to monitor OpenTelemetry traces via gRPC...", id="status"),
                    id="control-panel",
                ),
                Container(
                    Label("Received Traces", id="traces-title"),
                    Tree("Traces", id="traces-tree"),
                    id="traces-container",
                ),
            )
        )
        yield Footer()

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        if event.node.tree.id == "traces-tree":
            try:
                node_data = event.node.data
                if node_data and "trace_id" in node_data:
                    trace_id = node_data["trace_id"]

                    if trace_id in self.trace_store:
                        if "span_id" in node_data:
                            span_id = node_data["span_id"]
                            all_traces = self.trace_store[trace_id]
                            specific_trace = next(
                                (t for t in all_traces if t.span_id == span_id), None
                            )
                            if specific_trace:
                                self.app.push_screen(TraceDetailModal(trace_id, [specific_trace]))
                        else:
                            traces = sorted(self.trace_store[trace_id], key=lambda t: t.timestamp)
                            self.app.push_screen(TraceDetailModal(trace_id, traces))
            except Exception:
                pass

    def watch_server_status(self, status: str) -> None:
        try:
            stats = self.query_one("#stats", Static)
            total_traces = sum(len(traces) for traces in self.trace_store.values())
            stats.update(f"Server: {status} | Traces: {total_traces}")
        except Exception:
            pass

    def update_traces_display(self) -> None:
        try:
            traces_tree = self.query_one("#traces-tree", Tree)
            traces_tree.clear()

            for trace_id, traces in self.trace_store.items():
                trace_node = traces_tree.root.add(
                    f"{trace_id} - {traces[-1].name}", data={"trace_id": trace_id}
                )
                for trace in traces:
                    kind_emoji = get_span_kind_emoji(trace.data.kind, trace.data.attributes)
                    trace_node.add_leaf(
                        f"[{trace.timestamp.strftime('%H:%M:%S.%f')[:-3]}]  {kind_emoji}  {trace.name}",
                        data={"trace_id": trace_id, "span_id": trace.span_id},
                    )
        except Exception:
            pass

    def action_toggle_dark(self) -> None:
        self.app.dark = not self.app.dark

    def action_quit(self) -> None:
        self.app.exit()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        status = self.query_one("#status", Static)

        if event.button.id == "start-btn":
            from oteltui.main import OtelTUIApp

            if isinstance(self.app, OtelTUIApp):
                self.app.start_server()
                self.server_status = "running"
                status.update("😄 gRPC server started on localhost:4317")
        elif event.button.id == "stop-btn":
            from oteltui.main import OtelTUIApp

            if isinstance(self.app, OtelTUIApp):
                self.app.stop_server()
                self.server_status = "stopped"
                status.update("😐 Server stopped.")
        elif event.button.id == "clear-btn":
            self.trace_store.clear()
            self.update_traces_display()
            status.update("Traces cleared.")
