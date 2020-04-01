#!/bin/bash
#./complex_graph_all.sh ../rcc/e2*/*.csv

PYTHON3=python3 # ~/anaconda3/bin/python3
PG2NEO="docker run --rm -v $PWD:/work g2glab/pg:0.3.4 pg2neo" #~/pg/src/pg2neo.js 

$PYTHON3 `dirname $0`/complex_graph_desc.py $@ > `pwd`/graph_complex_all.pg && $PG2NEO `pwd`/graph_complex_all.pg

export NEO4J_DIR="/var/lib/neo4j" # On Ubuntu 18.04

#sudo neo4j-import --into $NEO4J_DIR/data/databases/graph.db \
#	--nodes graph.neo.nodes --relationships graph.neo.edges

