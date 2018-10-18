#!/bin/bash

# splitimages.sh
#  Take a directory of photos and create/populate subdirectories of "Geotagged" and "Nongeotagged" photos

# Directory arg
if [ "$1" = "" ]; then
  dir="."
else
  dir=$1
fi
#echo $dir


# Make directories
if [ ! -d "$dir/Geotagged" ]; then
    echo "Creating Geotagged directory"
    mkdir "$dir/Geotagged"
else
    echo "No need to create Geotagged directory"
fi

if [ ! -d "$dir/Nongeotagged" ]; then
    echo "Creating Nongeotagged directory"
    mkdir "$dir/Nongeotagged"
else
    echo "No need to create Nongeotagged directory"
fi

# Sort through photos and divide them up
for file in `ls $dir`
do
    # Skip nonjpgs
    filename=$(basename -- "$file")
    extension="${filename##*.}"    
    if [ ! "$extension" = "jpg" ]; then
        echo "Skipping $file"
        continue
    fi

    num=`exiftool "$dir/$file" |  grep GPS | cut -d " " -f 2 | wc -l`
    # num = num of lines of GPS data in EXIF of photo
    if [ "$num" -eq "0" ]; then
        echo "Want to copy file $file to: '$dir/Nongeotagged/$file'"
        cp "$dir/$file" "$dir/Nongeotagged/$file"
    else
        echo "Want to copy file $file to: '$dir/Geotagged/$file'"
        cp "$dir/$file" "$dir/Geotagged/$file"
    fi
done

