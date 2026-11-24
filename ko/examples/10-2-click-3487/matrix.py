import io
import json
import click

rows = []
for label, factory, payload in [
    ('str-empty', io.StringIO, lambda: ''),
    ('str-value', io.StringIO, lambda: 'A'),
    ('bytes-empty', io.BytesIO, lambda: b''),
    ('bytes-value', io.BytesIO, lambda: b'A'),
    ('bytearray-empty', io.BytesIO, lambda: bytearray()),
    ('bytearray-value', io.BytesIO, lambda: bytearray(b'A')),
    ('none', io.StringIO, lambda: None),
    ('zero', io.StringIO, lambda: 0),
    ('false', io.StringIO, lambda: False),
]:
    for nl in [False, True]:
        buffer = factory()
        try:
            click.echo(payload(), file=buffer, nl=nl)
            result = {'output': repr(buffer.getvalue()), 'error': None}
        except Exception as e:
            result = {'output': repr(buffer.getvalue()), 'error': f'{type(e).__name__}: {e}'}
        rows.append({'case': label, 'nl': nl, **result})
print(json.dumps(rows, indent=2))
