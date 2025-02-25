#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

# do not run init script at each container strat but only at the first start
if [ ! -f /tmp/neo4j-import-done.flag ]; then
    #/var/lib/neo4j/bin/neo4j-admin neo4j-admin restore --from=<backup-directory mount as a docker volume under /neo4j-data> [--database=<name>] [--force[=<true|false>]]
    if [ -e /var/lib/neo4j/data/databases/graph.db ]; then
        rm -r /var/lib/neo4j/data/databases/graph.db
    fi
    /var/lib/neo4j/bin/neo4j-admin import --multiline-fields=true --database graph.db --delimiter '\t' --nodes /neo4j/graph_complex_all2_uniq.neo.nodes --relationships /neo4j/graph_complex_all2_uniq.neo.edges
#    /var/lib/neo4j/bin/neo4j-admin import --multiline-fields=true --database graph.db --delimiter '\t' --nodes /neo4j/graph_complex_all.neo.nodes --relationships /neo4j/graph_complex_all.neo.edges
    touch /tmp/neo4j-import-done.flag
else
    echo "The import has already been made."
fi
