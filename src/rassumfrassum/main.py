#!/usr/bin/env python3
"""
rassumfrassum - A simple LSP multiplexer that forwards JSONRPC messages.
"""

import argparse
import asyncio
import sys

from .rassum import run_multiplexer
from .util import log


def parse_server_commands(args: list[str]) -> tuple[list[str], list[list[str]]]:
    """
    Split args on '--' separators.
    Returns (rass_args, [server_command1, server_command2, ...])
    """
    if "--" not in args:
        return args, []

    # Find all '--' separator indices
    separator_indices = [i for i, arg in enumerate(args) if arg == "--"]

    # Everything before first '--' is rass options
    rass_args = args[: separator_indices[0]]

    # Split server commands
    server_commands: list[list[str]] = []
    for i, sep_idx in enumerate(separator_indices):
        # Find start and end of this server command
        start = sep_idx + 1
        end = (
            separator_indices[i + 1]
            if i + 1 < len(separator_indices)
            else len(args)
        )

        server_cmd: list[str] = args[start:end]
        if server_cmd:  # Only add non-empty commands
            server_commands.append(server_cmd)

    return rass_args, server_commands


def main() -> None:
    """
    Parse arguments and start the multiplexer.
    """
    args = sys.argv[1:]

    # Parse multiple '--' separators for multiple servers
    rass_args, server_commands = parse_server_commands(args)

    # Parse rass options with argparse
    parser = argparse.ArgumentParser(
        prog='rass',
        usage="%(prog)s [-h] [%(prog)s options] -- server1 [args...] [-- server2 ...]",
        add_help=True,
    )

    parser.add_argument(
        '--quiet-server', action='store_true', help='Suppress server\'s stderr.'
    )
    parser.add_argument(
        '--delay-ms',
        type=int,
        default=0,
        metavar='N',
        help='Delay all messages from rass by N ms.',
    )
    parser.add_argument(
        '--drop-tardy',
        action='store_true',
        help='Drop tardy messages instead of re-sending aggregations.',
    )
    parser.add_argument(
        '--logic-class',
        type=str,
        default='LspLogic',
        metavar='CLASS',
        help='Logic class to use for routing (default: LspLogic).',
    )
    opts = parser.parse_args(rass_args)

    if not server_commands:
        log(
            "Usage: rass [OPTIONS] -- <primary-server> [args] [-- <secondary-server> [args]]..."
        )
        sys.exit(1)

    # Validate
    assert opts.delay_ms >= 0, "--delay-ms must be non-negative"

    try:
        asyncio.run(run_multiplexer(server_commands, opts))
    except KeyboardInterrupt:
        log("\nShutting down...")
    except Exception as e:
        log(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
