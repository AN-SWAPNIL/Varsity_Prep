"""Regression checks on the new workbook examples, extracted from their Markdown."""
from pathlib import Path
import ast
import math
import random
import re
import shutil
import sqlite3
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build' / 'seniors_audit' / 'checks'
OUT.mkdir(parents=True, exist_ok=True)
random.seed(17)
checks = 0

def check(condition, label):
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1

def markdown(prefix):
    return next(ROOT.glob(prefix + '*.md')).read_text(encoding='utf-8')

def functions(prefix, wanted, extra=None):
    ns = dict(extra or {})
    found = set()
    for block in re.findall(r'```python\n(.*?)\n```', markdown(prefix), re.S):
        if not any('def ' + name + '(' in block for name in wanted):
            continue
        tree = ast.parse(block)
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in wanted]
        found.update(n.name for n in nodes)
        exec(compile(ast.Module(body=nodes, type_ignores=[]), '<markdown>', 'exec'), ns)
    check(found == set(wanted), 'all requested functions found: ' + prefix)
    return ns

dsa = functions('01_', ['exponential_search', 'max_profit', 'counting_sort',
                        'radix_sort', 'bucket_sort', 'shell_sort'])
for n in range(41):
    for _ in range(8):
        a = [random.randrange(100) for _ in range(n)]
        expected = sorted(a)
        check(dsa['counting_sort'](a, 100) == expected, 'counting')
        check(dsa['radix_sort'](a) == expected, 'radix')
        b = a[:]
        dsa['shell_sort'](b)
        check(b == expected, 'shell')
        f = [x / 100 for x in a]
        check(dsa['bucket_sort'](f) == sorted(f), 'bucket')
        optimum = max([0] + [a[j]-a[i] for i in range(n) for j in range(i+1,n)])
        check(dsa['max_profit'](a) == optimum, 'one transaction')
        def read(i):
            return expected[i] if i < len(expected) else None
        for key in (-1, 0, 10, 55, 99, 101):
            pos = dsa['exponential_search'](read, key)
            check((pos == -1 and key not in expected) or
                  (0 <= pos < n and expected[pos] == key), 'exponential search')

nt = functions('10_', ['egcd', 'inverse_mod', 'diophantine', 'bigmod', 'factorize', 'sieve', 'crt'])
for a in range(1, 50):
    for b in range(1, 30):
        g,x,y = nt['egcd'](a,b)
        check(g == math.gcd(a,b) and a*x+b*y == g, 'Bezout')
        if b > 1 and g == 1:
            check(a*nt['inverse_mod'](a,b) % b == 1, 'inverse')
    check(nt['bigmod'](a,13,17) == pow(a,13,17), 'bigmod')
    factors = nt['factorize'](a)
    check(math.prod(p**e for p,e in factors) == a, 'factorization')
check(nt['sieve'](20) == [2,3,5,7,11,13,17,19], 'sieve example')
check(nt['crt']([2,3,2],[3,5,7]) == (23,105), 'CRT example')
x,y,dx,dy = nt['diophantine'](6,9,24)
check(all(6*(x+t*dx)+9*(y+t*dy)==24 for t in range(-5,6)), 'Diophantine family')
check(nt['diophantine'](6,9,25) is None, 'Diophantine unsolvable')
check(struct.pack('>f',-13.25).hex() == 'c1540000', 'IEEE binary32')
check(pow(17,6,23)==pow(8,7,23)==12, 'DH Alice-Mallory')
check(pow(17,15,23)==pow(19,7,23)==15, 'DH Bob-Mallory')
check(10*10 % 49 == 2, 'Hensel example')

mealy = {'A': [('A',0),('B',0)], 'B': [('C',0),('B',0)], 'C': [('A',0),('B',1)]}
moore = {'A': ['A','B'], 'B': ['C','B'], 'C': ['A','D'], 'D': ['C','B']}
for length in range(1,9):
    for value in range(2**length):
        bits = format(value, f'0{length}b')
        s,t = 'A','A'
        for i,bit in enumerate(bits):
            s,out = mealy[s][int(bit)]
            t = moore[t][int(bit)]
            goal = int(bits[:i+1].endswith('101'))
            check(out == goal and int(t=='D') == goal, 'overlapping FSM')

db = sqlite3.connect(':memory:')
db.execute('PRAGMA foreign_keys=ON')
sql = next(b for b in re.findall(r'```sql\n(.*?)\n```', markdown('05_'), re.S)
           if 'CREATE TABLE OrderLine' in b and 'CREATE TABLE Customer' in b)
db.executescript(sql)
db.executescript("INSERT INTO Customer VALUES (2,'Rina'); INSERT INTO Product VALUES ('P1'),('P2');"
                 "INSERT INTO OrderHeader VALUES (9,2); INSERT INTO OrderLine VALUES (9,1,'P1',2,120),(9,2,'P2',1,50);")
check(db.execute('SELECT SUM(qty*unit_price) FROM OrderLine').fetchone()[0] == 290, 'SQL migration total')
try:
    db.execute("INSERT INTO OrderLine VALUES (9,3,'P1',0,2)")
    raise AssertionError('CHECK constraint should fail')
except sqlite3.IntegrityError:
    checks += 1

try:
    import numpy as np
except ImportError:
    print('NumPy unavailable: PCA/LSTM runtime checks skipped; formulas checked separately.')
else:
    ml = functions('11_', ['pca_fit','lstm_cell'], {'np':np})
    mean,v,scores,_ = ml['pca_fit']([[1,1],[2,2],[3,3]],1)
    check(np.allclose(scores@v.T + mean, [[1,1],[2,2],[3,3]]), 'PCA reconstruction')
    weights = {k:np.zeros((1,2)) for k in 'fioc'}
    biases = {k:np.array([x]) for k,x in zip('fioc',[math.log(9),math.log(.25),math.log(4),math.atanh(.5)])}
    h,c = ml['lstm_cell'](np.array([0.]),np.array([0.]),np.array([2.]),weights,biases)
    check(np.allclose(c,1.9) and np.allclose(h,.8*np.tanh(1.9)), 'LSTM numerical step')

# Compile the complete friend-class example, not the intentionally incomplete teaching snippets.
compiler = shutil.which('g++')
if compiler:
    friend = next(b for b in re.findall(r'```cpp\n(.*?)\n```', markdown('03_'), re.S)
                  if 'class Second;' in b and 'int main()' in b)
    src,exe = OUT/'friend.cpp', OUT/'friend.exe'
    src.write_text(friend, encoding='utf-8')
    subprocess.run([compiler,'-std=c++17','-Wall','-Wextra',str(src),'-o',str(exe)],check=True)
    result = subprocess.run([str(exe)],text=True,capture_output=True,check=True)
    check(result.stdout.strip() == '11', 'compiled C++ friend result')

print(f'PASS: {checks} assertions on workbook additions. Existing full books were not all executed.')
