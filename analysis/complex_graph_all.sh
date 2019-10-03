#!/bin/bash

~/anaconda3/bin/python3 complex_graph_desc.py ../rcc/e2*/*.csv > graph_complex_all4.pg && ~/pg/src/pg2neo.js graph_complex_all4.pg

export NEO4J_DIR="/var/lib/neo4j" # On Ubuntu 18.04

#sudo neo4j-import --into $NEO4J_DIR/data/databases/graph.db \
#	--nodes graph.neo.nodes --relationships graph.neo.edges

