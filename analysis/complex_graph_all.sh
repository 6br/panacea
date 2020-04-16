#!/bin/bash
#./complex_graph_all.sh ../rcc/e2*/*.csv

PYTHON3=~/anaconda3/bin/python3 #python3 # ~/anaconda3/bin/python3
PG2NEO=~/pg/src/pg2neo.js 

$PYTHON3 `dirname $0`/complex_graph_desc_all.py $@ > `pwd`/graph_complex_all2.pg && $PG2NEO `pwd`/graph_complex_all2.pg

export NEO4J_DIR="/var/lib/neo4j" # On Ubuntu 18.04

#sudo neo4j-import --into $NEO4J_DIR/data/databases/graph.db \
#	--nodes graph.neo.nodes --relationships graph.neo.edges

