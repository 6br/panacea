#!/usr/bin/env python3

import pandas as pd
import sys
import re

company_hash = {}
company_latest_id = 1000000
i = 0
MIN_PROPS_COUNT=3

normalize_hash = {"日立": "日立製作所", "hitachi": "日立製作所", "sony": "ソニー", "canon": "キヤノン", "キャノン": "キヤノン", "ntt": "日本電信電話", "トヨタ": "トヨタ自動車", "nttdocomo": "nttドコモ", "エプソン": "セイコーエプソン", "honda": "本田技研工業", "ホンダ": "本田技研工業", "本田技研": "本田技研工業", "日産": "日産自動車"}

def add_company(name):
    # TODO: WE NEED TO NORMALIZE A NAME OF COMPANY
    global company_latest_id
    global company_hash
    #name = name.replace("株式会社", "")
    name = name.lower()
    if name in normalize_hash:
        name = normalize_hash[name]
    if name in company_hash:
        return company_hash[name]
    company_latest_id += 1
    company = [str(company_latest_id), ":company", "name:" + name]
    print("\t".join(company))
    company_hash[name] = company_latest_id
    return company_hash[name]


for item in sys.argv[1:]:
    e2r = pd.read_csv(item, low_memory=False)

    for _, row in e2r.iterrows():
        node = [str(i+1), ":person"]
        props = {}
        props["id"] = row["ユーザID"]
        props["job_type"] = row["希望職種系統"]
        props["recruit_type"] = row["選考種別フラグ"] 
        props["recruit_type"] = row["採用選考区分"] 
        props["university"] = row["大学名"] 
        props["name"] = row["大学名"] 
        props["year"] = re.findall("[0-9]{4}", item)[0]
        #props["category"] = row["【内】ユーザ区分"]
        props["category"] = row["内々定_意思確認フラグ"]
        if "内々定_配属カンパニー" in row:
            props["belong"] = row["内々定_配属カンパニー"]
        if "内々定_配属ドメイン" in row:
            props["belong"] = row["内々定_配属ドメイン"]
        props_list = [x[0] + ":" + "\"" + str(x[1].rstrip()) + "\"" for x in list(props.items()) if x[1] == x[1]]
        if len(props_list) <= MIN_PROPS_COUNT:
            continue
        node.extend(props_list)
        
        print("\t".join(node))
        
        try:
            competitors = [row["BOS(CC)志望先1（当社を含む）"], row["BOS(CC)志望先2（当社を含む）"], row["BOS(CC)志望先3（当社を含む）"]] 
        except:
            competitors = [row["[CC]志望先1（当社を含む）"], row["[CC]志望先2（当社を含む）"], row["[CC]志望先3（当社を含む）"]] 
    
        for rank, company in enumerate(competitors):
            if company == company:
                company = company.replace("株式会社", "")
                company = company.replace("(株)", "")
                company = company.replace("（株）", "")
                if company != "" and company != "パナソニック" and company != "Panasonic" and company != "panasonic":
                    company_id = add_company(company)
                    edge = [str(i+1), "->", str(company_id), ":is_interested_in", "rank:" + str(rank)]
                    print("\t".join(edge))
    
        escape = row["内々定辞退_辞退先"] 
        escape_reason = row["内々定辞退_理由"]
    
        if escape == escape: # Not numpy.nan
            escape = escape.replace("株式会社", "")
            escape = escape.replace("(株)", "")
            escape = escape.replace("（株）", "")
            if escape != "パナソニック" and escape != "Panasonic":
                company_id = add_company(escape)
                edge = [str(i+1), "->", str(company_id), ":fled_to", "reason:" + str(escape_reason)]
                print("\t".join(edge))

        i += 1
        
"""
    internships = [row["インターンシップ社名01"], row["インターンシップ社名02"], row["インターンシップ社名03"]]

    for company in internships:

        if company == company and company != "パナソニック" and company != "Panasonic":
            company_id = add_company(company)
            edge = [str(i+1), "->", str(company_id), ":has_worked_at"]
            print("\t".join(edge))
"""
 
