#!/bin/bash

# usage: tag-hive-thumbs.sh metadata.db girlid
# e.g. tag-hive-thumbs.sh ../hivedata.db 2258686

sqlite3 $1 'select printf("f=%d-%d.jpg ; if [[ -f $f ]] ; then exiftool -v -DATETIME=""%s"" $f ; fi", girlid, id, tstamp) from thumb where girlid = '$2';' | bash
