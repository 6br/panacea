Panacea: Polarizing Attributes for Network Analysis of Correlation on Entities Association
-------

# Getting Started

```bash
$ docker-compose build
$ docker-compose up
``` 

If it does not work,

```bash
$ docker-compose down
$ docker-compose up
```

If you need to rebuild,

```bash
$ docker-compose build --no-cache
```

Consider to check `~/.docker/config.json` when you struggle with proxies.

# Import Data

1. Modify the path on `analysis/complex_graph_all.sh`
2. Run `analysis/complex_graph_all.sh <csv_files_of_hr_data>`
3. Move the output to neo4j folder `mv analysis/graph_complex_all.neo.* panacea/graph_complex_all.neo.*`
4. Run docker-compose `./docker-compose up`


