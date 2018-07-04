# existing markdown inlinePatterns
# https://github.com/Python-Markdown/markdown/blob/2.6/markdown/inlinepatterns.py

from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern, Pattern
from markdown.inlinepatterns import SubstituteTagPattern
from markdown.util import etree
from markdown import util

DEL_RE = r'(~)(.*?)~' # Strikeout in slack
INS_RE = r'(__)(.*?)__' # not slack ;-)
STRONG_RE = r'(\*)(.*?)\*' # Bold in slack
EMPH_RE = r'(_)(.*?)_' # Italics in slack
CODE_RE = r'(`)(.*?)`' # code in slack
PREFORMATTED_RE = r'(```\n)(.*?)\n```' # preformatted in slack
NEWLINE_RE = r'\n' # newline in slack
USERNAME_RE = r'(<@)(.*?)>' # username tag
CHANNEL_RE = r'(<#.+?\|)(.*?)>' # username tag
CHANNEL_2_RE = r'(<#)(.*?)>' # username tag

class MyExtension(Extension):
  def __init__(self, *args, **kwargs):
    # Define config options and defaults
    self.config = {
      'data_for_replacing_text': ['it shall be a list', 'To provide data_for_replacing_text data']
    }
    # Call the parent class's __init__ method to configure options
    super(MyExtension, self).__init__(*args, **kwargs)

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

    preformatted_tag = SimpleTagPattern(PREFORMATTED_RE, 'pre')
    md.inlinePatterns.add('preformatted', preformatted_tag, '<backtick')

    newline_tag = SubstituteTagPattern(NEWLINE_RE, 'br')
    md.inlinePatterns.add('linebreak2', newline_tag, '>linebreak') 

    data_for_replacing_text = self.getConfig('data_for_replacing_text')
    if isinstance(data_for_replacing_text, list):
      username_tag = UsernameTagPatternWithClassOptions(USERNAME_RE, 'span', 'username', data_for_replacing_text)
      md.inlinePatterns.add('username', username_tag, '<link')
    else:
      username_tag = SimpleTagPatternWithClassOptions(USERNAME_RE, 'span', 'username')
      md.inlinePatterns.add('username', username_tag, '<link')

    channel_tag = SimpleTagPatternWithClassOptions(CHANNEL_RE, 'span', 'channel')
    md.inlinePatterns.add('channel', channel_tag, '<username')

    channel_2_tag = SimpleTagPatternWithClassOptions(CHANNEL_2_RE, 'span', 'channel')
    md.inlinePatterns.add('channel_2', channel_2_tag, '>channel')

class SimpleTagPatternWithClassOptions(Pattern):
    """
    Return element of type `tag` with a text attribute of group(3)
    of a Pattern.
    """
    def __init__(self, pattern, tag, class_name_in_html):
        Pattern.__init__(self, pattern)
        self.tag = tag
        self.class_name_in_html = class_name_in_html

    def handleMatch(self, m):
        el = util.etree.Element(self.tag)
        el.text = m.group(3)
        el.set('class', self.class_name_in_html)
        return el

class UsernameTagPatternWithClassOptions(Pattern):
    """
    Return element of type `tag` with input text
    of a Pattern.
    """
    def __init__(self, pattern, tag, class_name_in_html, data_for_replacing_text):
        Pattern.__init__(self, pattern)
        self.tag = tag
        self.class_name_in_html = class_name_in_html
        self.data_for_replacing_text = data_for_replacing_text

    def handleMatch(self, m):
        el = util.etree.Element(self.tag)
        data_id = m.group(3)
        user_name = self.get_user_name(self.data_for_replacing_text, data_id)
        el.text = user_name
        el.set('class', self.class_name_in_html)
        return el

    def get_user_name(self, data_for_replacing_text, data_id):
      user_name = data_id
      for datum_for_replacing_text in data_for_replacing_text:
        if datum_for_replacing_text.get('data_id') == data_id:
          datum_for_replacing_text_name = datum_for_replacing_text.get('text')
          break
      return datum_for_replacing_text_name
