#!/usr/bin/env python3

import pandas as pd
import sys
import re
import logging

formatter = '%(levelname)s : %(asctime)s : %(message)s'

logging.basicConfig(level=logging.DEBUG, format=formatter)

company_hash = {}
company_latest_id = 1000000 # We start company id from here.
meta_id = 10000000
i = 0
MIN_PROPS_COUNT=3

normalize_hash = {"日立": "日立製作所", "hitachi": "日立製作所", "sony": "ソニー", "canon": "キヤノン", "キャノン": "キヤノン", "ntt": "日本電信電話", "トヨタ": "トヨタ自動車", "nttdocomo": "nttドコモ", "エプソン": "セイコーエプソン", "honda": "本田技研工業", "ホンダ": "本田技研工業", "本田技研": "本田技研工業", "日産": "日産自動車"}


#if sys.argv[1]:
category = pd.read_csv(sys.argv[1], low_memory=False, encoding="utf-8", skipinitialspace=True)
category_hash = {}
meta_nodes = []
for _, row in category.iterrows():
    category_hash[row["2019"]] = row["カテゴリ名"]
    meta_nodes.append(row["カテゴリ名"])

meta_set = set(meta_nodes)
meta_list = list(meta_set)
meta_hash = {}
for meta_name in meta_list:
    if type(meta_name) is str:
        meta = [str(meta_id), ":meta", "name:\"" + meta_name.rstrip().strip("\\").replace('\t', ' ') + "\""]
        print("\t".join(meta))
        meta_hash[meta_name] = meta_id
        meta_id += 1

for (key, value) in category_hash.items():
    # Key is a type of attribute.
    if type(key) is str:
        meta = [str(meta_id), ":item", "name:\"" + key.rstrip().strip("\\").replace('\t', ' ') + "\""] # "category: str(value).replace('"', '\\"')
        print("\t".join(meta))
        # Add category edge:
        if value in meta_list:
            edge = [str(meta_id), "->", str(meta_hash[value]), ":categorized_as", "label:" + "\"" + str(value).replace('"', '\\"') + "\""]
            print("\t".join(edge))
        meta_id += 1


def add_company(name, node_type):
    # TODO: WE NEED TO NORMALIZE A NAME OF COMPANY
    global company_latest_id
    global company_hash
    #name = name.replace("株式会社", "")
    name = name.lower()
    if name in normalize_hash:
        name = normalize_hash[name]
    if name in company_hash:
        return company_hash[name]
    
    # If not exist:
    company_latest_id += 1
    company = [str(company_latest_id), node_type, "name:\"" + name.rstrip().strip("\\").replace('\t', ' ') + "\""]
    print("\t".join(company))
    company_hash[name] = company_latest_id

    return company_hash[name]


