from pathlib import Path

import click

from card2vec.tools.generate_training_dataset import generate_training


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    click.echo("Debug mode is %s" % ("on" if debug else "off"))


@cli.command()
@click.argument("shuffles", type=click.INT)
@click.argument("window_size", type=click.INT)
@click.argument("negative_samples", type=click.INT)
def generate(shuffles, window_size, negative_samples):
    input_path = Path("input")
    output_path = Path("output")
    if not output_path.exists():
        output_path.mkdir(exist_ok=True)

    generate_training(input_path, output_path, shuffles, window_size, negative_samples)


if __name__ == "__main__":
    cli()
