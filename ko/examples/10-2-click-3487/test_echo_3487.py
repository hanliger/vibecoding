"""Fixed expectations for the chapter's before/after comparison."""
import io
import click
import pytest


@pytest.mark.parametrize("nl", [False, True], ids=["no-newline", "newline"])
@pytest.mark.parametrize(
    "factory,payload,expected",
    [
        (io.StringIO, lambda: "", ""),
        (io.StringIO, lambda: "A", "A"),
        (io.BytesIO, lambda: b"", b""),
        (io.BytesIO, lambda: b"A", b"A"),
        (io.BytesIO, lambda: bytearray(), b""),
        (io.BytesIO, lambda: bytearray(b"A"), b"A"),
        (io.StringIO, lambda: None, ""),
        (io.StringIO, lambda: 0, "0"),
        (io.StringIO, lambda: False, "False"),
    ],
    ids=["str-empty", "str-value", "bytes-empty", "bytes-value",
         "bytearray-empty", "bytearray-value", "none", "zero", "false"],
)
def test_echo_output(factory, payload, expected, nl):
    buffer = factory()
    newline = "\n" if isinstance(expected, str) else b"\n"
    click.echo(payload(), file=buffer, nl=nl)
    assert buffer.getvalue() == expected + (newline if nl else expected[:0])
