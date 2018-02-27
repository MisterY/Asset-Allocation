"""
Main entry point to the library
"""
import logging
import sys

import click
import click_log

from asset_allocation import dal
from asset_allocation.app import AppAggregate
# sub-commands
from asset_allocation.assetclass_cli import ac
from asset_allocation.config import Config
from asset_allocation.config_cli import config
from asset_allocation.formatters import AsciiFormatter, HtmlFormatter
from asset_allocation.stocklink_cli import sl

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

@click.group()
@click_log.simple_verbosity_option(logger)
def cli():
    pass

@click.command()
@click.option("--format", default="ascii", help="format for the report output. ascii or html.")
                # prompt="output format")
@click.option("--full", is_flag=True, default=False, help="Display full model with securities")
@click_log.simple_verbosity_option(logger)
def show(format, full):
    """ Print current allocation to the console. """
    # load asset allocation
    app = AppAggregate()
    app.logger = logger
    model = app.get_asset_allocation_model()

    if format == "ascii":
        formatter = AsciiFormatter()
    elif format == "html":
        formatter = HtmlFormatter
    else:
        raise ValueError(f"Unknown formatter {format}")

    # formatters can display stock information with --full
    output = formatter.format(model, full=full)
    print(output)

@click.command()
def validate():
    """ validate model """
    app = AppAggregate()
    app.validate_model()


cli.add_command(ac)
cli.add_command(sl)
cli.add_command(show)
cli.add_command(config)
cli.add_command(validate)

##############################
# For debugging.
# if __name__ == '__main__':
#     show(["--format", "ascii", "--full"])
