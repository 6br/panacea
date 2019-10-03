#!/bin/bash

~/anaconda3/bin/python3 graph.py ../rcc/e2*/*.csv > graph_all.pg
~/pg/src/pg2neo.js graph_all.pg

export NEO4J_DIR="/var/lib/neo4j" # On Ubuntu 18.04
NEO4J_DIR="/var/lib/neo4j" # On Ubuntu 18.04

sudo neo4j-import --into $NEO4J_DIR/data/databases/graph.db --delimiter "\t"  \
	--nodes graph_all.neo.nodes --relationships graph_all.neo.edges

