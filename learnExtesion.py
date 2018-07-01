import markdown
from myextension import MyExtension
txt = """
... Some __underline__
... Some ~strike~
... Some *bold*
... Some _italics_
... Some `import myextension`
... website link: <https://github.com/wingleungchoi/myextension>
... image link: <https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-02-15/316074573012_6e20e900d2366268a877_512.png>
... combination: _*~bold italics strikeout~*_
... usename: <@UBG4243ME> how is the project?
... channel: I refer to channel <#CBHSFG3T9|general>
... not channel: I don't refer to channel <#|general>
... """

result = markdown.markdown(txt, extensions=[MyExtension()])
print(result)

text_file = open("test.html", "w")
text_file.write(result)
text_file.close()
