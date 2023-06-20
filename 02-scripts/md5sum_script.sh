## This script creates the md5 hash sums for the downloaded data for comparison with the ENA data base 


for file in *.gz; do
    if [ -f "$file" ]; then
        md5sum "$file" > "${file}.md5"
    fi
done
