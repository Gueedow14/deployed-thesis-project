#import networkx as nx
import logging
import os
import anonygraph.utils.data as data


from .static_graph import StaticGraph

logger = logging.getLogger(__name__)

class AnonyThGraph(StaticGraph):

    @staticmethod
    def from_raw_file(data_dir, args):

        graph = StaticGraph()

        campaignId = data.get_campaign_id(args["campaign"])

        owners = data.get_owners_from_campaign_id(campaignId)

        attrEdges = data.load_all_attr_edges()
        relEdges = data.load_all_rel_edges()

        for owner in owners:
            for attrEdge in attrEdges:
                edgeData = attrEdge.split(",")
                if edgeData[0] == owner:
                    graph.add_attribute_edge(data.get_owner_from_id(edgeData[0]) , data.get_attribute_from_id(edgeData[1]) , data.get_value_from_id(edgeData[2]))

        for owner in owners:
            for relEdge in relEdges:
                edgeData = relEdge.split(",")
                if edgeData[0] == owner:
                    graph.add_relationship_edge(data.get_owner_from_id(edgeData[0]) , data.get_relationship_from_id(edgeData[1]) , data.get_owner_from_id(edgeData[2]))

        return graph
