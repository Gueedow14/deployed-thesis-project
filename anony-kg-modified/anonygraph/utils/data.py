import os
from anonygraph import algorithms
import logging
import numpy as np

import anonygraph.data as data
import anonygraph.utils.path as putils


logger = logging.getLogger(__name__)


def load_graph_from_raw_data(data_name, sample, args):
    raw_dir = putils.get_raw_data_path(data_name)
    data_fn_dict = {
        # "email-temp": data.EmailTempGraph,
        "dummy": data.DummyGraph,
        # "yago": data.YagoGraph,
        # "icews14": data.ICEWS14Graph,
        # "dblp": data.DBLPGraph,
        "freebase": data.FreebaseGraph,
        # "gplus": data.GplusGraph,
        "email": data.EmailGraph,
        "yago": data.YagoGraph,
        "anonykg_thesis": data.AnonyThGraph,
    }

    data_fn = data_fn_dict.get(data_name)
    if data_fn is not None:
        graph = data_fn.from_raw_file(raw_dir, args)
    else:
        raise NotImplementedError("Unsupported graph: {}".format(data_name))

    return graph




def countLines(file):
    with open(file, 'r') as fp:
        lines = len(fp.readlines())
    return lines + 1




def get_campaign_id(campaign):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    campaigns_file = os.path.join(raw_dir, "campaigns.idx")
    with open(campaigns_file, 'r') as fp:
        for row in fp.readlines():
            if row.split(",")[0] == campaign:
                return row.split(",")[2][:-1]

def get_attr_id(attr):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    attrs_file = os.path.join(raw_dir, "attrs.idx")
    with open(attrs_file, 'r') as fp:
        for row in fp.readlines():
            if row.split(",")[0] == attr:
                return row.split(",")[1][:-1]

def get_rel_id(rel):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    rels_file = os.path.join(raw_dir, "rels.idx")
    with open(rels_file, 'r') as fp:
        for row in fp.readlines():
            if row.split(",")[0] == rel:
                return row.split(",")[1][:-1]

def get_value_id(val):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    values_file = os.path.join(raw_dir, "values.idx")
    with open(values_file, 'r') as fp:
        for row in fp.readlines():
            if row.split(",")[0] == val:
                return row.split(",")[1][:-1]

def get_owner_id(owner):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    owners_file = os.path.join(raw_dir, "owners.idx")
    with open(owners_file, 'r') as fp:
        for row in fp.readlines():
            if row.split(",")[0] == owner:
                return row.split(",")[4][:-1]

def get_provider_id(provider):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    providers_file = os.path.join(raw_dir, "providers.idx")
    with open(providers_file, 'r') as fp:
        for row in fp.readlines():
            if row.split(",")[0] == provider:
                return row.split(",")[2][:-1]




def generate_owner(email, pwd, k, campaign):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    owners_file = os.path.join(raw_dir, "owners.idx")
    num_lines = countLines(owners_file)

    chkExist = False

    with open(owners_file, "r") as f:
        for row in f.readlines():
            row_values = row.split(",")
            if row_values[0] == email:
                chkExist = True

    if chkExist == False:
        f = open(owners_file, "a")
        new_owner = email + "," + pwd + "," + str(k) + "," + get_campaign_id(campaign) + "," + str(num_lines) + "\n"
        f.write(new_owner)
        f.close()
        logger.info("created owner {}".format(email))
    else:
        logger.info("owner {} already exists".format(email))


def generate_provider(email, pwd):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    providers_file = os.path.join(raw_dir, "providers.idx")
    num_lines = countLines(providers_file)

    chkExist = False

    with open(providers_file, "r") as f:
        for row in f.readlines():
            row_values = row.split(",")
            if row_values[0] == email:
                chkExist = True

    if chkExist == False:
        f = open(providers_file, "a")
        new_provider = email + "," + pwd + "," + str(num_lines) + "\n"
        f.write(new_provider)
        f.close()
        logger.info("created provider {}".format(email))
    else:
        logger.info("provider {} already exists".format(email))


