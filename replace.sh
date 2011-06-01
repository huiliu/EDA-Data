#!/bin/bash

for file in `ls *`
do
    echo $file
    sed -i 's/#!\/export\/home\/liuhui\/opt\/python3\/bin\/python3/#!\/export\/home\/liuhui\/opt\/bin\/python3/1' $file
done
