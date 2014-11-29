import os
import os.path
import time
import urllib
import urllib2

def get_script_dir():
    return os.path.dirname(
            os.path.abspath(__file__))

def main():
    dirname = os.path.join(get_script_dir(), 'problem_list')
    volumes = ['0', '1', '2', '5', '6',
               '10', '11', '12', '13', '15',
               '20', '21', '22', '23', '24',
               '25', '100']

    print dirname

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    for volume in volumes:
        url = 'http://judge.u-aizu.ac.jp/onlinejudge/webservice/problem_list'
        values = { 'volume' : volume }
        url_values = urllib.urlencode(values)
        full_url = url + '?' + url_values
        print full_url
        body = urllib2.urlopen(full_url).read()
        fname = os.path.join(dirname, 'volume{}.xml'.format(volume))
        with open(fname, 'w') as f:
            f.write(body)
        time.sleep(3)

if __name__ == '__main__':
    main()