def generate_campaign(campaign, creator):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    campaigns_file = os.path.join(raw_dir, "campaigns.idx")
    num_lines = countLines(campaigns_file)

    chkExist = False

    with open(campaigns_file, "r") as f:
        for row in f.readlines():
            row_values = row.split(",")
            if row_values[0] == campaign:
                chkExist = True

    if chkExist == False:
        f = open(campaigns_file, "a")
        new_campaign = campaign + "," + get_provider_id(creator) + "," + str(num_lines) + "\n"
        f.write(new_campaign)
        f.close()
        logger.info("created campaign {}".format(campaign))
    else:
        logger.info("campaign {} already exists".format(campaign))


def generate_campaign_attrs(campaign, attrs):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    campaign_attrs_file = os.path.join(raw_dir, "campaign_attrs.idx")

    chkExist = False

    with open(campaign_attrs_file, "r") as f:
        for row in f.readlines():
            row_values = row.split(":")
            if row_values[0] == get_campaign_id(campaign):
                chkExist = True

    if chkExist == True:
        with open(campaign_attrs_file, "r") as f:
            lines = f.readlines()
        with open(campaign_attrs_file, "w") as f:
            pass
        with open(campaign_attrs_file, "w") as f:
            for line in lines:
                row_values = row.split(":")
                if row_values[0] != get_campaign_id(campaign):
                    f.write(line)

    f = open(campaign_attrs_file, "a")
    new_campaign = get_campaign_id(campaign)  + ":"
    for attr in attrs:
        new_campaign += get_attr_id(attr + "_attr") + ","
    new_campaign = new_campaign[:-1]
    f.write(new_campaign)
    f.close()

def generate_campaign_rels(campaign, rels):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    campaign_rels_file = os.path.join(raw_dir, "campaign_rels.idx")

    chkExist = False

    with open(campaign_rels_file, "r") as f:
        for row in f.readlines():
            row_values = row.split(":")
            if row_values[0] == get_campaign_id(campaign):
                chkExist = True

    if chkExist == True:
        with open(campaign_rels_file, "r") as f:
            lines = f.readlines()
        with open(campaign_rels_file, "w") as f:
            pass
        with open(campaign_rels_file, "w") as f:
            for line in lines:
                row_values = row.split(":")
                if row_values[0] != get_campaign_id(campaign):
                    f.write(line)

    f = open(campaign_rels_file, "a")
    new_campaign = get_campaign_id(campaign) + ":"
    for rel in rels:
        new_campaign += get_rel_id(rel + "_rel") + ","
    new_campaign = new_campaign[:-1]
    f.write(new_campaign)
    f.close()

def generate_value(value):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    values_file = os.path.join(raw_dir, "values.idx")
    num_lines = countLines(values_file)

    chkExist = False

    with open(values_file, "r") as f:
        for row in f.readlines():
            row_values = row.split(",")
            if row_values[0] == value:
                chkExist = True

    if chkExist == False:
        f = open(values_file, "a")
        new_value = value  + "," + str(num_lines) + "\n"
        f.write(new_value)
        f.close()
        logger.info("created value {}".format(value))
    else:
        logger.info("value {} already exists".format(value))


def generate_relationship(rel):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    rels_file = os.path.join(raw_dir, "rels.idx")
    attrs_file = os.path.join(raw_dir, "attrs.idx")
    num_lines = countLines(rels_file) + countLines(attrs_file) - 1

    chkExist = False

    with open(rels_file, "r") as f:
        for row in f.readlines():
            row_values = row.split(",")
            if row_values[0] == (rel + "_rel"):
                chkExist = True

    if chkExist == False:
        f = open(rels_file, "a")
        new_value = rel  + "_rel," + str(num_lines) + "\n"
        f.write(new_value)
        f.close()
        logger.info("created relationship {}".format(rel))
    else:
        logger.info("relationship {} already exists".format(rel))


