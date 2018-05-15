# -*- coding=utf-8 -*- import os
import os
import imp
import time 
def search(topic,ofile="input.py"):
    sh_script="""
echo "# -*- coding=utf-8 -*-" >{0}
echo "repo_list=[" >>{0}
curl -G https://api.github.com/search/repositories       \
    --data-urlencode "q={1}" \
    --data-urlencode "sort=stars"                          \
    --data-urlencode "order=desc"                          \
    -H "Accept: application/vnd.github.preview"            \
    | jq ".items[] | {{ name, description, language, watchers_count, html_url }}" |sed -e 's/null/None/g' |sed -e 's/}}/}},/g' >> {0}
echo "]">> {0}
""".format(ofile,topic)
    print sh_script
    os.system(sh_script)
    return ofile

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
        
def gen_html(md_files, html_file):
    shell_scripts = "cat {} |markdown >{}".format(" ".join(md_files),html_file)
    os.system(shell_scripts)    
    return os.path.abspath(html_file)

def send_mail(mail,html,subject="New top 10 repos"):
    cmd = """mutt -e "set content_type=text/html" -s "[Github] {} `date +%Y/%m/%d`" {}< {}""".format(subject,mail,html)
    print cmd
    os.system(cmd) 
    time.sleep(20)
    os.system("rm -fr *.md")
