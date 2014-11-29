# coding: utf-8
from __future__ import print_function
import os.path
import sqlite3

def get_script_dir():
    return os.path.dirname(
            os.path.abspath(__file__))

def main():
    conn = sqlite3.connect(
            os.path.join(get_script_dir(), 'online_judge.sqlite3'))
    with conn:
        # primary keyを振っておけばunique indexを付けたのと同様の効果が得られるらしい
        conn.execute('CREATE TABLE solved_records(solved_record_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, run_id INTEGER NOT NULL, user_id TEXT NOT NULL, problem_id TEXT NOT NULL, date INTEGER NOT NULL, language TEXT NOT NULL, cputime INTEGER NOT NULL, memory INTEGER NOT NULL, code_size INTEGER NOT NULL)')
        conn.execute('CREATE TABLE compressed_codes(compressed_code_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, run_id INTEGER NOT NULL, compressed_code NONE NOT NULL)')
        conn.execute('CREATE TABLE codes(code_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, run_id INTEGER NOT NULL, code TEXT NOT NULL)')
        conn.execute('CREATE TABLE unauthorized_codes(unauthorized_code_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, run_id INTEGER NOT NULL)')
        conn.execute('CREATE INDEX index_run_id_on_solved_records ON solved_records(run_id)')
        conn.execute('CREATE INDEX index_run_id_on_compressed_codes ON compressed_codes(run_id)')
        conn.execute('CREATE INDEX index_run_id_on_codes ON codes(run_id)')
        conn.execute('CREATE INDEX index_run_id_on_unauthorized_codes ON codes(run_id)')

if __name__ == '__main__':
    main()
