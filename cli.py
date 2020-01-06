# -*- coding: utf-8 -*-
import os
import click
from plate_spinner.main_loop import main_loop

@click.command()
@click.option('--sharding_keys', required=False, type=str)
@click.option('--specified_jobnames', required=False, type=str)
@click.option('--start_with_jobs', required=False, type=bool)
@click.option('--foreground', required=False, type=bool)
def main(specified_jobnames=None, sharding_keys=None, start_with_jobs=False, foreground=False):
    config_path = os.path.join(os.getcwd(), "config", "operations.yml")
    specified_jobname_list = [] if specified_jobnames is None else specified_jobnames.split("")
    sharding_key_list = [] if sharding_keys is None else sharding_keys.split("")

    main_loop(
        config_path=config_path,
        specified_jobnames=specified_jobname_list,
        start_with_jobs=start_with_jobs,
        sharding_keys=sharding_key_list
    )


if __name__ == "__main__":
    main()
