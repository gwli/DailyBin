#! /usr/bin/env python

# Python's bundled WSGI server
from cgi import parse_qs
from wsgiref.simple_server import make_server
server_port= 7896
server_ip="10.19.226.116"
mysql_db = "/home/devtoolsqa8/git/dailybin/etc/lgzpwd.sl3"


def parse_data(environ):
    data = None
    if environ['REQUEST_METHOD'] == 'POST':
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        data = parse_qs(request_body)  # turns the qs to a dict
    elif environ['REQUEST_METHOD'] == 'GET':
        data = parse_qs(environ['QUERY_STRING'])

    return data

def application (environ, start_response):

    response_body = "404 Not Found!"
    status = '404 Not Found'

    # Sorting and stringifying the environment key, value pairs
    #response_body = [
    #    '%s: %s' % (key, value) for key, value in sorted(environ.items())
    #]
    #response_body = '\n'.join(response_body)

    client = environ['REMOTE_ADDR']
    path = environ['PATH_INFO']

    if path == '/':
        status = '200 OK'
        response_body = '''Usage:
GET   /                       Print help message and list all devices
GET   /gen_account(msg=XXXX)  generate aacount
GET   /gen_key(msg=XXXX,salt=XXX) generate key
GET   /encrypt(key=XXX,msg=XXX)   encrypt a message
POST  /update (key=xxxx,msg=xxx)  Update account db
GET   /decrypt(key=xxxx,msg=xxx)  decrypt a message 
'''

    elif path == '/list':
        status = '200 OK'

        option = None
        data = parse_data(environ)
        if data.has_key('hostname'):
            option = data['hostname'][0]

        devices = query(option)
        if not devices:
            if data.has_key('hostname'):
                response_body = 'Device "%s" is not exist!' % data['hostname'][0]
            else:
                response_body = 'Device table is empty now!'
        else:
            response_body = 'Exist devices:\n'
            response_body += '\tID\tHOSTNAME\tCONFIG\n'
            for i in devices:
                response_body += "\t%d\t%s\t%s\n" % (i[0], i[1], i[2])

    elif path == '/update':
        status = '200 OK'
        data = parse_data(environ) 
        print data
        if data.has_key('hostname') and data.has_key('config'):
            update(data['hostname'][0], data['config'][0])
            response_body = "Update '%s' with config '%s'!" % (data['hostname'][0], client)
        else:
            response_body = "hostname is not specified!"
    elif path == '/dl':
        status = '200 OK'
        response_body = """ """ 
    
        response_body += r"""my $server_endpoint = "http://{}:{}/update";""".format(server_ip,server_port)
        response_body += """
my $req =$ua->post($server_endpoint,[hostname =>"$hostname",config=>"mem:$mem_size"]); 
"""
    else:
        pass



    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)

    return [response_body]



def query(name=None):
    option = ""
    if name != None:
        option = " where hostname = '%s'" % name

    sql = MySQLdb.connect(
        host = mysql_host,
        db = mysql_db,
        user = mysql_user,
        passwd = mysql_passwd
        )
    cursor = sql.cursor()

    cursor.execute("select * from machine%s" % option)
    rows = cursor.fetchall()
    cursor.close()
    sql.close()

    return rows


def update(name, config):
    sql = MySQLdb.connect(
        host = mysql_host,
        db = mysql_db,
        user = mysql_user,
        passwd = mysql_passwd
        )
    cursor = sql.cursor()

    cursor.execute("insert into machine (hostname, config) values('%s', '%s') ON DUPLICATE KEY UPDATE config='%s'" %
            ( name, config,config)
            )
    sql.commit()
    cursor.close()
    sql.close()

# Instantiate the server
httpd = make_server (
    #'127.0.0.1', # The host name
    '',
    server_port, # A port number where to wait for the request
    application # The application object name, in this case a function
)

print "Serving on port %d" % server_port

# Wait for a single request, serve it and quit
httpd.serve_forever()
