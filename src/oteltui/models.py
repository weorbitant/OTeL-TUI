from typing import Any

from pydantic import BaseModel


class TraceMetadata(BaseModel):
    grpc_method: str
    content_type: str


class EventInfo(BaseModel):
    time_unix_nano: int
    name: str
    attributes: dict[str, Any]
    dropped_attributes_count: int


class LinkInfo(BaseModel):
    trace_id: str
    span_id: str
    trace_state: str
    attributes: dict[str, Any]
    dropped_attributes_count: int
    flags: int


class ScopeInfo(BaseModel):
    name: str
    version: str
    attributes: dict[str, Any]
    dropped_attributes_count: int
    schema_url: str


class SpanInfo(BaseModel):
    trace_id: str
    span_id: str
    parent_span_id: str | None
    name: str
    kind: int
    status_code: int
    status_message: str
    start_time: int
    end_time: int
    duration_ns: int
    attributes: dict[str, Any]
    events: list[EventInfo]
    links: list[LinkInfo]
    dropped_attributes_count: int
    dropped_events_count: int
    dropped_links_count: int
    scope: ScopeInfo
    flags: int


class ResourceInfo(BaseModel):
    attributes: dict[str, Any]
    dropped_attributes_count: int
    schema_url: str


def _extract_attributes(attributes: Any) -> dict[str, Any]:
    attrs = {}
    for attr in attributes:
        if attr.value.HasField("string_value"):
            attrs[attr.key] = attr.value.string_value
        elif attr.value.HasField("bool_value"):
            attrs[attr.key] = attr.value.bool_value
        elif attr.value.HasField("int_value"):
            attrs[attr.key] = attr.value.int_value
        elif attr.value.HasField("double_value"):
            attrs[attr.key] = attr.value.double_value
        elif attr.value.HasField("array_value"):
            attrs[attr.key] = "[array]"  # Simplified
        elif attr.value.HasField("kvlist_value"):
            attrs[attr.key] = "[kvlist]"  # Simplified
    return attrs


class TraceData(BaseModel):
    type: str
    resources_count: int
    spans_count: int
    request_size: int
    spans: list[SpanInfo]
    resources: list[ResourceInfo]
    raw_protobuf_size: int
    metadata: TraceMetadata

    @classmethod
    def from_otel_request(cls, request: Any) -> "TraceData":
        spans_count = sum(
            len(scope_span.spans)
            for resource_span in request.resource_spans
            for scope_span in resource_span.scope_spans
        )
        resources_count = len(request.resource_spans)
        request_bytes = request.SerializeToString()

        metadata = TraceMetadata(
            grpc_method="opentelemetry.proto.collector.trace.v1.TraceService/Export",
            content_type="application/grpc+proto",
        )

        resources = []
        spans = []

        for resource_span in request.resource_spans:
            # Extract resource information
            resource_attrs = {}
            if resource_span.resource and resource_span.resource.attributes:
                resource_attrs = _extract_attributes(resource_span.resource.attributes)

            resource_info = ResourceInfo(
                attributes=resource_attrs,
                dropped_attributes_count=resource_span.resource.dropped_attributes_count
                if resource_span.resource
                else 0,
                schema_url=resource_span.schema_url,
            )
            resources.append(resource_info)

            for scope_span in resource_span.scope_spans:
                # Extract scope information
                scope_attrs = {}
                if scope_span.scope and scope_span.scope.attributes:
                    scope_attrs = _extract_attributes(scope_span.scope.attributes)

                scope_info = ScopeInfo(
                    name=scope_span.scope.name if scope_span.scope else "",
                    version=scope_span.scope.version if scope_span.scope else "",
                    attributes=scope_attrs,
                    dropped_attributes_count=scope_span.scope.dropped_attributes_count
                    if scope_span.scope
                    else 0,
                    schema_url=scope_span.schema_url,
                )

                for span in scope_span.spans:
                    # Extract span attributes, events, and links
                    span_attrs = _extract_attributes(span.attributes)

                    events = [
                        EventInfo(
                            time_unix_nano=event.time_unix_nano,
                            name=event.name,
                            attributes=_extract_attributes(event.attributes),
                            dropped_attributes_count=event.dropped_attributes_count,
                        )
                        for event in span.events
                    ]

                    links = [
                        LinkInfo(
                            trace_id=link.trace_id.hex(),
                            span_id=link.span_id.hex(),
                            trace_state=link.trace_state,
                            attributes=_extract_attributes(link.attributes),
                            dropped_attributes_count=link.dropped_attributes_count,
                            flags=link.flags,
                        )
                        for link in span.links
                    ]

                    span_info = SpanInfo(
                        trace_id=span.trace_id.hex(),
                        span_id=span.span_id.hex(),
                        parent_span_id=span.parent_span_id.hex() if span.parent_span_id else None,
                        name=span.name,
                        kind=span.kind,
                        status_code=span.status.code if span.status else 0,
                        status_message=span.status.message if span.status else "",
                        start_time=span.start_time_unix_nano,
                        end_time=span.end_time_unix_nano,
                        duration_ns=span.end_time_unix_nano - span.start_time_unix_nano
                        if span.end_time_unix_nano and span.start_time_unix_nano
                        else 0,
                        attributes=span_attrs,
                        events=events,
                        links=links,
                        dropped_attributes_count=span.dropped_attributes_count,
                        dropped_events_count=span.dropped_events_count,
                        dropped_links_count=span.dropped_links_count,
                        scope=scope_info,
                        flags=span.flags,
                    )
                    spans.append(span_info)

        return cls(
            type="grpc",
            resources_count=resources_count,
            spans_count=spans_count,
            request_size=len(request_bytes),
            spans=spans,
            resources=resources,
            raw_protobuf_size=len(request_bytes),
            metadata=metadata,
        )
