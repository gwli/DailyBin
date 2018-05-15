#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import datetime
import argparse
import imp
today=datetime.datetime.now().strftime("%Y_%m_%d")
prefix="github_{}".format(today)
sys.path.append("/home/vili/git/dailybin/lib/python")
from gitsearch import search,get_readme,gen_html,send_mail


def main(args):
   today=datetime.datetime.now().strftime("%Y_%m_%d")
   prefix="github_{}".format(today)
   output_file = "{}_TechBookHunter.py".format(prefix)
   search_pattern = "user:{}".format(args.user)
   search(search_pattern,output_file)
   data = imp.load_source("data",output_file)
   for index,ele in enumerate(data.repo_list):
       print("name:{},git:{}.git".format(ele["name"],ele["html_url"])) 
         
if __name__== "__main__":
   parser = argparse.ArgumentParser(description="TechBookHunter")
   parser.add_argument('--user',help='user',type=str, default='TechBookHunter')
   args = parser.parse_args()
   main(args)
