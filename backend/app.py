#!/usr/bin/env python3

import responder
import graphene
import algorithm
import json

api = responder.API(cors=True, cors_params={"allow_origins": ['*']})

class Query(graphene.ObjectType):
    query = graphene.types.json.JSONString(first=graphene.String(default_value="degree"), second=graphene.String(default_value="domain"), year=graphene.Int(default_value=2019), inherit=graphene.Boolean(default_value=False), auto=graphene.Boolean(default_value=False), layout=graphene.String(default_value="circular"), scale=graphene.Int(default_value=12), english=graphene.Boolean(default_value=False), dark=graphene.Boolean(default_value=False), lower_bound=graphene.Int(default_value=12), upper_bound=graphene.Int(default_value=12))

    def resolve_query(self, info, first, second, year, inherit, auto, layout, scale, english, dark, lower_bound, upper_bound):
        return algorithm.fetch(first, second, year, inherit, auto, layout, scale, english, dark, lower_bound, upper_bound)

    profile = graphene.types.json.JSONString(prof_type=graphene.String(default_value="all"))
    
    def resolve_profile(self, info, prof_type):
        return algorithm.profile_query(prof_type)
    
    table = graphene.types.json.JSONString(first=graphene.String(default_value="degree"), second=graphene.String(default_value="domain"), scale=graphene.Int(default_value=12))
    
    def resolve_table(self, info, first, second, scale):
        return algorithm.table_query(first, second, scale)
    
schema = graphene.Schema(query=Query)
view = responder.ext.GraphQLView(api=api, schema=schema)

api.add_route("/graph", view)

if __name__ == '__main__':
    api.run()
    