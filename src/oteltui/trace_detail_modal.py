from datetime import datetime

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.events import Key
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static

from oteltui.span_utils import get_span_kind_display
from oteltui.trace_store import Trace


class TraceDetailModal(ModalScreen):
    def __init__(self, trace_id: str, traces: list[Trace]):
        super().__init__()
        self.trace_id = trace_id
        self.traces = traces
        self.show_raw_json = False

    def compose(self) -> ComposeResult:
        yield Container(
            Container(
                Label(
                    f"Trace Details - {self.trace_id} ({len(self.traces)} traces)", id="modal-title"
                ),
                Horizontal(
                    Button("Toggle JSON", id="toggle-json-btn", variant="primary"),
                    Button("Close", id="close-btn", variant="error"),
                    classes="modal-buttons",
                ),
                classes="modal-header",
            ),
            ScrollableContainer(
                Static(self.format_traces_data(), id="trace-content"), classes="modal-body"
            ),
            id="modal-container",
        )

    def format_traces_data(self) -> str:
        if not self.traces:
            return "No trace data available"

        if self.show_raw_json:
            return self.format_raw_json()
        else:
            return self.format_structured_view()

    def format_raw_json(self) -> str:
        import json

        formatted = "=" * 60 + "\n"
        formatted += f"RAW JSON DATA - {self.trace_id}\n"
        formatted += "=" * 60 + "\n\n"

        try:
            traces_data = [trace.model_dump() for trace in self.traces]
            formatted += json.dumps(traces_data, indent=2, default=str)
        except Exception as e:
            formatted += f"Error formatting JSON: {str(e)}\n\n"
            formatted += str([trace.model_dump() for trace in self.traces])

        return formatted

    def format_structured_view(self) -> str:
        formatted = "=" * 60 + "\n"
        formatted += f"TRACE DETAILS - {self.trace_id}\n"
        formatted += "=" * 60 + "\n\n"

        formatted += f"Total Traces: {len(self.traces)}\n"
        formatted += f"Trace ID: {self.trace_id}\n\n"

        for i, trace in enumerate(self.traces, 1):
            formatted += f"TRACE {i}/{len(self.traces)}:\n"
            formatted += "=" * 50 + "\n"

            formatted += f"Name: {trace.name}\n"
            formatted += f"Timestamp: {trace.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"

            trace_data = trace.data
            formatted += "Type: GRPC\n\n"

            formatted += "SPAN DETAILS:\n"
            formatted += "-" * 30 + "\n"
            formatted += f"  Span ID: {trace_data.span_id}\n"
            formatted += f"  Parent Span ID: {trace_data.parent_span_id or 'None'}\n"

            start_time = trace_data.start_time
            end_time = trace_data.end_time
            duration_ns = trace_data.duration_ns

            if start_time:
                start_dt = datetime.fromtimestamp(start_time / 1_000_000_000)
                formatted += f"  Start Time: {start_dt.strftime('%H:%M:%S.%f')[:-3]} UTC\n"

            if end_time:
                end_dt = datetime.fromtimestamp(end_time / 1_000_000_000)
                formatted += f"  End Time: {end_dt.strftime('%H:%M:%S.%f')[:-3]} UTC\n"

            if duration_ns > 0:
                if duration_ns < 1_000:  # < 1μs
                    formatted += f"  Duration: {duration_ns} ns\n"
                elif duration_ns < 1_000_000:  # < 1ms
                    formatted += f"  Duration: {duration_ns / 1_000:.2f} μs\n"
                elif duration_ns < 1_000_000_000:  # < 1s
                    formatted += f"  Duration: {duration_ns / 1_000_000:.2f} ms\n"
                else:  # >= 1s
                    formatted += f"  Duration: {duration_ns / 1_000_000_000:.3f} s\n"

            kind = trace_data.kind
            formatted += f"  Kind: {get_span_kind_display(kind, trace_data.attributes)}\n"

            status = trace_data.status_code
            status_names = {0: "UNSET", 1: "OK", 2: "ERROR"}
            formatted += f"  Status: {status_names.get(status, f'UNKNOWN({status})')}\n"

            if trace_data.status_message:
                formatted += f"  Status Message: {trace_data.status_message}\n"

            attributes = trace_data.attributes
            if attributes:
                formatted += "\n  ATTRIBUTES:\n"
                for key, value in attributes.items():
                    formatted += f"    {key}: {value}\n"

            events = trace_data.events
            if events:
                formatted += f"\n  EVENTS ({len(events)}):\n"
                for j, event in enumerate(events, 1):
                    formatted += f"    Event {j}: {event.name}\n"

            links = trace_data.links
            if links:
                formatted += f"\n  LINKS ({len(links)}):\n"
                for j, link in enumerate(links, 1):
                    formatted += f"    Link {j}: {link.trace_id}\n"

            if i < len(self.traces):
                formatted += "\n\n"

        return formatted

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close-btn":
            self.dismiss()
        elif event.button.id == "toggle-json-btn":
            self.show_raw_json = not self.show_raw_json
            # Update the content
            content = self.query_one("#trace-content", Static)
            content.update(self.format_traces_data())

    def on_key(self, event: Key) -> None:
        if event.key == "escape":
            self.dismiss()
