# -*- coding: utf-8 -*-
#Python 2.7 버전 사용
import csv
import sys

filename = 'Stock_list.csv'
f = open(filename, 'rb')
reader = csv.reader(f)


try:
    for row in reader:
        for r in row:
            print r.decode('euckr').encode('utf-8')

except csv.Error as e:
    sys.exit('file %s, line %d: %s \n' % (filename, reader.line_num, e))
f.close()
