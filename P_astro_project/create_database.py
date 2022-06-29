"""This script will import the .csv of the samples and turn in into an sqlite3 database. This is mainly for exploring SQL databases, it is not expected to hold any advantage over working with the .csv file."""

import csv
import sqlite3
import glob
import os

file_path = "../outputs/params_inc_FAR.csv"

def do_directory(dirname, db):
    """
    Perform the conversion of the .csv file into an SQLite3 database.
    
    Parameters
    ----------
    dirname: string
        File path to the directory of the .csv file.
    db: string
        Location and name of the database to be created.
    """
    for filename in glob.glob(os.path.join(dirname, 'params_inc_FAR.csv')):
        convert_file(filename, db)

def convert_file(filename, db):
    """
    Perform the conversion of the .csv file into an SQLite3 database.
    
    Parameters
    ----------
    dirname: string
        File path to the directory of the .csv file.
    db: string
        Location and name of the database to be created.
    """
    with open(filename) as f:
        with db:
            data = csv.DictReader(f)
            cols = data.fieldnames
            table=os.path.splitext(os.path.basename(filename))[0]

            sql = f'drop table if exists "{table}"'
            db.execute(sql)

            sql = 'create table "{table}" ( {cols} )'.format(table=table, cols=','.join(f'"{col}"' for col in cols))

            db.execute(sql)

            sql = 'insert into "{table}" values ( {vals} )'.format(table=table, vals=','.join('?' for _ in cols))

            db.executemany(sql, (list(map(row.get, cols)) for row in data))

if __name__ == '__main__':
    conn = sqlite3.connect('../outputs/database.db')
    do_directory('../outputs/', conn)