from io import BytesIO
from io import StringIO

import click
import pytest


@pytest.mark.parametrize("kind", [bytes, bytearray])
@pytest.mark.parametrize(
    ("payload", "nl", "expected"),
    [
        (b"", True, b"\n"),
        (b"X", True, b"X\n"),
        (b"", False, b""),
        (b"X", False, b"X"),
    ],
)
def test_binary_echo(kind, payload, nl, expected):
    target = BytesIO()
    click.echo(kind(payload), file=target, nl=nl)
    assert target.getvalue() == expected


@pytest.mark.parametrize("message", ["", None])
def test_text_echo(message):
    target = StringIO()
    click.echo(message, file=target)
    assert target.getvalue() == "\n"
