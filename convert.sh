#!/bin/bash

FILE_TO_CONVERT=$1
#COLUMN=$2

echo -n "Enter number of columns per line: "
read COLUMN

if [[ -f "$1.temp" ]];then
    echo "Backingup old \"$1\" file."
    mv "$1.temp" "$1.temp-$(date +%d-%m-%Y_%H-%M)"
fi

if [[ -f $1 ]]; then
    echo  "Converting..."
    cat $1 | awk '{print $1,$2}' | sed 's/ /:/g' > "$1.temp"
    while mapfile -t -n $COLUMN ary && ((${#ary[@]})); do printf -- "movech -perm -ovrd "; printf '%s ' "${ary[@]}" | tr '\n' ' '; printf -- '\r\n'; done < "$1.temp" > "converted_$1"
    rm "$1.temp"
    echo "Done"
fi
