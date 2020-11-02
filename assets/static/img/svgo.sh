#!/bin/bash
for f in cta/cta-icon_*.svg
do
    dirname=$(dirname "$f")
    filename=$(basename "$f")
    ext="${filename##*.}"
    filename="${filename%.*}"
    if [[ $filename == *-opt ]]
    then
        continue
    fi
	outname="$dirname/${filename}-opt.$ext"
    echo "optimizing $f"
    svgo -i $f -o $outname
done
