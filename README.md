#Copernicus


Osint tool to get results from Google, Bing, Yahoo, PagesBlanches about people.

Then make a graph in neo4j .

 - usage: copernicus.py [-h] [-l 'LANG'] [-pb 'PB'] [-s 'NAME'] [-f
   FAMILY NAME]
                        [-a OPTION] [-c CITY]
   
   optional arguments:   -h, --help            show this help message
   and exit   -l 'LANG', --language 'LANG'
                           Country : en,zh-CN,es,ar,pt,ja,ru,fr,de...   -pb 'PB', --pagesblanches 'PB'
                           -pb true : Only use the city arg with pagesblanches   -s 'NAME', --search 'NAME'
                           Name to Search   -f FAMILY NAME, --family FAMILY NAME
                           Specify Family name if any (needed with -a and to use
                           pageblanche)ex: -s Albert Einstein -f Einstein -a
                           relativity,physics   -a OPTION, --add OPTION
                           Additional information to catch more results: --add
                           Word1,Word2,Word3   -c CITY, --city CITY  Specify city