def generate_attribute(attr):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    rels_file = os.path.join(raw_dir, "rels.idx")
    attrs_file = os.path.join(raw_dir, "attrs.idx")
    num_lines = countLines(rels_file) + countLines(attrs_file) - 1

    chkExist = False

    with open(attrs_file, "r") as f:
        for row in f.readlines():
            row_values = row.split(",")
            if row_values[0] == (attr + "_attr"):
                chkExist = True

    if chkExist == False:
        f = open(attrs_file, "a")
        new_value = attr  + "_attr," + str(num_lines) + "\n"
        f.write(new_value)
        f.close()
        logger.info("created attribute {}".format(attr))
    else:
        logger.info("attribute {} already exists".format(attr))


def generate_relationship_edge(owner1, rel, owner2):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    rels_file = os.path.join(raw_dir, "rels.edges")

    chkExist = False

    with open(rels_file, "r") as f:
        for row in f.readlines():
            row_values = row.split(",")
            if row_values[0] == get_owner_id(owner1) and row_values[1] == get_rel_id(rel + "_rel") and row_values[2].strip('\n') == get_owner_id(owner2):
                chkExist = True

    if chkExist == False:
        f = open(rels_file, "a")
        new_value = get_owner_id(owner1)  + "," + get_rel_id(rel + "_rel")  + "," + get_owner_id(owner2) + "\n"
        f.write(new_value)
        f.close()
        logger.info("created relationship edge {} ---[{}]--> {}".format(owner1, rel, owner2))
    else:
        logger.info("relationship edge {} ---[{}]--> {} already exists".format(owner1, rel, owner2))
    

def generate_attribute_edge(owner, attr, value):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    attrs_file = os.path.join(raw_dir, "attrs.edges")

    chkExist = False

    with open(attrs_file, "r") as f:
        for row in f.readlines():
            row_values = row.split(",")
            if row_values[0] == get_owner_id(owner) and row_values[1] == get_attr_id(attr + "_attr") and row_values[2].strip('\n') == get_value_id(value):
                chkExist = True

    if chkExist == False:
        f = open(attrs_file, "a")
        new_value = get_owner_id(owner)  + "," + get_attr_id(attr + "_attr")  + "," + get_value_id(value) + "\n"
        f.write(new_value)
        f.close()
        logger.info("created attribute edge {} ---[{}]--> {}".format(owner, attr, value))
    else:
        logger.info("attribute edge {} ---[{}]--> {} already exists".format(owner, attr, value))



def reset_pwd_owner(email, pwd, k, campaign):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    owners_file = os.path.join(raw_dir, "owners.idx")
    tmp_file = os.path.join(raw_dir, "tmp.idx")

    with open(owners_file, "r") as f_input:
        with open(tmp_file, "w") as f_output:
            for count, row in enumerate(f_input.readlines()):
                if row.split(",")[0] == email:
                    new_data = email + "," + pwd + "," + str(k) + "," + get_campaign_id(campaign) + "," + str(count+1) + "\n"
                    row = new_data
                f_output.write(row)

    os.replace(tmp_file, owners_file)

def reset_pwd_provider(email, pwd):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    providers_file = os.path.join(raw_dir, "providers.idx")
    tmp_file = os.path.join(raw_dir, "tmp.idx")

    with open(providers_file, "r") as f_input:
        with open(tmp_file, "w") as f_output:
            for count, row in enumerate(f_input.readlines()):
                if row.split(",")[0] == email:
                    new_data = email + "," + pwd + "," + str(count+1) + "\n"
                    row = new_data
                f_output.write(row)

    os.replace(tmp_file, providers_file)




def modify_attribute_edge(owner, attr, value):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    attrs_file = os.path.join(raw_dir, "attrs.edges")
    tmp_file = os.path.join(raw_dir, "tmp.idx")
    
    with open(attrs_file, "r") as f_input:
        with open(tmp_file, "w") as f_output:
            for row in f_input.readlines():
                if row.split(",")[0] == get_owner_id(owner) and row.split(",")[1] == get_attr_id(attr + "_attr"):
                    new_data = get_owner_id(owner) + "," + get_attr_id(attr + "_attr") + "," + get_value_id(value) + "\n"
                    row = new_data
                f_output.write(row)

    os.replace(tmp_file, attrs_file)



