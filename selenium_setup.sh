#!/bin/bash -xe

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "\n${GREEN}[LOGS] Checking for geckodriver in \$PATH variable ...${NC}"

num=$(which geckodriver | wc -l)
isGeckoInPATH=false

if [ ${num} -ge 1 ]; then isGeckoInPATH=true; fi

if ${isGeckoInPATH}; then
    echo -e "\n${GREEN}[LOGS] geckodriver is available in \$PATH ...${NC}"
else
    echo -e "\n${GREEN}[LOGS] geckodriver is NOT available in \$PATH ...${NC}"
    echo -e "\n${GREEN}[LOGS] Removing any existing geckodriver file in \$PWD ...${NC}"
    rm -f geckodriver* || true
    
    echo -e "\n${GREEN}[LOGS] Download and extract geckodriver in \$PWD and add it to \$PATH ...${NC}"
    wget --no-check-certificate https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz
    tar -xvzf geckodriver-v0.23.0-linux64.tar.gz
    rm -f geckodriver-v0.23.0-linux64.tar.gz || true
    export PATH=$PWD:$PATH
fi

echo -e "\n${GREEN}[LOGS] Upgrading urllib3 python module to 1.23 version ...${NC}"
sudo pip install --upgrade --ignore-installed urllib3==1.23 || true
sudo pip install selenium

echo -e "${GREEN}[LOGS] DONE!${NC}"

