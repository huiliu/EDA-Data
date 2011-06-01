#!/bin/bash

if [ $# -eq 0 ];then
    echo "Input error! Please enter an file name."
    echo "singleEda [-r --report|-s --summary] FileName"
    exit 1
fi

for file in ./*.lcd
do
    if refine "$file"; then
        echo "$file"
        if [[ "$1" == "-c" ]]; then
            offset $1 "${file%.*}.tmp">>LCD
        elif [[ "$1" == "-s" ]]; then 
            offset $1 "${file%.*}.tmp"
        else
            echo "Input error!"
            exit 1
        fi
    fi
done