def delete_rel_edge(o1, rel, o2):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    rels_file = os.path.join(raw_dir, "rels.edges")
    tmp_file = os.path.join(raw_dir, "tmp.idx")

    chkExist = False

    with open(rels_file, "r") as f:
        for row in f.readlines():
            row_values = row.split(",")
            if row_values[0] == get_owner_id(o1) and row_values[1] == get_rel_id(rel + "_rel") and row_values[2].strip('\n') == get_owner_id(o2):
                chkExist = True

    if chkExist == True:
        text2del = get_owner_id(o1) + "," + get_rel_id(rel + "_rel") + "," + get_owner_id(o2)

        with open(rels_file, "r") as f_input:
            with open(tmp_file, "w") as f_output:
                for row in f_input.readlines():
                    if row.strip("\n") != text2del:
                        f_output.write(row)

        os.replace(tmp_file, rels_file)
        logger.info("deleted relationship edge {} ---[{}]--> {}".format(o1,rel,o2))
    else:
        logger.info("relationship edge {} ---[{}]--> {} already deleted".format(o1,rel,o2))



def load_all_attr_edges():
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    attrs_file = os.path.join(raw_dir, "attrs.edges")

    attrEdges = []

    with open(attrs_file, "r") as f:
        for row in f.readlines():
            attrEdges.append(row.strip("\n"))

    f.close()

    return attrEdges



def load_all_rel_edges():
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    rels_file = os.path.join(raw_dir, "rels.edges")

    relEdges = []

    with open(rels_file, "r") as f:
        for row in f.readlines():
            relEdges.append(row.strip("\n"))

    f.close()

    return relEdges


def load_all_kvals(campaign):
    raw_dir = putils.get_campaign_output_path("anonykg_thesis", "-1", campaign)
    rels_file = os.path.join(raw_dir, "k_values", campaign.replace(" ", "_") + ".txt")

    kvals = []

    with open(rels_file, "r") as f:
        for row in f.readlines():
            kval = row.split(",")[1]
            kvals.append(int(kval.strip("\n")))

    f.close()

    return kvals



def get_owner_from_id(ownerId):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    owners_file = os.path.join(raw_dir, "owners.idx")

    with open(owners_file, "r") as f:
        for row in f.readlines():
            rowData = row.split(",")
            if rowData[4].strip("\n") == ownerId:
                return rowData[0]

def get_kval_from_id(ownerId):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    owners_file = os.path.join(raw_dir, "owners.idx")

    with open(owners_file, "r") as f:
        for row in f.readlines():
            rowData = row.split(",")
            if rowData[4].strip("\n") == ownerId:
                return rowData[2]

def get_attribute_from_id(attrId):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    owners_file = os.path.join(raw_dir, "attrs.idx")

    with open(owners_file, "r") as f:
        for row in f.readlines():
            rowData = row.split(",")
            if rowData[1].strip("\n") == attrId:
                size = len(rowData[0])
                attr = rowData[0][:size - 5]
                return attr

def get_relationship_from_id(relId):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    owners_file = os.path.join(raw_dir, "rels.idx")

    with open(owners_file, "r") as f:
        for row in f.readlines():
            rowData = row.split(",")
            if rowData[1].strip("\n") == relId:
                size = len(rowData[0])
                rel = rowData[0][:size - 4]
                return rel

def get_value_from_id(valueId):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    owners_file = os.path.join(raw_dir, "values.idx")

    with open(owners_file, "r") as f:
        for row in f.readlines():
            rowData = row.split(",")
            if rowData[1].strip("\n") == valueId:
                return rowData[0]


def get_owners_from_campaign_id(campaignId):
    raw_dir = putils.get_raw_data_path("anonykg_thesis")
    owners_file = os.path.join(raw_dir, "owners.idx")

    owners = []

    with open(owners_file, "r") as f:
        for row in f.readlines():
            rowData = row.split(",")
            if rowData[3] == campaignId:
                owners.append(rowData[4].strip("\n"))

    return owners


