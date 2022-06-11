curl https://www.plurk.com/{username} -o plurk_res_tmp.html
response_count=$(cat plurk_res_tmp.html | grep -oP '(?<=response_count">)(\d+)(?=</td>)')
last_visit=$(cat plurk_res_tmp.html | grep -oP "(?<=last_visit = new Date\(\')[\d\-\s:]+(?=\')")

echo "$(date -u +'%Y-%m-%d %H:%M:%S'),$response_count,$last_visit" >> /tmp/plurk_response.csv
rm plurk_res_tmp.html
