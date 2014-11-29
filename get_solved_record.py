import os
import os.path
import glob
import time
import urllib
import urllib2

def get_script_dir():
    return os.path.dirname(
            os.path.abspath(__file__))

def get_problem_list():
    pathname = os.path.join(get_script_dir(), 'problem_list', '*.txt')
    problem_list = []
    for fname in glob.iglob(pathname):
        with open(fname, 'r') as f:
            problem_list.extend([line.rstrip() for line in f])
    return problem_list

def main():
    problem_list = get_problem_list()

    dirname = os.path.join(get_script_dir(), 'solved_record')
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    for problem_id in problem_list:
        url = 'http://judge.u-aizu.ac.jp/onlinejudge/webservice/solved_record'
        values = { 'problem_id': problem_id }
        full_url = url + '?' + urllib.urlencode(values)
        print full_url,

        fname = os.path.join(dirname, '{}.xml'.format(problem_id))
        if os.path.exists(fname):
            print '... skipped'
            continue

        body = urllib2.urlopen(full_url).read()
        with open(fname, 'w') as f:
            f.write(body)
        print '... done'
        time.sleep(3)

if __name__ == '__main__':
    main()
