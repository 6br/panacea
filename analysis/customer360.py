#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pickle
import sys
import traceback

from matplotlib import pyplot
from matplotlib_venn import venn3


# In[2]:


e2r = pickle.load(open('e2r.pkl', 'rb'))
sonar = pickle.load(open('sonar.pkl', 'rb'))
merged = pickle.load(open('merged.pkl', 'rb'))
#merged2 = pd.merge(merged, e2r, how="left", right_on=["氏名（姓・名）", "学部"], left_on=["氏名", "学部名_x"])


# In[3]:


#merged3 = merged2
merged2 = merged


# In[4]:


merged2.head()


# In[5]:


#[i for i in merged2.columns if "意思" in i]
merged2[merged2["意思確認"]== "確認しました。"].head()


# In[9]:


j = 19
for i in range(merged2.iloc[j].size):
    try:
        vc = merged2.iloc[:,i].value_counts()
        #print(vc.iat[0])
        #print(merged2.iloc[0][i])
        #print(vc[merged2.iloc[0][i]])
        if "【" in merged2.columns[i]:
            continue
        if merged2.iloc[j][i] != merged2.iloc[j][i]:
            continue
    #    print(merged2.iloc[j][i])
        if merged2.iloc[j][i] in vc and vc[merged2.iloc[j][i]] > 3 and (vc.iat[0] == vc[merged2.iloc[j][i]] and len(vc) <= 5): # vc[merged2.iloc[0][i]] > 10:
            continue

        #print (merged2.columns[i], merged2.iloc[j][i], vc[merged2.iloc[j][i]], vc.iat[0], vc.index[0], len(vc))
    except:
        pass


# In[ ]:


node_id = 0
props_hash = {}
for j in range(len(merged2)):
    if ((merged2["意思確認"]== "確認しました。")[j]):
        #print(j)
        for i in range(merged2.iloc[j].size):
            try:
                vc = merged2.iloc[:,i].value_counts()
                #print(vc.iat[0])
                #print(merged2.iloc[0][i])
                #print(vc[merged2.iloc[0][i]])
                if "【" in merged2.columns[i] or "ES" in merged2.columns[i] or "応募者ID" in merged2.columns[i]:
                    continue
                if merged2.iloc[j][i] != merged2.iloc[j][i]:
                    continue
                if vc[merged2.iloc[j][i]] > 3 and (vc.iat[0] == vc[merged2.iloc[j][i]] and len(vc) <= 5): # vc[merged2.iloc[0][i]] > 10:
                    continue
                    

                if merged2.columns[i] == "氏名":
                    node = [str(node_id), ":person"]
                    props = {"label": merged2.iloc[j][i]}
                    props_list = [x[0] + ":" + "\"" + str(x[1]) + "\"" for x in list(props.items()) if x[1] == x[1]]
                    #if len(props_list) <= 1:
                    #    continue
                    orig_node = node_id
                    node.extend(props_list)
                    node_id += 1
                    print("\t".join(node))
                else:
                    node = [":" + merged2.columns[i]]
                    props = {"label": merged2.iloc[j][i]}
                    props_list = [x[0] + ":" + "\"" + str(x[1]) + "\"" for x in list(props.items()) if x[1] == x[1]]
                    #if len(props_list) <= 1:
                    #    continue
                    node.extend(props_list)
                    if tuple(node) in props_hash:
                        #node = [str(props_hash[tuple(node)])] + node
                        #print("\t".join(node))
                        edge = [str(orig_node), "->", str(props_hash[tuple(node)])]
                        print("\t".join(edge))
                    else:
                        props_hash[tuple(node)] = node_id
                        node = [str(node_id)] + node
                        print("\t".join(node))
                        edge = [str(orig_node), "->", str(node_id)]
                        print("\t".join(edge))
                        node_id += 1
            except:
                #print(traceback.format_exc()) 
                pass

#            print (merged2.columns[i], merged2.iloc[j][i], vc[merged2.iloc[j][i]], vc.iat[0], vc.index[0], len(vc))


# In[ ]:


#print(merged2.size)

