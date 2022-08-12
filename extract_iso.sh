#!/bin/bash

for i in `ls *.iso`; do
    FILE_NAME="${i%%.*}"
    echo -n "Extracting ${i} file, please wait..."
	photorec /d "$FILE_NAME" /cmd "${i}" fileopt,everything,disable,mov,enable,rar,enable,search 1> /dev/null  2>&1
	echo " OK"
	pushd "${i%%.*}.1" 
	echo "Truncating..."
	for j in `ls *.mp4`; do
	    FILE_SIZE=$(ls ${j} -l | awk "{print \$5}")
	    TRUNCATE_SIZE=$(((RANDOM%20)*(1024*1024)))
	    if [[ $TRUNCATE_SIZE -lt $FILE_SIZE ]]; then
		SIZE_DIFF=$(($FILE_SIZE-$TRUNCATE_SIZE))
	    else
		SIZE_DIFF=$(($FILE_SIZE/2))
	    fi
	    echo "File name: ${j}"
	    echo "File size: ${FILE_SIZE} KB"
	    echo "Truncate Size: ${TRUNCATE_SIZE} KB"
	    echo "Size Diff: ${SIZE_DIFF}"
	    
	    head -c ${SIZE_DIFF}  < /dev/urandom > f0
	    truncate ${j} --size=${TRUNCATE_SIZE}
	    cat ${j} f0 > ${j}_new && rm ${j} && rm f0 && mv ${j}_new ${j}
	    echo "....................................................."
	done
    popd
    echo -n "Compressing $FILE_NAME directory, please wait..."
	mv "${FILE_NAME}.1" $FILE_NAME 
	rm $FILE_NAME/report.xml
	tar cvf "${FILE_NAME}.tar" $FILE_NAME 1> /dev/null 2>&1 && rm -rf $FILE_NAME
	echo " OK"
done