import argparse
import logging

import anonygraph.utils.runner as rutils
import anonygraph.utils.data as dutils
import anonygraph.utils.path as putils

logger = logging.getLogger(__file__)

def add_arguments(parser):
    rutils.add_data_argument(parser)
    rutils.add_info_loss_argument(parser)
    rutils.add_clustering_argument(parser)
    rutils.add_cluster_constraint_enforcer_argument(parser)
    rutils.add_log_argument(parser)
    rutils.add_campaign_argument(parser)


def main(args):
    logger.info(args)

    attrs = dutils.load_anon_graph_attribute_edges_from_path(args["data"], args["sample"], args["campaign"], args["info_loss"], args["handler"], args["calgo"], args["enforcer"], args)
    rels = dutils.load_anon_graph_relationship_edges_from_path(args["data"], args["sample"], args["campaign"], args["info_loss"], args["handler"], args["calgo"], args["enforcer"], args)

    dutils.generate_anon_kg_file(attrs, rels, args)
    



if __name__ == "__main__":
    args = rutils.setup_arguments(add_arguments)
    rutils.setup_console_logging(args)
    main(args)