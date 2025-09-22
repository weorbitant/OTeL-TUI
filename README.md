# 🚀 OtelTUI

> A modern Terminal User Interface (TUI) for monitoring OpenTelemetry traces in real-time. Built with Python and Textual, OtelTUI provides a clean, interactive interface for viewing and analyzing distributed traces.

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 OtelTUI - OpenTelemetry Trace Monitor                  │
├─────────────────────────────────────────────────────────────┤
│  📊 Real-time trace monitoring                             │
│  🌐 gRPC trace collection on port 4317                    │
│  🖱️  Interactive trace details                             │
│  🎨 Clean TUI interface with Textual                      │
│  🔍 Trace filtering and search                            │
│  📋 Multiple view modes (structured/raw JSON)             │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Features

- 🔄 **Real-time trace monitoring** - Watch OpenTelemetry traces as they arrive
- 🌐 **gRPC trace collection** - Receives traces via OpenTelemetry gRPC protocol on port 4317
- 🖱️ **Interactive trace details** - Click on traces to view detailed span information
- 🎨 **Clean TUI interface** - Built with Textual for a modern terminal experience
- 🔍 **Trace filtering and search** - Easily navigate through trace data
- 📋 **Multiple view modes** - Switch between structured and raw JSON views
- 🌙 **Dark mode support** - Toggle between light and dark themes
- ⚡ **High performance** - Efficient trace processing and display

## 📦 Installation

### 🚀 Using uv (recommended)

```bash
git clone https://github.com/yourusername/oteltui.git
cd oteltui
uv sync
```

### 🛠️ Development Installation

For development with linting and testing tools:

```bash
git clone https://github.com/yourusername/oteltui.git
cd oteltui
uv sync --extra dev
uv run pre-commit install
```

### 📋 Using pip

```bash
git clone https://github.com/yourusername/oteltui.git
cd oteltui
pip install -e .
```

## 🚀 Usage

### 🎯 Quick Start

```bash
# Using uv
uv run oteltui

# Or if installed globally
oteltui
```

The TUI will start and listen for OpenTelemetry traces on `localhost:4317`.

### 📡 Sending traces

Configure your OpenTelemetry instrumented application to send traces to:
- **Endpoint**: `localhost:4317`
- **Protocol**: gRPC (OpenTelemetry Protocol)
- **Transport**: HTTP/2 (gRPC)

### 🧪 Test with the included client

```bash
# Start the TUI in one terminal
uv run oteltui

# In another terminal, send test traces
uv run python client.py
```


## 🛠️ Development

### 🚀 Setup

```bash
git clone https://github.com/yourusername/oteltui.git
cd oteltui
uv sync --extra dev
```

### 🔍 Code quality

```bash
# Run all pre-commit hooks
uv run pre-commit run --all-files

# Individual tools
uv run ruff format      # Format code
uv run ruff check       # Lint code
uv run mypy src/        # Type checking
uv run black src/       # Alternative formatter
```

### 🏗️ Project Structure

```
oteltui/
├── 📁 src/oteltui/          # Main source code
├── 📁 tests/                # Test files
├── 📁 docs/                 # Documentation
├── 📄 pyproject.toml        # Project configuration
├── 📄 README.md             # This file
└── 📄 client.py             # Test client
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### 🎯 How to Contribute

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔄 Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- 🌐 [OpenTelemetry](https://opentelemetry.io/) - Observability framework
- 🎨 [Textual](https://textual.textualize.io/) - Python TUI framework
- 🔍 [Jaeger](https://www.jaegertracing.io/) - Distributed tracing platform
- 📊 [Grafana](https://grafana.com/) - Monitoring and observability
- 🐛 [Sentry](https://sentry.io/) - Error tracking and performance monitoring

## 🆘 Support

If you encounter any issues or have questions:

1. 🔍 Check the [existing issues](https://github.com/yourusername/oteltui/issues)
2. 🆕 Create a new issue with details about your problem
3. 📋 Include your Python version and operating system
4. 📝 Provide logs and error messages

## 🗺️ Roadmap

- [ ] 🔍 **Trace search and filtering** - Advanced search capabilities
- [ ] 📤 **Export/import functionality** - Export/import traces to/from various formats
- [ ] 🌐 **Multiple protocol support**
- [ ] 📊 **Performance metrics and statistics** - Real-time performance data

## 🏆 Acknowledgments

- 🙏 Thanks to the [OpenTelemetry](https://opentelemetry.io/) community
- 🎨 Thanks to [Textual](https://textual.textualize.io/) for the amazing TUI framework
- 💡 Inspired by [Jaeger UI](https://www.jaegertracing.io/) and other tracing tools
