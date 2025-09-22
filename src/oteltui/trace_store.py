from datetime import datetime

from pydantic import BaseModel

from oteltui.models import SpanInfo, TraceData


class Trace(BaseModel):
    name: str
    timestamp: datetime
    data: SpanInfo
    span_id: str


def _nanoseconds_to_datetime(nanoseconds: int) -> datetime:
    """Convert nanoseconds timestamp to datetime with microsecond precision."""
    seconds = nanoseconds // 1_000_000_000
    microseconds = (nanoseconds % 1_000_000_000) // 1_000
    return datetime.fromtimestamp(seconds).replace(microsecond=microseconds)


class TraceStore(dict[str, list[Trace]]):
    def add_trace_data(self, trace_data: TraceData) -> None:
        for span in trace_data.spans:
            trace_id = span.trace_id
            trace = Trace(
                name=span.name,
                timestamp=_nanoseconds_to_datetime(span.start_time),
                data=span,
                span_id=span.span_id,
            )

            if trace_id not in self:
                self[trace_id] = []

            self[trace_id].append(trace)
            self[trace_id].sort(key=lambda x: x.timestamp, reverse=True)
