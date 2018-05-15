# -*- coding=utf-8 -*-
import os
summery=[
{
  "html_url": "https://github.com/wearehive/project-guidelines",
  "watchers_count": 2409,
  "language": "JavaScript",
  "description": "A set of best practices for JavaScript projects",
  "name": "project-guidelines"
},
{
  "html_url": "https://github.com/ApolloAuto/apollo",
  "watchers_count": 1760,
  "language": "C++",
  "description": "An open autonomous driving platform",
  "name": "apollo"
},
{
  "html_url": "https://github.com/jeromedalbert/real-world-react",
  "watchers_count": 900,
  "language": None,
  "description": "Real World React apps and their open source codebases for developers to learn from",
  "name": "real-world-react"
},
{
  "html_url": "https://github.com/tj/gh-polls",
  "watchers_count": 773,
  "language": "Go",
  "description": "Polls for GitHub issues and readmes",
  "name": "gh-polls"
},
{
  "html_url": "https://github.com/evilsocket/dnssearch",
  "watchers_count": 590,
  "language": "Go",
  "description": "A subdomain enumeration tool.",
  "name": "dnssearch"
},
{
  "html_url": "https://github.com/justjavac/the-front-end-knowledge-you-may-dont-know",
  "watchers_count": 465,
  "language": None,
  "description": ":innocent: 你可能不知道的前端知识点",
  "name": "the-front-end-knowledge-you-may-dont-know"
},
{
  "html_url": "https://github.com/exyte/ARTetris",
  "watchers_count": 432,
  "language": "Swift",
  "description": "Augmented Reality Tetris made with ARKit and SceneKit",
  "name": "ARTetris"
},
{
  "html_url": "https://github.com/GianlucaGuarini/icaro",
  "watchers_count": 392,
  "language": "JavaScript",
  "description": "Smart and efficient javascript object observer, ideal for batching DOM updates (~1kb)",
  "name": "icaro"
},
]

for index,ele in enumerate(summery):
    print "# {}".format( ele['name'])
    print "  language {},watchers_count".format(ele['language'],ele['watchers_count'])
    print "  {}".format( ele['html_url'])
    print "  {}".format( ele['description'])
    print "-"
    repo= ele['html_url'].split('/')[-2:]
    #print repo
    read_me = " https://raw.githubusercontent.com/{}/{}/master/README.md".format(repo[0],repo[1]) 
    #print read_me
    #os.system("curl {}>{}_{}.html".format(ele['html_url'],index,ele['name']))
    #os.system("curl {}>{}_{}.md".format(read_me,index,ele['name']))

