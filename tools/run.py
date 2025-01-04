from datetime import datetime as dt
from pathlib import Path

import click
from loguru import logger

from llm_engineering import settings
import pipelines

@click.command(
    help="""

        TwinLLM Project command line.

        Run ZenML pipelines with various options.

        Examples:


        \b
        #Run with default parameters
        python3 run.py


        \b
        #Run with caching disabled
        python3 run.py --no-cache


        \b
        #Run only etl pipeline
        python3 run.py --only-etl


    """
)
@click.option(
    "--no-cache",
    is_flag=True,
    default=False,
    help="Disable cache for the pipeline."
)
@click.option(
    "--run-etl",
    is_flag=True,
    default=False,
    help="Run ETL pipline"
)
@click.option(
    "--etl-config-filename",
    default="digital_data_etl_test.yaml",
    help="File name of the ETL config file"
)
def main(
    no_cache: bool = False,
    run_etl: bool = False,
    etl_config_filename: str = "digital_data_etl_test.yaml") -> None:

        assert (
            run_etl
        ), "Specify action to be taken."

        pipeline_arg = {
            "enable_cache": not no_cache
        }

        root_dir = Path(__file__).resolve().parent.parent

        if run_etl:
            run_args_etl = {}
            pipeline_arg["config_path"] = root_dir/"configs"/etl_config_filename
            assert pipeline_arg["config_path"].exists(), f"Config file not found: {etl_config_filename}"
            pipeline_arg["run_name"] = f"digital_data_etl_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
            pipelines.digital_data_etl.with_options(**pipeline_arg)(**run_args_etl)

if __name__ == "__main__":

    main()
            
    