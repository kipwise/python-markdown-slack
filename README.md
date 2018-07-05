# python-markdown-slack
slack markdown extension for Python-Markdown https://github.com/Python-Markdown/markdown

Installation
- pip install -e git+git://github.com/wingleungchoi/python-markdown-slack.git#egg=python-markdown-slack
- Try the following codes
```python
  import markdown
  from python_markdown_slack import PythonMarkdownSlack
  result = markdown.markdown('... Some *bold*', extensions=[PythonMarkdownSlack()])
  print(result) #=> <p>... Some <strong>bold</strong></p>
```

Test script
- python test.py

For development of the library
- 1. git clone git@github.com:wingleungchoi/python-markdown-slack.git
- 2. python setup.py develop
- 3. python learnExtension.py

Reference: 
- https://github.com/Python-Markdown/markdown/wiki/Tutorial:-Writing-Extensions-for-Python-Markdown
- https://github.com/dkeeghan/slackformatter.js

Powered By:
-  Kipwsie <https://kipwise.com>