def get_owner_id_from_kg(data_name, campaign, sample, owner):
    kg_path = os.path.join(putils.get_output_path(data_name, sample), campaign)
    raw_kg_path = os.path.join(kg_path, "raw")
    entities_file = os.path.join(raw_kg_path, "entities.idx")

    with open(entities_file, "r") as f:
        for row in f.readlines():
            rowData = row.split(",")
            if rowData[0] == owner:
                return rowData[1][:-1]


def get_max_kval_in_campaign(campaign):
    kvals = load_all_kvals(campaign)

    return max(kvals)


def get_min_kval_in_campaign(campaign):
    kvals = load_all_kvals(campaign)

    return min(kvals)




def load_graph_metadata(data_name, sample):
    raw_graph_path = putils.get_raw_graph_path(data_name, sample)
    node2id, relation2id, _, _, attribute_relation_ids, relationship_relation_ids = data.static_graph.read_index_data(
        raw_graph_path)
    attribute_domains = data.static_graph.read_domains_data(
        raw_graph_path)

    return node2id, relation2id, attribute_relation_ids, relationship_relation_ids, attribute_domains


def load_campaign_graph_metadata(data_name, sample, campaign):
    raw_graph_path = putils.get_campaign_raw_graph_path(campaign, data_name, sample)

    node2id, relation2id, _, _, attribute_relation_ids, relationship_relation_ids = data.static_graph.read_index_data(raw_graph_path)
    attribute_domains = data.static_graph.read_domains_data(raw_graph_path)

    return node2id, relation2id, attribute_relation_ids, relationship_relation_ids, attribute_domains



def get_edges_iter(path):
    with open(path, "r") as file:
        for line in file:
            entity1_id, relation_id, entity2_id = list(map(int, line.strip().split(",")))
            yield entity1_id, relation_id, entity2_id


def load_edges_iter_from_path(path):
    rel_info_path = os.path.join(path, "rels.edges")
    attr_info_path = os.path.join(path, "attrs.edges")

    attribute_edges_iter = get_edges_iter(attr_info_path)
    relationship_edges_iter = get_edges_iter(rel_info_path)

    return attribute_edges_iter, relationship_edges_iter

def load_anonymized_graph_from_path(data_name, sample, k_generator_name, info_loss_name, handler_name, calgo_name, enforcer_name, args):
    node2id, relation2id, attribute_relation_ids, relationship_relation_ids, attribute_domains = load_graph_metadata(data_name, sample)

    path = putils.get_anony_graph_path(data_name, sample, k_generator_name, info_loss_name, handler_name, calgo_name, enforcer_name, args)

    attribute_edges_iter, relationship_edges_iter = load_edges_iter_from_path(path)

    return data.StaticGraph.from_index_and_edges_data(node2id, relation2id, relationship_relation_ids, attribute_relation_ids, attribute_domains, attribute_edges_iter, relationship_edges_iter)



def load_anonymized_campaign_graph_from_path(data_name, sample, campaign, info_loss_name, handler_name, calgo_name, enforcer_name, args):
    node2id, relation2id, attribute_relation_ids, relationship_relation_ids, attribute_domains = load_campaign_graph_metadata(data_name, sample, campaign)

    path = putils.get_campaign_anony_graph_path(data_name, sample, campaign, info_loss_name, handler_name, calgo_name, enforcer_name, args)

    attribute_edges_iter, relationship_edges_iter = load_edges_iter_from_path(path)

    return data.StaticGraph.from_index_and_edges_data(node2id, relation2id, relationship_relation_ids, attribute_relation_ids, attribute_domains, attribute_edges_iter, relationship_edges_iter)


def load_anon_graph_attribute_edges_from_path(data_name, sample, campaign, info_loss_name, handler_name, calgo_name, enforcer_name, args):
    path = putils.get_campaign_anony_graph_path(data_name, sample, campaign, info_loss_name, handler_name, calgo_name, enforcer_name, args)

    attr_edges_file = os.path.join(path, "attrs.edges")

    with open(attr_edges_file, "r") as f:
        return f.readlines()

