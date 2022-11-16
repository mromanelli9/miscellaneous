#!/bin/bash
LOCATION=$(curl -s https://api.github.com/repos/keepassxreboot/keepassxc/releases/latest \
| jq -r '.assets[] | select(.name | endswith("x86_64.dmg")) | .browser_download_url')
curl -s -L -O "$LOCATION"
curl -s -L -O "$LOCATION.DIGEST"
DIGEST=`ls *.DIGEST`
shasum -a 256 -c "$DIGEST"