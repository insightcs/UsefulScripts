#!/bin/bash
temp_file="file_result.txt"

function read_dir(){
	for file in `ls $1`
	do
		if [ -d $1"/"$file ]
		then
			if [[ $file != "3rd" -a $file != "Common" -a $file != "lib" -a $file != "include" -a $file != "build" ]]
			then
				read_dir $1"/"$file
			fi
		else
			name=$1"/"$file
			file -i --mime-encoding $name >> $temp_file
		fi
	done
} 

function analyze_file(){
	while read line
	do
		file_name=${line%%:*}
		char_set=${line##*=}
		if [[ $char_set == "iso-8859-1" ]];then
			char_set="GBK"
			old_file=$file_name".old"
			mv $file_name $old_file
			iconv -f $char_set -t "UTF-8" -c $old_file > $file_name
			echo "Convert "$file_name" from:"$char_set
		fi
	done < $1
}

#读取第一个参数
rm -rf $temp_file
if [[ $1 == "clean" ]];then
 	find . -name "*.old" -exec rm -f '{}' \;
else
	read_dir $1
	analyze_file $temp_file
	rm -rf $temp_file
fi