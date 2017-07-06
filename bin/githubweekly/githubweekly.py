#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import imp
import datetime
import argparse
today=datetime.datetime.now().strftime("%Y_5m_%d")
prefix="github_{}".format(today)
def gen_init_file():
    output_file = "{}_input.py".format(prefix)
    sh_script="""
echo "# -*- coding=utf-8 -*-" >{0}
echo "repo_list=[" >>{0}
curl -G https://api.github.com/search/repositories       \
    --data-urlencode "q=created:>`date --date '-7 days' '+%Y-%m-%d'`" \
    --data-urlencode "sort=stars"                          \
    --data-urlencode "order=desc"                          \
    -H "Accept: application/vnd.github.preview"            \
    | jq ".items[0,1,2,3,4,5,6,7] | {{ name, description, language, watchers_count, html_url }}" |sed -e 's/null/None/g' |sed -e 's/}}/}},/g' >> {0}
echo "]">> {0}
""".format(output_file)
    print sh_script
    os.system(sh_script)
    return output_file

def get_readme(input_file):
    data = imp.load_source("data",input_file)
    outputfiles = ["index.md"]
    with open("index.md",'w') as f:
        for index,ele in enumerate(data.repo_list):
            f.write("# {}\n".format( ele['name']))
            f.write("* language {},watchers_count{}\n".format(ele['language'],ele['watchers_count']))
            f.write("* <{}>\n".format( ele['html_url']))
            f.write("* {}\n".format( ele['description']))
            f.write("*\n")
            repo= ele['html_url'].split('/')[-2:]
            print repo
            read_me = " https://raw.githubusercontent.com/{}/{}/master/README.md".format(repo[0],repo[1]) 
            print read_me
            #os.system("curl {}>{}_{}.html".format(ele['html_url'],index,ele['name']))
            md_file = "{}_{}.md".format(index,ele['name'])
            os.system("curl {}>{}".format(read_me,md_file))
            outputfiles.append(md_file)
    return outputfiles
        
def gen_html(md_files):
    html="{}.html".format(prefix)
    shell_scripts = "cat {} |markdown >{}".format(" ".join(md_files),html)
    os.system(shell_scripts)    
    return html

def send_mail(mail,html):
    cmd = """mutt -e "set content_type=text/html" -s "[Github] New top 10 repos `date +%Y/%m/%d`" {}< {}""".format(mail,html)
    os.system(cmd) 
    os.system("rm -fr *.md")

if __name__== "__main__":
   parser = argparse.ArgumentParser(description="githubweekly")
   parser.add_argument('-m',help='mail address',type=str,required=True, default='')
   args = parser.parse_args()
   #gen_init_file()
   send_mail(args.m,gen_html(get_readme(gen_init_file())))
