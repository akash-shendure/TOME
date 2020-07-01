#!/usr/bin/python
# -*- coding: utf-8 -*-

# This script is made to reformat a specific .json file for another purpose
# Input: https://raw.githubusercontent.com/ChengxiangQiu/tree/master/mouse.json
# Output: https://raw.githubusercontent.com/akash-shendure/TOME/master/data.json

# Import the JSON module

import json

# Set whether or not the output will be pretty printed

pretty_printing = 1

# Set the name of the input file

infile_name = 'mouse.json'

# Set the name of the output file

outfile_name = 'data.json'

# Set the keys to be deleted from the input dictionary

del_keys = [
    'name',
    'datset',
    'derivator',
    'marker',
    'tf',
    'children',
    'size',
    'fx',
    'node_group',
    ]

# Set the tags for the node groups

groups = {
    0: 'E3: ',
    1: 'E3.5: ',
    2: 'E4.5: ',
    3: 'E5.5: ',
    4: 'E6.5: ',
    5: 'E6.75: ',
    6: 'E7: ',
    7: 'E7.25: ',
    8: 'E7.5: ',
    9: 'E7.75: ',
    10: 'E8: ',
    11: 'E8.25: ',
    12: 'E8.5: ',
    13: 'E9.5: ',
    14: 'E10.5: ',
    15: 'E11.5: ',
    16: 'E12.5: ',
    17: 'E13.5: ',
    }

# Set strings to be replaced in the id and ancestor tags of nodes

id_replacements = [
    ['Exe', 'Extraembryonic'],
    ['Prog.', 'Progenitors'],
    ['Haematoendothelial', 'Hemato-Endothelial'],
    ['Te', 'TE'],
    ['Icm', 'ICM'],
    ['Pgc', 'PGC'],
    ['Murola', 'Morula']
    ]


# Expand the input dictionary into a list of lists of nodes

def expand(data):
    complete_list = []
    list_of_children = []
    list_of_children.append(data)
    while list_of_children:
        new_list = []
        list_of_new_children = []
        for child_parent in list_of_children:
            new_list.append(child_parent)
            if 'children' in child_parent:
                for child_child in child_parent['children']:
                    list_of_new_children.append(child_child)
        complete_list.append(new_list)
        list_of_children = list_of_new_children
    return complete_list


# Remove unwanted information from the node dictionaries

def clean(data, del_keys):
    group_list = []
    for group in data:
        dictionary_list = []
        for dictionary in group:
            for key in del_keys:
                if key in dictionary:
                    dictionary.pop(key)
            dictionary_list.append(dictionary)
        group_list.append(dictionary_list)
    return group_list


# Reformat the information in the node dictionaries

def reformat(data, groups, id_replacements):
    new_data = []
    group_number = 0
    for group in data:
        group_data = []
        if group_number > 0:
            ancestor_code = groups[group_number - 1]
        for dictionary in group:
            seperated_id = dictionary['id'].split(':')
            new_id = seperated_id[0] + ': ' + seperated_id[1]
            dictionary['id'] = new_id
            dictionary['id'] = dictionary['id'].title()
            for id_replacement in id_replacements:
                old = id_replacement[0]
                new = id_replacement[1]
                dictionary['id'] = dictionary['id'].replace(old, new)
            if group_number > 0:
                new_ancestor = ancestor_code + dictionary['ancestor']
                dictionary['ancestor'] = new_ancestor
                for possible_ancestor_dictionary in data[group_number
                        - 1]:
                    possible_ancestor_name = dictionary['id'].split(': '
                            )[1]
                    possible_ancestor = ancestor_code \
                        + possible_ancestor_name
                    if possible_ancestor_dictionary['id'] \
                        == possible_ancestor:
                        dictionary['ancestor'] = possible_ancestor
                dictionary['ancestor'] = dictionary['ancestor'].title()
                for id_replacement in id_replacements:
                    old = id_replacement[0]
                    new = id_replacement[1]
                    dictionary['ancestor'] = dictionary['ancestor'
                            ].replace(old, new)
            else:
                dictionary.pop('ancestor')
            dictionary['group'] = group_number
            group_data.append(dictionary)
        new_data.append(group_data)
        group_number += 1
    return new_data


# Create the finalized list of node dictionaries

def create_nodes(data):
    nodes = []
    for group in data:
        for dictionary in group:
            node = {}
            node['id'] = dictionary['id']
            node['group'] = dictionary['group']
            nodes.append(node)
    return nodes


# Create the finalized list of link dictionaries

def create_links(data):
    links = []
    for group in data:
        for dictionary in group:
            if 'ancestor' in dictionary:
                link = {}
                link['source'] = dictionary['ancestor']
                link['target'] = dictionary['id']
                links.append(link)
    return links


# Open the input and output files

infile = open(infile_name, 'r')
outfile = open(outfile_name, 'w')

# Reformat the data from the input dictionary into an ouput dictionary

data = json.load(infile)
data = reformat(clean(expand(data), del_keys), groups, id_replacements)
nodes = create_nodes(data)
links = create_links(data)
output = {'nodes': nodes, 'links': links}

# Export the data with or without pretty printing

if pretty_printing == True:
    outfile.write(json.dumps(output, indent=2))
else:
    outfile.write(json.dumps(output))

# Close the input and output files

infile.close()
outfile.close()
