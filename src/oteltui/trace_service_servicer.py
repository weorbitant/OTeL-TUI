from collections.abc import Callable
from typing import Any

import grpc
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2, trace_service_pb2_grpc

from oteltui.models import TraceData


class TraceServiceServicer(trace_service_pb2_grpc.TraceServiceServicer):
    def __init__(self, on_receive_trace: Callable[[TraceData], None]) -> None:
        self.on_receive_trace = on_receive_trace

    async def Export(
        self, request: Any, context: Any
    ) -> trace_service_pb2.ExportTraceServiceResponse:
        try:
            trace_data = TraceData.from_otel_request(request)
            self.on_receive_trace(trace_data)

            return trace_service_pb2.ExportTraceServiceResponse()

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error processing traces: {str(e)}")
            return trace_service_pb2.ExportTraceServiceResponse()
