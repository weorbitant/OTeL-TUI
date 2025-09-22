from typing import Any


def _is_http_span(attributes: dict[str, Any]) -> bool:
    http_attrs = ["http.method", "http.url", "http.scheme", "http.status_code", "http.target"]
    return any(attr in attributes for attr in http_attrs)


def _is_db_span(attributes: dict[str, Any]) -> bool:
    db_attrs = ["db.system", "db.statement", "db.operation", "db.name", "db.connection_string"]
    return any(attr in attributes for attr in db_attrs)


def _is_messaging_span(attributes: dict[str, Any]) -> bool:
    messaging_attrs = ["messaging.system", "messaging.destination", "messaging.operation"]
    return any(attr in attributes for attr in messaging_attrs)


def _is_rpc_span(attributes: dict[str, Any]) -> bool:
    rpc_attrs = ["rpc.system", "rpc.service", "rpc.method"]
    return any(attr in attributes for attr in rpc_attrs)


def _is_file_span(attributes: dict[str, Any]) -> bool:
    file_attrs = ["file.path", "file.name"]
    return any(attr in attributes for attr in file_attrs)


def _get_specific_emoji(attributes: dict[str, Any]) -> str | None:
    if _is_http_span(attributes):
        return "🌐"  # HTTP requests
    elif _is_db_span(attributes):
        return "🗄️"  # Database operations
    elif _is_messaging_span(attributes):
        return "💬"  # Messaging operations
    elif _is_rpc_span(attributes):
        return "🔗"  # RPC operations
    elif _is_file_span(attributes):
        return "📁"  # File operations
    return None


def get_span_kind_emoji(kind: int, attributes: dict[str, Any] | None = None) -> str:
    if attributes:
        specific_emoji = _get_specific_emoji(attributes)
        if specific_emoji:
            return specific_emoji

    kind_emojis = {
        0: "❓",  # UNSPECIFIED
        1: "⚙️",  # INTERNAL
        2: "🖥️",  # SERVER
        3: "📱",  # CLIENT
        4: "📤",  # PRODUCER
        5: "📥",  # CONSUMER
    }
    return kind_emojis.get(kind, "❓")


def get_span_kind_name(kind: int) -> str:
    kind_names = {
        0: "UNSPECIFIED",
        1: "INTERNAL",
        2: "SERVER",
        3: "CLIENT",
        4: "PRODUCER",
        5: "CONSUMER",
    }
    return kind_names.get(kind, f"UNKNOWN({kind})")


def get_span_kind_display(kind: int, attributes: dict[str, Any] | None = None) -> str:
    emoji = get_span_kind_emoji(kind, attributes)
    name = get_span_kind_name(kind)
    return f"{emoji} {name}"
