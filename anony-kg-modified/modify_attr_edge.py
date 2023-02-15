import argparse
import logging

import anonygraph.utils.runner as rutils
import anonygraph.utils.data as dutils

logger = logging.getLogger(__file__)

def add_arguments(parser):
    rutils.add_attr_edge_argument(parser)
    rutils.add_campaign_argument(parser)
    rutils.add_log_argument(parser)


def main(args):
    logger.info(args)

    dutils.modify_attribute_edge(args["owner"], args["attr"], args["value"], args["campaign"])
    logger.info("Modified attribute edge {} ---[{}]--> {} for campaign {}".format(args["owner"], args["attr"], args["value"], args["campaign"]))


if __name__ == "__main__":
    args = rutils.setup_arguments(add_arguments)
    rutils.setup_console_logging(args)
    main(args)