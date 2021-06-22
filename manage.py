from pathlib import Path
import click
import uvicorn
from loguru import logger
import json
import pydash
from app import loader


@click.group()
def cli():
    pass


@click.group()
def load():
    pass


@click.group()
def generate():
    pass


@generate.command()
@click.argument("data_file", type=click.Path(exists=True))
def hospital_json(data_file="data/sample_geodetails.json"):

    data = []
    for row in json.load(open(geodetails_file)):
        data.append(row)

    json.dump(data, open("web/public/data.json", "w"))


cli.add_command(load)
cli.add_command(generate)


@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("uvicorn_args", nargs=-1, type=click.UNPROCESSED)
def runserver(uvicorn_args):
    host = "0.0.0.0"
    port = 8100
    logger.info(f"Running on {host}:{port}")
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        reload_dirs=[Path(__file__).parent / Path("app")],
        workers=2,
    )


if __name__ == "__main__":
    cli()
