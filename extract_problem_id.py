import os.path
import glob
import xml.etree.ElementTree

def get_script_dir():
    return os.path.dirname(
            os.path.abspath(__file__))

def main():
    pathname = os.path.join(get_script_dir(), 'problem_list', '*.xml')
    for fname in glob.iglob(pathname):
        tree = xml.etree.ElementTree.parse(fname)
        root = tree.getroot()
        id_list = [e.find('id').text.translate(None, '\r\n')
                    for e in root.findall('problem')]
        root, ext = os.path.splitext(fname)
        listname = root + '.txt'
        with open(listname, 'w') as f:
            for i in id_list:
                f.write(str(i) + '\n')

if __name__ == '__main__':
    main()
