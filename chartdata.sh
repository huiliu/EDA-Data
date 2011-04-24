#!/bin/bash

if [ -z $1 ];then
    echo "Input Error!"
    echo "chartdata <filename>"
    exit 1
fi

awk '{print $7}' $1 |sed '1d'>/tmp/chartdata
echo '' >> /tmp/chartdata
