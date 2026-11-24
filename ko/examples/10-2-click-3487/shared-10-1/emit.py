import click


@click.command()
@click.argument("target", type=click.File("wb"))
def emit(target):
    click.echo(b"", file=target)


if __name__ == "__main__":
    emit()
