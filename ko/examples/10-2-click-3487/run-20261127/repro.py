import io
import click

buffer = io.BytesIO()
click.echo(b"", file=buffer, nl=True)
print(repr(buffer.getvalue()))
