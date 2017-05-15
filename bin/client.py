import psutil
import socket
import requests

server_ip = "10.19.226.116:8051"
memory_size= psutil.virtual_memory().total
hostname = socket.gethostname()
url="http://{}/update?hostname={}&config=mem:{}".format(server_ip,hostname,memory_size)
url="http://{}/update".format(server_ip)
payload = {
    "hostname":hostname,
    "config": "mem:{}".format(memory_size)
}

print url,payload
#print requests.post(url)
print requests.post(url,data=payload)
