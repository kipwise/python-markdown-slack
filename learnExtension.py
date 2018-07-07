import markdown
from python_markdown_slack import PythonMarkdownSlack
txt = """
... Some __underline__
... Some ~strike~
... Some *bold*
... Some _italics_
... Some `import python-markdown-slack`
... website link: <https://github.com/wingleungchoi/python-markdown-slack>
... website link with text: <https://github.com/wingleungchoi/python-markdown-slack|python-markdown-slack>
... image link: <https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-02-15/316074573012_6e20e900d2366268a877_512.png>
... combination: _*~bold italics strikeout~*_
... usename: <@UBG4243ME> how is the project?
... channel: I refer to channel <#CBHSFG3T9|general>
... not channel: I don't refer to channel <#|general>
... emoji: at least two goods in slack. e.g. +1: :+1: thumb up:  :thumbsup:
... preformatted: ```\nMy code goes here line 1\nMy code goes here line 2\nMy code goes here line 3\n```
> single blockquote >
>>> triple blockquote >>>
... """

result = markdown.markdown(txt, extensions=[PythonMarkdownSlack(), 'pymdownx.emoji'])
print(result)

text_file = open("test.html", "w")
text_file.write(result)
text_file.close()
