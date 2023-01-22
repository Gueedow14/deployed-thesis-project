import argparse
import logging

import anonygraph.utils.runner as rutils
import anonygraph.utils.data as dutils

logger = logging.getLogger(__file__)

def add_arguments(parser):
    rutils.add_owner_argument(parser)
    rutils.add_log_argument(parser)


def main(args):
    logger.info(args)
    dutils.generate_owner(args["owner"], args["pwd"], args["kval"], args["campaign"])
    logger.info("created owner {}".format(args["owner"]))


if __name__ == "__main__":
    args = rutils.setup_arguments(add_arguments)
    rutils.setup_console_logging(args)
    main(args)
