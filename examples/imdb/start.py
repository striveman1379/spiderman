
# entry parameters:  crawl redis -s SPIDERMAN_SETTINGS=spider.settings

import re
import sys

from scrapy.cmdline import execute

if __name__ == '__main__':
    argv = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.argv[0] = argv
    sys.exit(execute())