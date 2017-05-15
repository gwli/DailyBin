#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import logging
logging.basicConfig(level=logging.DEBUG)
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
import pprint 
pp=pprint.PrettyPrinter(indent=4)
import imp
import ast
import random
import time
GOOGLER="/home/devtoolsqa8/git/dailybin/bin/googler"
ASCIINEMA_DEMO="https://asciinema.org/a/6mod6437ets7l2ml7lsa9b99l"
tpl = "/home/devtolsqa8/etc/lgzsearch_tpl"

def gen_key():
    alphabeta = {
       "Abstract": ("抽象","建模"),
       "Begin" : ("启始", "balance shift","从心开始"),
       "Combine" :("排列组合", "计算复杂度:常，对，线，平，立，指，阶"),
       "Decompose" :("分解","分类","分块"),
       "Evolve": ("演化","周期","迭代","增长"),
       "Friend/Family" : ("很感谢你能能来，不遗憾你离开","局部化"),
       "Graph":("可视化","联想","联接"),
       "Healthy" :("健康","生老病死"),
       "Interest" :("意义","复利","边际效应"),
       "Judge" :("策略","战略","稀缺","成本","选择","歧视","租","需求","弹性","价格","短缺和过剩"),
       "Keen": ("有趣","有料","有用"),
       "Limit":("奇点","边界","极限"),
       "Math":("概率","量化分析","费米计算"),
       "Network":("网络","拓扑","关系","秩"),
       "Optimize":("20/80原则","trade off","交换","优化"),
       "4P":("并行","刻意练飞","展示","推动"),
       "Question":("本质","4因5路"),
       "Recusive":("不动点","随机"),
       "Search":("近同反","外延"),
       "Unify":("统一","合并"),
       "Verify":("验证","证伪","批判"),
       "5W1H":("是什么","时间","地点","哪些人","为什么","如何"),
       "X": ("不确定","混沌"),
       "Y": ("未来","历史"),
       "Z": ("分层模块化","高维"),
       }
    for k,v in alphabeta.iteritems():
        logger.debug("{}:{}".format(k,random.choice(v)))
    return [random.choice(v) for k,v in alphabeta.iteritems()]

def test(km_repo):
    
    for dir_name, subdir,filelist in os.walk(km_repo):
      for file in filelist:
       real_path = os.path.join(dir_name,file)
       if file.endswith(".py"):
           update_status(real_path)

def dump_km_foo(foo,output_path,status="."):
    with open(output_path,'w') as ofile:
        #write header
        ofile.write("# -*- coding:utf-8 -*- \n\n")

        ofile.write("Q_dict = { \n")
        #write Q_queue
        for  k,v in foo.Q_dict.iteritems():
            ofile.write("######\n")
            ofile.write("#")
            ofile.write(k)
            ofile.write(" #:")
            ofile.write(v[0])   
            ofile.write("\n")
            ofile.write("######\n")
            ofile.write("\"")
            ofile.write(k)
            ofile.write("\"")
            ofile.write(": [\"")
            ofile.write(v[0])
            ofile.write("\",\n")
            for ele in v[1:]:
               ofile.write("    {\n")
               for ek,ev in ele.iteritems():
                   ofile.write("    \"")
                   ofile.write(     ek)
                   ofile.write("\" :\"")
                   ofile.write(     ev)
                   ofile.write("\",\n")
               ofile.write("    },\n")
            ofile.write("    ],\n")

        ofile.write("}\n")

        #####write Dynamic
        #keyword_list
        ofile.write("keyword_list = [ \n")
        for combin_key in gen_key():
            ofile.write("   \"   {}\",\n".format(combin_key))
        ofile.write("]\n")
        #meta
        ofile.write("meta_data = {")
        #ofile.write("\"status\":\"{}\",".format(foo.meta_data['status']))
        ofile.write("\"status\":\"{}\",".format(status))
        ofile.write("\"Major\": {},".format(foo.meta_data['Major']))
        ofile.write("\"Minor\": {},".format(foo.meta_data['Minor']))
        ofile.write("\"Prefix\": \"Q\"")
        ofile.write("}\n")

        #title
        ofile.write("km_0_title = \"")
        ofile.write(foo.km_0_title)
        ofile.write("\"\n")
        #sumary
        ofile.write("km_0_summary = \"")
        ofile.write(foo.km_0_summary)
        ofile.write("\"\n")
        #tags
        ofile.write("km_1_tags = [")
        for tag in foo.km_1_tags:
            ofile.write("\"")
            ofile.write(foo.km_1_tags)
            ofile.write("\",")
            
        ofile.write("]\n")
            

def update_status(km_file,sleep=True):
    logger.info("update :{}".format(km_file))
    km_foo =imp.load_source("data",km_file) 
    
    if km_foo.meta_data["status"] == ".":
       return
    km_foo.meta_data["Major"] +=1
    km_foo.meta_data["Minor"] = 0
    for keyword in km_foo.keyword_list:
       Q_num = "{}_{}_{}".format(km_foo.meta_data['Prefix'],km_foo.meta_data['Major'],km_foo.meta_data['Minor']) 
       
       cmd = [GOOGLER,"-c hk", "-n 10", "--np --json" ,keyword]
       logger.info(cmd)
       if sleep:
          time.sleep(random.randint(5,20))
       out= os.popen(" ".join(cmd)).read()
       logger.info(out)
       Question_entry = ast.literal_eval(out)
       Question_entry = [keyword] + Question_entry
       km_foo.Q_dict[Q_num]= Question_entry       
       km_foo.meta_data['Minor'] += 1
    dump_km_foo(km_foo,km_file)
    return

def mk_lgzsearch_tml(out_file,keyword):
    logger.info("read from :{}".format(tpl))
    km_foo =imp.load_source("data",tpl) 
    
    if km_foo.meta_data["status"] == ".":
       return
    km_foo.meta_data["Major"] = 0
    km_foo.meta_data["Minor"] = 0

    Q_num = "{}_{}_{}".format(km_foo.meta_data['Prefix'],km_foo.meta_data['Major'],km_foo.meta_data['Minor']) 
    
    cmd = [GOOGLER,"-c hk", "-n 10", "--np --json" ,keyword]
    logger.info(cmd)
    out= os.popen(" ".join(cmd)).read()
    logger.info(out)
    Question_entry = ast.literal_eval(out)
    Question_entry = [keyword] + Question_entry
    km_foo.Q_dict[Q_num]= Question_entry       
    dump_km_foo(km_foo,out_file,status="c")

if __name__ == "__main__":
   
   test("/home/devtoolsqa8/git/KM/source")
