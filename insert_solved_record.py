# coding: utf-8
from __future__ import print_function
import sys
import os.path
import glob
import sqlite3
import xml.etree.ElementTree

def get_script_dir():
    return os.path.dirname(
            os.path.abspath(__file__))

def extract(e, **arg):
    o = {}
    for (attr, func) in arg.iteritems():
        o.update({ attr: func(e.find(attr).text.translate(None, '\r\n')) })
    return o

def main():
    conn = sqlite3.connect(
            os.path.join(get_script_dir(), 'online_judge.sqlite3'))

    with conn:
        pathname = os.path.join(get_script_dir(), 'solved_record', '*.xml')
        for fname in glob.iglob(pathname):
            tree = xml.etree.ElementTree.parse(fname)
            root = tree.getroot()
            def generate(root):
                for e in root.findall('solved'):
                    o = extract(e, run_id=int, user_id=str, problem_id=str,
                            date=int, language=str, cputime=int, memory=int,
                            code_size=int)
                    yield o

            conn.executemany('INSERT INTO solved_records(run_id, user_id, problem_id, date, language, cputime, memory, code_size) VALUES(:run_id, :user_id, :problem_id, :date, :language, :cputime, :memory, :code_size)', generate(root))
            print(fname)

if __name__ == '__main__':
    main()
