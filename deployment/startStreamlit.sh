#!/bin/bash
cd /home/streamlit/streamlitApps
cd $1

test -f output.log || touch output.log
echo '--------- STARTING streamlit app ---------' >> output.log
echo $(date -u) >> output.log
/home/streamlit/.local/bin/streamlit run *.py >> output.log
echo $(date -u) >> output.log
echo '--------- STOPPING streamlit app ---------' >> output.log