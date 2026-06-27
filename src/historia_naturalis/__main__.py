import argparse
import os


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="historia-naturalis",
        description="Run the Historia Naturalis MCP server.",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "sse"],
        default=os.getenv("HISTORIA_TRANSPORT", "stdio"),
        help="MCP transport to use.",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("HISTORIA_HOST", "127.0.0.1"),
        help="Host for HTTP transports.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("HISTORIA_PORT", "8000")),
        help="Port for HTTP transports.",
    )
    parser.add_argument(
        "--path",
        default=os.getenv("HISTORIA_MCP_PATH", "/mcp"),
        help="HTTP MCP path for streamable HTTP transport.",
    )
    parser.add_argument(
        "--db-path",
        default=os.getenv("HISTORIA_DB_PATH", "historia_naturalis.db"),
        help="SQLite ledger path.",
    )
    args = parser.parse_args()

    os.environ["HISTORIA_TRANSPORT"] = args.transport
    os.environ["HISTORIA_HOST"] = args.host
    os.environ["HISTORIA_PORT"] = str(args.port)
    os.environ["HISTORIA_MCP_PATH"] = args.path
    os.environ["HISTORIA_DB_PATH"] = args.db_path

    from .mcp_server import app

    app.run(transport=args.transport)


if __name__ == "__main__":
    main()
