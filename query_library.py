#encoding:utf-8

import codecs
downloaded = []
unavailable = []

try:
  with codecs.open( "books_records_out.txt", 'r+' ) as f:
    downloaded = [  (l[:l.find('|')]).decode("utf-8") for l in f.readlines() ]
except: downloaded = []
try:
  with codecs.open( "books_records_unavailable.txt", 'r+' ) as f:
    unavailable = [  l.decode('utf-8').replace('\n','').replace('\r','') for l in f.readlines() ]
except: unavailable = []

print "unavailable:", len(unavailable)
print "downloaded:", len(downloaded)

from selenium_lib import query_book

passed_list = []
last_unavailable = []
new_unavailable = []
total_books = 0
count_downloaded = 0
count_unavailable = 0
count_new_unavailable = 0
count_new_downloaded = 0
count_repetitions = 0
count_wrong_year = 0
count_new_wrong_year = 0

import codecs
with codecs.open( "books_records_out.txt", 'a+', encoding="utf-8" ) as outf:
    with codecs.open( "records.txt", 'r', encoding="utf-8" ) as bf:
        lines = [  l.replace('\n','').replace('\r','') for l in bf.readlines() ]
        total_books = len( lines )
        for i,line in enumerate(lines):

            if line=="END": break; # Прекратить обработку, если встречается этот индикатор

            if line in passed_list: count_repetitions = count_repetitions+1;
            else:
              passed_list.append( line )

              if line in downloaded:
                  #print i+1, 'downloaded';
                  count_downloaded = count_downloaded+1;
              elif line in unavailable:
                  last_unavailable.append( line )
                  #print i+1, 'unavailable';
                  count_unavailable = count_unavailable+1;

                  # Для полноты картины, попробуем поискать эту же книгу, но без года
                  if u'$' in line:
                      line = line.split('$')[0]

                      if line not in passed_list:
                        passed_list.append( line )
  
                        if line in downloaded:
                            #print i+1, 'downloaded';
                            count_wrong_year = count_wrong_year + 1;
                        elif line in unavailable:
                            continue
                            #print i+1, 'unavailable';
                        else:
                            info = query_book( line.replace('$',' ') )
                            if info:
                              outf.write( line + '|' + '|'.join(info) + '\n' )
                              print i+1
                              count_new_wrong_year = count_new_wrong_year + 1
                            else:
                              new_unavailable.append( line )
                              print i+1, '-'

              else:
                  info = query_book( line.replace('$',' ') )
                  if info:
                    outf.write( line + '|' + '|'.join(info) + '\n' )
                    print i+1
                    count_new_downloaded = count_new_downloaded + 1
                  else:
                    last_unavailable.append( line )
                    count_new_unavailable = count_new_unavailable + 1
                    new_unavailable.append( line )
                    print i+1, '-'
            
                    # Для полноты картины, попробуем поискать эту же книгу, но без года
                    if u'$' in line:
                      line = line.split('$')[0]

                      if line not in passed_list:
                        passed_list.append( line )
  
                        if line in downloaded:
                          #print i+1, 'downloaded';
                          count_wrong_year = count_wrong_year + 1;
                        elif line in unavailable:
                          continue;
                        #  #print i+1, 'unavailable';
                        else:
                            info = query_book( line.replace('$',' ') )
                            if info:
                              outf.write( line + '|' + '|'.join(info) + '\n' )
                              print i+1
                              count_new_wrong_year = count_new_wrong_year + 1
                            else:
                              new_unavailable.append( line )
                              print i+1, '-'

with codecs.open( "books_records_unavailable.txt", 'a+', encoding="utf-8" ) as outf:
    for l in new_unavailable:
        outf.write( (l + "\n") )

with codecs.open( "books_records_last_unavailable.txt", 'w', encoding="utf-8" ) as outf:
    for l in last_unavailable:
        outf.write( (l + "\n") )

print "From", total_books, 'book records (%d plus %d repetitions)' % (total_books - count_repetitions, count_repetitions)
print count_downloaded, "-- already downloaded", "(%d new)" % count_new_downloaded
print count_unavailable, "-- still unavailable", '(%d new)' % count_new_unavailable
print "-- successful without year: %d (%d new)" % (count_wrong_year, count_new_wrong_year)
print "OK/NOK: %d/%d" % (count_downloaded + count_new_downloaded, count_new_unavailable + count_unavailable)