for item in sys.argv[2:]:
    logging.debug('%s', item)
    e2r = pd.read_csv(item, low_memory=False, encoding="cp932", skipinitialspace=True)

    for _, row in e2r.iterrows():
        props = {}
        props["ユーザID"] = row["ユーザID"]
        props["希望職種系統"] = row["希望職種系統"]
        props["選考種別フラグ"] = row["選考種別フラグ"] 
        props["選考採用区分"] = row["採用選考区分"] 
        if row["大学名"] == row["大学名"]:
            props["name"] = "\"" + str(row["大学名"].rstrip()) + "\""
        props["year"] = re.findall("[0-9]{4}", item)[0]
        year = re.findall("[0-9]{4}", item)[0]
        props["category"] = row["内々定_意思確認フラグ"]
        if "内々定_配属カンパニー" in row:
            belong = row["内々定_配属カンパニー"]
        elif "内々定_配属ドメイン" in row:
            belong = row["内々定_配属ドメイン"]
        university = row["学校"] 
        bunri = row["文理区分"]
        department = row["学部"]
        keitou = row["系統"]
        if "希望職種" in row:
            syokusyu = row["希望職種"]
        elif "プレエントリー／希望職種" in row:
            syokusyu = row["プレエントリー／希望職種"]
        east_west = row["エントリーシート出力用東西区分"]
        degree = row["学歴区分"]
        when = row["選考会エントリー期"]
        if "性別" in row:
            gender = row["性別"]
        else:
            gender = row["性別（自動判定）"]
        province = row["学校所在地域"]
        if "英語のレベル" in row:
            english = row["英語のレベル"]
        else:
            english = row["プレエントリー／英語のレベル"]
        referral = row["選考種別フラグ"]
        evaluation = row["最終選考_評価_採用センター所長"]

        tuples = [(":文理", bunri, ":is_related_to"), (":学部", department, ":is_at"), (":系統", keitou, ":is_majored_in"), (":東西区分", east_west, ":is_categorized_as"), (":学歴区分", degree, ":is_now"), (":希望職種", syokusyu, ":desires"), (":希望職種系統", row["希望職種系統"], ":desires"), (":学校所在地域", province, ":is_located_at"), (":選考会エントリー期", when, ":is_applied_when"), (":性別", gender, ":is"), (":英語のレベル", english, ":speaks_English_as"), (":選考種別フラグ", referral, ":is_a"), (":最終選考_評価_採用センター所長", evaluation, ":is_evaluated_as"), (":time", year, ":in")]
        node = [str(i+1), ":person"] if (props["category"] != "入社意思確定" and props["category"] != "07da9a3b2054dcaf92b695d4ab55bad29bc18c0c7b26de25f9f1bb86cf2513f3" and props["category"] != "dc42f4638f80ae5dc1a5ddaf2e4edfdee6577407b4e0bf6a1a23c8b2b90b6202" and props["category"] != "5cd05332ceec0f70e816e2a698345f7f8f9e4feaf33e6272f1c6236dbcec1af5" and props["category"] != "987e0dab1fe8551842fe8662b87becaee41ef1d2471ef7bc7bba4b2a6e21e8fc") else [str(i+1), ":candidate"]
        if university == university:
            company_id = add_company(university, ":大学名")
            edge = [str(i+1), "->", str(company_id), ":is_at"]
            print("\t".join(edge))
        if belong and belong == belong:
            company_id = add_company(belong, ":ドメイン")
            edge = [str(i+1), "->", str(company_id), ":works_at"]
            print("\t".join(edge))
        for x in tuples:
            if x[1] and x[1] == x[1]:
                company_id = add_company(x[1], x[0])
                edge = [str(i+1), "->", str(company_id), x[2]]
                print("\t".join(edge))


        already_taken = ["ユーザID", "希望職種系統", "選考種別フラグ", "採用選考区分", "大学名", "文理", "選考種別フラグ", "英語のレベル", "学校所在地域", "プレエントリー／英語のレベル", "性別（自動判定）", "性別", "選考会エントリー期","プレエントリー／希望職種", "学歴区分", "希望職種", "系統", "文理区分", "学校", "学部", "内々定_配属ドメイン", "内々定_配属カンパニー", "内々定_意思確認フラグ", "希望マッチング先第一希望ドメイン", "希望マッチング先第二希望ドメイン", "希望マッチング先第三希望ドメイン", "希望マッチング先第二希望度合", "希望マッチング先第三希望度合", "１次選考_マッチング先会社判断01", "１次選考_マッチング先会社判断02", "１次選考_マッチング先会社判断03", "内々定辞退_辞退先", "内々定辞退_理由", "[CC]志望先1（当社を含む）", "[CC]志望先2（当社を含む）", "[CC]志望先3（当社を含む）", "BOS(CC)志望先1（当社を含む）", "BOS(CC)志望先2（当社を含む）", "BOS(CC)志望先3（当社を含む）"]

        for (k, v) in row.items():
            if len(k) <= 12 and not k in already_taken and v and v == v:
                    company_id = add_company(str(v), ":" + str(k))
                    edge = [str(i+1), "->", str(company_id), ":is"]
                    print("\t".join(edge))


       
        actual_belong = belong
        try:
            sci_expectations = [row["希望マッチング先第一希望ドメイン"], row["希望マッチング先第二希望ドメイン"], row["希望マッチング先第三希望ドメイン"]]
            sci_expectations_probability = [row["希望マッチング先第二希望度合"], row["希望マッチング先第三希望度合"]]
            sci_required = [row["１次選考_マッチング先会社判断01"], row["１次選考_マッチング先会社判断02"], row["１次選考_マッチング先会社判断03"]]
            for rank, belong in enumerate(sci_expectations):
                if belong and belong == belong and not belong == actual_belong:
                    company_id = add_company(belong, ":ドメイン")
                    edge = [str(i+1), "->", str(company_id), ":is_interested_in", "rank:" + "\"" + str(rank).replace('"', '\\"') + "\""]
                    print("\t".join(edge))
            for rank, belong in enumerate(sci_required):
                if belong and belong == belong and not belong in sci_expectations:
                    company_id = add_company(belong, ":ドメイン")
                    edge = [str(i+1), "->", str(company_id), ":is_required_to_work_at", "rank:" + "\"" + str(rank).replace('"', '\\"') + "\""]
                    print("\t".join(edge))
        except:
            pass


        props_list = [x[0] + ":" + str(x[1]) for x in list(props.items()) if x[1] == x[1]]
        if len(props_list) <= 1:
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
                    company_id = add_company(company, ":競合他社")
                    edge = [str(i+1), "->", str(company_id), ":is_interested_in", "rank:" + "\"" + str(rank).replace('"', '\\"') + "\""]
                    print("\t".join(edge))
    
        escape = row["内々定辞退_辞退先"] 
        escape_reason = row["内々定辞退_理由"]
    
        if escape == escape: # Not numpy.nan
            escape = escape.replace("株式会社", "")
            escape = escape.replace("(株)", "")
            escape = escape.replace("（株）", "")
            if escape != "パナソニック" and escape != "Panasonic":
                company_id = add_company(escape, ":競合他社")
                edge = [str(i+1), "->", str(company_id), ":fled_to", "reason:" + "\"" + str(escape_reason).replace('"', '\\"') + "\""]
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
 