def load_anon_graph_relationship_edges_from_path(data_name, sample, campaign, info_loss_name, handler_name, calgo_name, enforcer_name, args):
    path = putils.get_campaign_anony_graph_path(data_name, sample, campaign, info_loss_name, handler_name, calgo_name, enforcer_name, args)

    rels_edges_file = os.path.join(path, "rels.edges")

    with open(rels_edges_file, "r") as f:
        return f.readlines()




def generate_anon_kg_file(attrEdges, relEdges, args):
    ent_path = putils.get_campaign_anony_graph_file_path(args["data"], args["sample"], args["campaign"], "entities.idx")
    val_path = putils.get_campaign_anony_graph_file_path(args["data"], args["sample"], args["campaign"], "values.idx")
    attr_path = putils.get_campaign_anony_graph_file_path(args["data"], args["sample"], args["campaign"], "attrs.idx")
    rel_path = putils.get_campaign_anony_graph_file_path(args["data"], args["sample"], args["campaign"], "rels.idx")

    entities = {}

    with open(ent_path, "r") as f:
        for row in f.readlines():
            entity = row.strip("\n").split(",")
            entities[entity[1]] = entity[0]

    values = {}

    with open(val_path, "r") as f:
        for row in f.readlines():
            value = row.strip("\n").split(",")
            values[value[1]] = value[0]

    attrs = {}

    with open(attr_path, "r") as f:
        for row in f.readlines():
            attr = row.strip("\n").split(",")
            attrs[attr[1]] = attr[0]

    rels = {}

    with open(rel_path, "r") as f:
        for row in f.readlines():
            rel = row.strip("\n").split(",")
            rels[rel[1]] = rel[0]

    
    newEdges = []

    for attrEdge in attrEdges:
        edgeVals = attrEdge.strip("\n").split(",")

        attrEdgeOwner = entities[edgeVals[0]]
        attrEdgeAttribute = attrs[edgeVals[1]][:-5]
        attrEdgeValue = values[edgeVals[2]]

        newEdges.append(attrEdgeOwner + " ---[" + attrEdgeAttribute + "]--> " + attrEdgeValue)
    
    for relEdge in relEdges:
        edgeVals = relEdge.strip("\n").split(",")

        relEdgeOwner1 = entities[edgeVals[0]]
        relEdgeRelationship = rels[edgeVals[1]][:-4]
        relEdgeOwner2 = entities[edgeVals[2]]

        newEdges.append(relEdgeOwner1 + " ---[" + relEdgeRelationship + "]--> " + relEdgeOwner2)

    newFilePath = putils.get_campaign_anony_graph_path(args["data"], args["sample"], args["campaign"], args["info_loss"], args["handler"], args["calgo"], args["enforcer"], args)

    new_file = os.path.join(newFilePath, "anony_" + args["campaign"].replace(" ", "_") + ".txt")

    with open(new_file,'w') as f:
        pass

    with open(new_file, "a") as f:
        for row in newEdges:
            f.write(row + "\n")






def load_raw_graph(data_name, sample):
    path = putils.get_raw_graph_path(data_name, sample)

    return data.StaticGraph.from_raw_graph_output(path)

def load_raw_campaign_graph(data_name, campaign, sample):
    path = putils.get_campaign_raw_graph_path(campaign, data_name, sample)
    return data.StaticGraph.from_raw_graph_output(path)

def load_entity_idx2id_dict(data_name, sample):
    idx_path = putils.get_entity_index_path(data_name, sample)
    idx2id_dict = {}

    with open(idx_path, "r") as f:
        for idx, line in enumerate(f):
            _,entity_id = line.rstrip().split(",")
            idx2id_dict[idx] = int(entity_id)

    return idx2id_dict

def load_campaign_entity_idx2id_dict(data_name, sample, campaign):
    idx_path = putils.get_campaign_entity_index_path(campaign, data_name, sample)
    idx2id_dict = {}

    campaign_id = get_campaign_id(campaign)

    owners_db_id = get_owners_from_campaign_id(campaign_id)

    owners = []

    for owner_db_id in owners_db_id:
        owners.append(get_owner_from_id(owner_db_id))

    with open(idx_path, "r") as f:
        for idx, line in enumerate(f):
            entity_name,entity_id = line.rstrip().split(",")
            if entity_name in owners:
                idx2id_dict[idx] = int(entity_id)

    return idx2id_dict


