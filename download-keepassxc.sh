#!/bin/bash
LOCATION=$(curl -s https://api.github.com/repos/keepassxreboot/keepassxc/releases/latest \
| grep "browser_download_url" \
| grep 'x86_64.dmg"' \
| awk '{ print $2 }' \
| sed 's/"//g')
curl -s -L -O "$LOCATION"
curl -s -L -O "$LOCATION.DIGEST"
DIGEST=`ls *.DIGEST`
shasum -a 256 -c "$DIGEST"