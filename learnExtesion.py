import markdown
from myextension import MyExtension
txt = """
... Some __underline__
... Some ~strike~
... Some *bold*
... Some _italics_
... Some `import myextension`
... """

result = markdown.markdown(txt, extensions=[MyExtension()])
print(result)