def load_entity_id2idx_dict(data_name, sample):
    idx_path = putils.get_entity_index_path(data_name, sample)
    id2idx_dict = {}

    with open(idx_path, "r") as f:
        for idx, line in enumerate(f):
            _,entity_id = line.rstrip().split(",")
            id2idx_dict[int(entity_id)] = idx

    return id2idx_dict

def load_campaign_entity_id2idx_dict(data_name, sample, campaign):
    idx_path = putils.get_campaign_entity_index_path(campaign, data_name, sample)
    id2idx_dict = {}

    campaign_id = get_campaign_id(campaign)

    owners_db_id = get_owners_from_campaign_id(campaign_id)

    owners = []

    for owner_db_id in owners_db_id:
        owners.append(get_owner_from_id(owner_db_id))

    with open(idx_path, "r") as f:
        for idx, line in enumerate(f):
            entity_name,entity_id = line.rstrip().split(",")
            if entity_name in owners:
                id2idx_dict[int(entity_id)] = idx

    return id2idx_dict

def load_dist_matrix(data_name, sample, info_loss_name, args):
    path = putils.get_distance_matrix_path(data_name, sample, info_loss_name, args)
    return np.load(path)

def load_campaign_dist_matrix(data_name, sample, info_loss_name, campaign, args):
    path = putils.get_campaign_distance_matrix_path(data_name, sample, info_loss_name, campaign, args)
    return np.load(path)

def load_entity_id2k_dict(data_name, sample, generator_name, args):
    id2k_dict_path = putils.get_k_values_path(data_name, sample, generator_name, args)

    id2k_dict = {}

    with open(id2k_dict_path, "r") as f:
        for line in f:
            entity_id, k = map(int, line.rstrip().split(","))
            id2k_dict[entity_id] = k

    return id2k_dict

def load_campaign_entity_id2k_dict(data_name, sample, campaign, args):
    id2k_dict_path = putils.get_campaign_k_values_path(data_name, sample, campaign, args)

    id2k_dict = {}

    with open(id2k_dict_path, "r") as f:
        for line in f:
            entity_id, k = map(int, line.rstrip().split(","))
            id2k_dict[entity_id] = k

    return id2k_dict

def load_k_values_sequence(data_name, sample, generator_name, args):
    id2k_dict = load_entity_id2k_dict(data_name, sample, generator_name, args)

    sequence = np.zeros(len(id2k_dict), dtype=int)

    sorted_entity_ids = sorted(list(id2k_dict.keys()))

    for idx, entity_id in enumerate(sorted_entity_ids):
        sequence[idx] = id2k_dict[entity_id]

    return sequence


def load_raw_clusters(data_name, sample, generator_name, info_loss_name, handler_name, calgo_name, args):
    clusters_path = putils.get_raw_clusters_path(data_name, sample, generator_name, info_loss_name, handler_name, calgo_name, args)
    clusters = algorithms.Clusters.from_file(clusters_path)

    logger.debug("loaded raw clusters at: {}".format(clusters_path))

    return clusters

def load_campaign_raw_clusters(data_name, sample, campaign, info_loss_name, handler_name, calgo_name, args):
    clusters_path = putils.get_campaign_raw_clusters_path(data_name, sample, campaign, info_loss_name, handler_name, calgo_name, args)
    clusters = algorithms.Clusters.from_file(clusters_path)

    logger.debug("loaded raw clusters at: {}".format(clusters_path))

    return clusters


def get_number_of_entities(data_name, sample):
    graph_dir = putils.get_raw_graph_path(data_name, sample)
    entities_idx_path = os.path.join(graph_dir, "entities.idx")

    num_entities = 0
    with open(entities_idx_path) as f:
        for _ in f:
            num_entities += 1

    return num_entities
