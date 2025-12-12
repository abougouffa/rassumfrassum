"""Python preset: basedpyright + ruff."""

def servers():
    """Return basedpyright and ruff server commands."""
    return [
        ['basedpyright-langserver', '--stdio'],
        ['ruff', 'server']
    ]




