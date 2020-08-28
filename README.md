# Cut the verdict
判決書切割與結構化工具

## 安裝
安裝套件(form Source) **recommend**
```sh
pip install -U git+https://github.com/seanbbear/VerdictCut.git
```

安裝套件(form PyPI)
```sh
pip install VerdictCut
```
## 使用
- `break_line`: 文件本身使用的換行符號，請務必設置正確
    - windows(CRLF): `\r\n`
    - linux(LF): `\n`
### 找人物
```python
def find_roles(cj_doc, target_roles=['上訴人', '被告', '選任辯護人'], break_line='\r\n', name_length_limit=25, search_rows_limit=100):
```
```python
from VerdictCut import find_roles
roles = find_roles(text)
print(roles)
```

### 找主文
```python
def find_maintext(judgement, break_line='\r\n'):
```
```python
from VerdictCut import find_maintext
maintext = find_maintext(text)
print(maintext)
```

### 找事實(段落分割)
```python
def find_fact(judgement, break_line='\r\n'):
```
```python
from VerdictCut import find_fact
fact = find_fact(text)
print(fact)
```

### 找事實(無分割)
```python
def extract_fact(judgement, break_line='\r\n'):
```
```python
from VerdictCut.find_fact import extract_fact
```

### 找論罪科刑
```python
def find_justice(judgement, break_line = '\r\n'):
```
```python
from VerdictCut import find_justice
justice = find_justice(text)
print(justice)
```

### 找附錄法條
```python
def find_laws(judgement, break_line='\r\n'):
```
```python
from VerdictCut import find_laws
laws = find_laws(laws))
print(laws)
```