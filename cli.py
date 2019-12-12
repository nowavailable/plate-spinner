# -*- coding: utf-8 -*-
import sys
import click
from plate_spinner.main_loop import main_loop

@click.command()
@click.option('--sharding_keys', required=False, type=str)
@click.option('--specified_jobnames', required=False, type=str)
@click.option('--foreground', required=False, type=bool)
def main(specified_jobnames=None, sharding_keys=None, foreground=False):

    config_path = None

    specified_jobname_list = [] if specified_jobnames is None else specified_jobnames.split("")
    sharding_key_list = [] if sharding_keys is None else sharding_keys.split("")

    main_loop(config_path, specified_jobname_list, sharding_key_list, foreground)


if __name__ == "__main__":
    main()
