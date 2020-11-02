"""
This module deals with messages shown to client
"""

# suppress flag
suppress_messages = False


def warning(msg: str):
    _display_(f'warning: {msg}')


def information(msg: str):
    _display_(f'information: {msg}')


def _display_(msg: str):
    if not suppress_messages:
        print(f'electrolens: {msg}')
