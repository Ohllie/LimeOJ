#!/bin/bash

DIR=$(dirname $(readlink -f $0))

if [ $# -ne 1 ]; then
  echo "Usage: $0 [test/prod]"
  exit 1
fi

SERVER="$1"

case $SERVER in
  test )
      ( cd "$DIR" && ansible-playbook -v -l staging playbook.yml )
  ;;
  prod )
    read -p "Are you sure you want to deploy to production? <y/N> " prompt
    if [[ $prompt == "y" || $prompt == "Y" || $prompt == "yes" || $prompt == "Yes" ]]; then
      ( cd "$DIR" && ansible-playbook -l production playbook.yml )
    else
      exit 1
    fi
  ;;
  * )
    echo "Unknown server $SERVER"  
    exit 1
  ;;
esac
