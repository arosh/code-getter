# coding: utf-8
from __future__ import print_function
import sys
import os.path
import glob
import sqlite3
import tarfile
import itertools
from multiprocessing import Pool
from HTMLParser import HTMLParser

def get_script_dir():
    return os.path.dirname(
            os.path.abspath(__file__))

class GetCode(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_pre_tag = False
        self.code = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'pre' and attrs['id'] == 'code':
            self.in_pre_tag = True

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.in_pre_tag = False

    def handle_data(self, data):
        if self.in_pre_tag:
            self.code += data.decode('UTF-8')

    def handle_charref(self, ref):
        if self.in_pre_tag:
            self.code += self.unescape('&#' + ref + ';')

    def handle_entityref(self, name):
        if self.in_pre_tag:
            self.code += self.unescape('&' + name + ';')

def task(fname):
    with tarfile.open(fname, 'r:bz2') as f:
        for name in f.getnames():
            (run_id, _) = os.path.splitext(name)
            run_id = int(run_id)
            data = ''.join(f.extractfile(name).readlines())
            get_code = GetCode()
            get_code.feed(data)
            if get_code.code == 'You are not authorized to see this code.':
                return dict(run_id=run_id, code=None)

            return dict(run_id=run_id, code=get_code.code)

def main():
    conn = sqlite3.connect(
            os.path.join(get_script_dir(), 'online_judge.sqlite3'))

    with conn:
        conn.row_factory = sqlite3.Row

        ended = set()

        cur = conn.cursor()
        cur.arraysize = 256

        rows = cur.execute('SELECT run_id FROM codes')
        ended.update(
                os.path.join(
                    get_script_dir(),
                    'review_page',
                    str(row['run_id']) + '.html.tar.bz2')
                for row in rows)

        rows = cur.execute('SELECT run_id FROM unauthorized_codes')
        ended.update(
                os.path.join(
                    get_script_dir(),
                    'review_page',
                    str(row['run_id']) + '.html.tar.bz2')
                for row in rows)

        pathname = os.path.join(get_script_dir(), 'review_page', '*.html.tar.bz2')
        files = glob.iglob(pathname)
        files = itertools.ifilterfalse(lambda item: item in ended, files)

        p = Pool(None)
        result = p.imap_unordered(task, files, 1000)
        # ジェネレータは一度読み取ると消えて無くなるのでコピーする
        ok, ng = itertools.tee(result)
        ok = itertools.ifilterfalse(lambda item: item['code'] is None, ok)
        ng = itertools.ifilter(lambda item: item['code'] is None, ng)
        conn.executemany('INSERT INTO codes(run_id, code) VALUES(:run_id, :code)', ok)
        conn.executemany('INSERT INTO unauthorized_codes(run_id) VALUES(:run_id)', ng)

if __name__ == '__main__':
    main()
