#!/bin/sh

script=`readlink -f $0`
script_name=`basename $script`

sudo cp -f $script /bin/
script="/bin/$script_name"
sudo chmod a+x $script
kill `ps -ef | grep $script | grep -v $$ | awk '{print $2}'` 
kill `ps -ef | grep "./$script_name" | grep -v $$ | awk '{print $2}'` 

if grep -q "$script" /etc/rc.local; then
    :
else
    sed "s#^exit 0#${script} >/dev/null \&\n&#g" /etc/rc.local >/tmp/rc.local
    sudo cp -f /etc/rc.local /etc/rc.local.bak
    sudo cp -f /tmp/rc.local /etc/rc.local
fi

HOST_IP=${DEVICE_SERVER:-10.19.224.241}
HOST_PORT="8051"

INTERVAL=1
UPDATE_INTERVAL=100

while true; do
    NAME=`cat /etc/hostname`
    while true; do
        if [ $? -eq 0 ]; then
            status=`printf "GET /update?hostname=$NAME HTTP/1.1\r\n" | /bin/nc $HOST_IP $HOST_PORT`
            if echo "x $status x" | grep -q "200 OK"; then
                echo "$NAME is registered to $HOST_IP!"
                break
            else
                echo "Failed to register. Try again in $INTERVAL second"
            fi
        fi
        sleep $INTERVAL
    done
    sleep $UPDATE_INTERVAL
done
