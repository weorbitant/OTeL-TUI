import asyncio

from grpc import aio as aio_grpc
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2_grpc

from oteltui.trace_service_servicer import TraceServiceServicer


class TraceServer:
    host: str
    port: int
    server: aio_grpc.Server | None
    is_running: bool
    trace_servicer: TraceServiceServicer

    def __init__(
        self, trace_servicer: TraceServiceServicer, host: str = "localhost", port: int = 4317
    ):
        self.host = host
        self.port = port
        self.server = None
        self.is_running = False
        self.trace_servicer = trace_servicer

    async def start(self) -> None:
        if self.is_running:
            return

        self.server = aio_grpc.server()
        trace_service_pb2_grpc.add_TraceServiceServicer_to_server(self.trace_servicer, self.server)

        listen_addr = f"{self.host}:{self.port}"
        self.server.add_insecure_port(listen_addr)

        self.is_running = True
        await self.server.start()

        try:
            await self.server.wait_for_termination()
        except asyncio.CancelledError:
            await self.stop()
        except Exception:
            pass

    async def stop(self) -> None:
        if self.server and self.is_running:
            await self.server.stop(grace=5)
            self.is_running = False
