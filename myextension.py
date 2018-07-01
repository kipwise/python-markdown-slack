# existing markdown inlinePatterns
# https://github.com/Python-Markdown/markdown/blob/2.6/markdown/inlinepatterns.py

from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern
from markdown.inlinepatterns import SubstituteTagPattern

DEL_RE = r'(~)(.*?)~' # Strikeout in slack
INS_RE = r'(__)(.*?)__' # not slack ;-)
STRONG_RE = r'(\*)(.*?)\*' # Bold in slack
EMPH_RE = r'(_)(.*?)_' # Italics in slack
CODE_RE = r'(`)(.*?)`' # code in slack
PREFORMATTED_RE = r'(```)(.*?)```' # preformatted in slack
NEWLINE_RE = r'\n' # newline in slack
USERNAME_RE = r'(<@)(.*?)>' # username tag
# NOIMG = r'(?<!\!)'
# NOBRACKET = r'[^\]\[]*'
# BRK = (
#     r'\[(' +
#     (NOBRACKET + r'(\[')*6 +
#     (NOBRACKET + r'\])*')*6 +
#     NOBRACKET + r')\]'
# )
# USERNAME_RE = NOIMG + BRK + r'''\(\s*(<.*?>|((?:(?:\(.*?\))|[^\(\)]))*?)\s*((['"])(.*?)\12\s*)?\)'''

class MyExtension(Extension):
  def extendMarkdown(self, md, md_globals):
    # del md.inlinePatterns['backtick'] # `backtick style`

    del_tag = SimpleTagPattern(DEL_RE, 'del')
    md.inlinePatterns.add('del', del_tag, '>not_strong')

    ins_tag = SimpleTagPattern(INS_RE, 'ins')
    md.inlinePatterns.add('ins', ins_tag, '>del')

    strong_tag = SimpleTagPattern(STRONG_RE, 'strong')
    md.inlinePatterns['strong'] = strong_tag

    emph_tag = SimpleTagPattern(EMPH_RE, 'em')
    md.inlinePatterns.add('em', emph_tag, '>del')

    # code_tag = SimpleTagPattern(CODE_RE, 'code')
    # md.inlinePatterns['backtick'] = code_tag

    newline_tag = SubstituteTagPattern(NEWLINE_RE, 'br')
    md.inlinePatterns.add('linebreak2', newline_tag, '>linebreak') 

    username_tag = SimpleTagPattern(USERNAME_RE, 'span')
    md.inlinePatterns.add('username', username_tag, '<link')
