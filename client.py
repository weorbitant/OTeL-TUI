import asyncio
import time

import grpc
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2, trace_service_pb2_grpc
from opentelemetry.proto.common.v1 import common_pb2
from opentelemetry.proto.resource.v1 import resource_pb2
from opentelemetry.proto.trace.v1 import trace_pb2


def create_test_trace(
    trace_id: str, span_name: str, service_name: str
) -> trace_service_pb2.ExportTraceServiceRequest:
    # Create resource attributes
    resource_attributes = [
        common_pb2.KeyValue(
            key="service.name", value=common_pb2.AnyValue(string_value=service_name)
        ),
        common_pb2.KeyValue(key="service.version", value=common_pb2.AnyValue(string_value="1.0.0")),
    ]

    # Create resource
    resource = resource_pb2.Resource(attributes=resource_attributes)

    # Create span attributes
    span_attributes = [
        common_pb2.KeyValue(key="http.method", value=common_pb2.AnyValue(string_value="GET")),
        common_pb2.KeyValue(
            key="http.url",
            value=common_pb2.AnyValue(string_value=f"http://localhost:8080/{span_name.lower()}"),
        ),
        common_pb2.KeyValue(key="http.status_code", value=common_pb2.AnyValue(int_value=200)),
    ]

    # Create timestamps
    now_ns = int(time.time() * 1_000_000_000)
    start_time = now_ns - 50_000_000  # 50ms ago
    end_time = now_ns

    # Create span
    span = trace_pb2.Span(
        trace_id=bytes.fromhex(trace_id.replace("-", "")),
        span_id=bytes.fromhex("1234567890abcdef"),
        name=span_name,
        kind=trace_pb2.Span.SPAN_KIND_SERVER,
        start_time_unix_nano=start_time,
        end_time_unix_nano=end_time,
        attributes=span_attributes,
        status=trace_pb2.Status(code=trace_pb2.Status.STATUS_CODE_OK),
    )

    # Create scope span
    scope_span = trace_pb2.ScopeSpans(
        scope=common_pb2.InstrumentationScope(name="test-tracer", version="1.0.0"), spans=[span]
    )

    # Create resource span
    resource_span = trace_pb2.ResourceSpans(resource=resource, scope_spans=[scope_span])

    # Create export request
    request = trace_service_pb2.ExportTraceServiceRequest(resource_spans=[resource_span])

    return request


async def send_traces() -> None:
    print("Connecting to OpenTelemetry TUI server at localhost:4317...")

    try:
        async with grpc.aio.insecure_channel("localhost:4317") as channel:
            stub = trace_service_pb2_grpc.TraceServiceStub(channel)

            # Send first trace
            print("Sending trace 1: User Login")
            trace1 = create_test_trace(
                trace_id="12345678-1234-1234-1234-123456789abc",
                span_name="user_login",
                service_name="auth-service",
            )
            _ = await stub.Export(trace1)
            print("✓ Trace 1 sent successfully")

            # Wait a bit
            await asyncio.sleep(1)

            # Send second trace
            print("Sending trace 2: Get User Profile")
            trace2 = create_test_trace(
                trace_id="87654321-4321-4321-4321-fedcba987654",
                span_name="get_user_profile",
                service_name="user-service",
            )
            _ = await stub.Export(trace2)
            print("✓ Trace 2 sent successfully")

            print("\nBoth traces sent! Check the TUI to see them.")

    except grpc.aio.AioRpcError as e:
        print(f"Error connecting to server: {e}")
        print("Make sure the OpenTelemetry TUI is running with 'uv run oteltui'")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(send_traces())
