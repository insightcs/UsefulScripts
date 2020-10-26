#!/bin/bash

set -e

for file in `ls $1`
do
    file_name=$1/$file
    if [ -e "$file_name" ];then
        mv $file_name $1/"0_"$file
    fi
done

