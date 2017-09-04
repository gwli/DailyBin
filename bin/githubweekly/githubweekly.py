#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import datetime
import argparse
today=datetime.datetime.now().strftime("%Y_%m_%d")
prefix="github_{}".format(today)
sys.path.append("/home/devtoolsqa8/git/dailybin/lib/python")
from gitsearch import search,get_readme,gen_html,send_mail

today=datetime.datetime.now().strftime("%Y_%m_%d")
prefix="github_{}".format(today)
output_file = "{}_input.py".format(prefix)
if __name__== "__main__":
   parser = argparse.ArgumentParser(description="githubweekly")
   parser.add_argument('-m',help='mail address',type=str,default='')
   parser.add_argument('-s',help='search topics',type=str,default='')
   args = parser.parse_args()
   if args.s != '':
      search(args.s)
if __name__== "__main__":
   parser = argparse.ArgumentParser(description="githubweekly")
   parser.add_argument('-m',help='mail address',type=str,required=True, default='')
   args = parser.parse_args()
   search_pattern = "created:>`date --date '-7 days' '+%Y-%m-%d'`"
   send_mail(args.m,gen_html(get_readme(search(search_pattern,output_file)),"{}.html".format(prefix)),"New 10 repos")
