#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(debug='False', url='mysql+pymysql://root:@localhost/plate_spinner?charset=utf8mb4', repository='.')