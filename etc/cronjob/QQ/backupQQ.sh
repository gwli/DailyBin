cmd="select content,group_name,nickname from chat_logs where date(create_time) = curdate() order by group_number,qq;"
datafile="im_`date +%Y_%m_%d`.rst"
#mysql -N -B --default-character-set=utf8 -u root -pdevtoolsqa -DIM -e "$cmd" >$datafile
mysql -N  --default-character-set=utf8 -u root -pdevtoolsqa -DIM -e "$cmd" >$datafile
pandoc $datafile -t html| mutt -e "set content_type=text/html" -s "$datafile" gangwei.li@outlook.com
