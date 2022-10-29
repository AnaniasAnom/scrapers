sqlite3 ../hivedata.db 'select printf("exiftool -v -DATETIME=""%s"" %d-%d.jpg", tstamp, girlid, id) from thumb;' | bash
