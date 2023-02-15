import argparse
import logging

import anonygraph.utils.runner as rutils
import anonygraph.utils.data as dutils

logger = logging.getLogger(__file__)

def add_arguments(parser):
    rutils.add_campaign_argument(parser)
    rutils.add_owner_email_argument(parser)
    rutils.add_owner_kval_argument(parser)
    rutils.add_log_argument(parser)


def main(args):
    logger.info(args)

    dutils.add_campaign_owner(args["campaign"], args["owner"], args["kval"])


if __name__ == "__main__":
    args = rutils.setup_arguments(add_arguments)
    rutils.setup_console_logging(args)
    main(args)