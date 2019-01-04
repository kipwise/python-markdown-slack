# existing markdown inlinePatterns
# https://github.com/Python-Markdown/markdown/blob/2.6/markdown/inlinepatterns.py
import re

from markdown.extensions import Extension
from markdown.inlinepatterns import AutolinkPattern, SimpleTagPattern, Pattern
from markdown.util import etree
from markdown.blockprocessors import OListProcessor
from markdown import util
from markdown.blockparser import BlockParser

DEL_RE = r'(~)(.*?)~' # Strikeout in slack
INS_RE = r'(__)(.*?)__' # not slack ;-)
STRONG_RE = r'(\*)(.*?)\*' # Bold in slack
EMPH_RE = r'(_)(.*?)_' # Italics in slack
CODE_RE = r'(`)(.*?)`' # code in slack
PREFORMATTED_RE = r'(```)(.*?)```' # preformatted in slack
# NEWLINE_RE = r'\n' # newline in slack
USERNAME_RE = r'(<@)(.*?)>' # username tag
CHANNEL_RE = r'(<#.+?\|)(.*?)>' # username tag
CHANNEL_2_RE = r'(<#)(.*?)>' # username tag
# <http://www.123.com|123>
AUTOLINK_WITH_NAME_RE = r'<((?:[Ff]|[Hh][Tt])[Tt][Pp][Ss]?://[^>]*)\|(.*?)>'
NON_MARKUP_TAGS_RE = r'(<)([0-9a-zA-Z-_\/ ]+)>'


class UListProcessor(OListProcessor):
    """ Process unordered list blocks. """

    TAG = 'ul'

    def __init__(self, parser):
        super(UListProcessor, self).__init__(parser)
        # Detect an item (``1. item``). ``group(1)`` contains contents of item.
        self.RE = re.compile(r'^[ ]{0,%d}[•*+-][ ]+(.*)' % (self.tab_length - 0))
        self.CHILD_RE = re.compile(r'^[ ]{0,%d}((\d+\.)|[•*+-])[ ]+(.*)' %
                                   (self.tab_length - 1))
        # Detect indented (nested) items of either type
        self.INDENT_RE = re.compile(r'^[ ]{%d,%d}((\d+\.)|[•*+-])[ ]+.*' %
                                    (self.tab_length, self.tab_length * 2 - 1))


class SlackInlineTagPattern(SimpleTagPattern):
  def __init__(self, pattern, tag):
    super().__init__(pattern, tag)
    self.compiled_re = re.compile("^(.*?(?:[^a-z0-9]|^))%s((?:[^a-z0-9]|$).*)$" % pattern,
                                      re.DOTALL | re.UNICODE)

class PythonMarkdownSlack(Extension):
  def __init__(self, *args, **kwargs):
    # Define config options and defaults
    self.config = {
      'data_for_replacing_text': ['it shall be a list', 'To provide data_for_replacing_text data']
    }
    # Call the parent class's __init__ method to configure options
    super(PythonMarkdownSlack, self).__init__(*args, **kwargs)

  def extendMarkdown(self, md, md_globals):
    data_for_replacing_text = self.getConfig('data_for_replacing_text')

    autolink_with_name_tag = AutolinkWihtNamePattern(AUTOLINK_WITH_NAME_RE, md)
    md.inlinePatterns.add('autolink_2', autolink_with_name_tag, '<autolink')

    # escape_brackets = NonMarkupTagsPattern(NON_MARKUP_TAGS_RE, md)
    # md.inlinePatterns.add('escape_brackets', escape_brackets, '>escape')

    del_tag = SlackInlineTagPattern(DEL_RE, 'del')
    md.inlinePatterns.add('del', del_tag, '>not_strong')

    ins_tag = SimpleTagPattern(INS_RE, 'ins')
    md.inlinePatterns.add('ins', ins_tag, '>del')

    strong_tag = SlackInlineTagPattern(STRONG_RE, 'strong')
    md.inlinePatterns['strong'] = strong_tag

    emph_tag = SlackInlineTagPattern(EMPH_RE, 'em')
    md.inlinePatterns['emphasis'] = emph_tag

    preformatted_tag = SimpleTagPattern(PREFORMATTED_RE, 'pre')
    md.inlinePatterns.add('preformatted', preformatted_tag, '<backtick')

    md.parser.blockprocessors['ulist'] = UListProcessor(md.parser)

    if isinstance(data_for_replacing_text, list):
      username_tag = SimpleTagPatternWithClassOptionsAndData(USERNAME_RE, 'span', 'username', data_for_replacing_text)
      md.inlinePatterns.add('username', username_tag, '<link')
      channel_tag = SimpleTagPatternWithClassOptionsAndData(CHANNEL_RE, 'span', 'channel', data_for_replacing_text)
      md.inlinePatterns.add('channel', channel_tag, '<username')
      channel_2_tag = SimpleTagPatternWithClassOptionsAndData(CHANNEL_2_RE, 'span', 'channel', data_for_replacing_text)
      md.inlinePatterns.add('channel_2', channel_2_tag, '>channel')
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

class SimpleTagPatternWithClassOptionsAndData(Pattern):
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
        datum_for_replacing_text_name = self.get_datum_text(self.data_for_replacing_text, data_id)
        el.text = datum_for_replacing_text_name
        el.set('class', self.class_name_in_html)
        return el

    def get_datum_text(self, data_for_replacing_text, data_id):
      datum_for_replacing_text_name = data_id
      for datum_for_replacing_text in data_for_replacing_text:
        if datum_for_replacing_text.get('data_id') == data_id:
          datum_for_replacing_text_name = datum_for_replacing_text.get('text')
          break
      return datum_for_replacing_text_name


class AutolinkWihtNamePattern(AutolinkPattern):
    """ Return a link Element given an autolink (`<http://example/com|Please click>`). """
    def handleMatch(self, m):
        el = super(AutolinkWihtNamePattern, self).handleMatch(m)
        el.text = util.AtomicString(m.group(3))
        return el


class NonMarkupTagsPattern(Pattern):
    """ Return an element to html entites (`<Route> <Link/>`). """

    def __init__(self, pattern, md=None):
        """
        Create an instant of an inline pattern.

        Keyword arguments:

        * pattern: A regular expression that matches a pattern

        """
        self.pattern = pattern
        self.compiled_re = re.compile(pattern, re.DOTALL | re.UNICODE)

        # Api for Markdown to pass safe_mode into instance
        self.safe_mode = False
        self.md = md

    def handleMatch(self, m, data):
        rawhtml = self.unescape(m.group(1))
        place_holder = self.md.htmlStash.store(rawhtml)
        return place_holder, m.start(0), m.end(0)

    def unescape(self, text):
        return text
        """ Return unescaped text given text with an inline placeholder. """
        try:
            stash = self.md.treeprocessors['inline'].stashed_nodes
        except KeyError:  # pragma: no cover
            return text

        def get_stash(m):
            id = m.group(1)
            value = stash.get(id)
            if value is not None:
                try:
                    return self.md.serializer(value)
                except Exception:
                    return r'\%s' % value

        return util.INLINE_PLACEHOLDER_RE.sub(get_stash, text)