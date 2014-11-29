from __future__ import print_function
import os
import os.path
import glob
import time
import urllib
import urllib2
import tarfile
import xml.etree.ElementTree

def get_script_dir():
    return os.path.dirname(
            os.path.abspath(__file__))

def get_solved_record(fname):
    tree = xml.etree.ElementTree.parse(fname)
    root = tree.getroot()
    return [e.find('run_id').text.translate(None, '\r\n')
                for e in root.findall('solved')]

def download(run_id, dirname):
    url = 'http://judge.u-aizu.ac.jp/onlinejudge/review.jsp'
    values = { 'rid' : run_id }
    full_url = url + '?' + urllib.urlencode(values)

    htmlname = os.path.join(dirname, '{}.html'.format(run_id))
    tarname = htmlname + '.tar.bz2'
    if os.path.exists(tarname):
        print('S', end='')
        return

    body = urllib2.urlopen(full_url).read()
    with open(htmlname, 'w') as f:
        f.write(body)

    with tarfile.open(tarname, 'w:bz2') as f:
        f.add(htmlname, arcname='{}.html'.format(run_id))

    os.remove(htmlname)

    print('D', end='')
    time.sleep(3)

def main():
    pathname = os.path.join(get_script_dir(), 'solved_record', '*.xml')
    dirname = os.path.join(get_script_dir(), 'review_page')
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    for fname in glob.iglob(pathname):
        print(fname, end=' ')
        for run_id in get_solved_record(fname):
            download(run_id, dirname)

        print()

if __name__ == '__main__':
    main()
