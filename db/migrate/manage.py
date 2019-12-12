#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(debug='False', url='mysql+pymysql://root:@localhost/serial_stories_extractor?charset=utf8mb4', repository='.')
