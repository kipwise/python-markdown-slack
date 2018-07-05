import unittest
import markdown
from python_markdown_slack import PythonMarkdownSlack

data_for_replacing_text = [{'data_id': 'UBG4243ME', 'text': 'John Doe'}]

channel_data_for_replacing_text = [{'data_id': 'CBHSFG3T9', 'text': 'Random Channel'}]

def convert_markdown(txt):
  return markdown.markdown(txt, extensions=[PythonMarkdownSlack()])

def convert_markdown_with_options(txt, opts):
  return markdown.markdown(txt, extensions=[PythonMarkdownSlack(opts)])

class TestStringMethods(unittest.TestCase):

  def test_strike(self):
    self.assertEqual(convert_markdown('~strike~'), '<p><del>strike</del></p>')
    self.assertEqual(convert_markdown('this is ~strike~.'), '<p>this is <del>strike</del>.</p>')

  def test_bold(self):
    self.assertEqual(convert_markdown('*bold*'), '<p><strong>bold</strong></p>')
    self.assertEqual(convert_markdown('*bold Title*foo'), '<p><strong>bold Title</strong>foo</p>')

  def test_italics(self):
    self.assertEqual(convert_markdown('_italics_'), '<p><em>italics</em></p>')

  def test_code(self):
    self.assertEqual(convert_markdown('`code`'), '<p><code>code</code></p>')

  def test_newline(self):
    self.assertEqual(convert_markdown('somes before newline\n some after newline'), '<p>somes before newline\n some after newline</p>')
    self.assertEqual(convert_markdown('somes before newline \n some after newline'), '<p>somes before newline \n some after newline</p>')
    self.assertEqual(convert_markdown('somes before newline  \n some after newline'), '<p>somes before newline<br />\n some after newline</p>')
    self.assertEqual(convert_markdown('somes before newline   \n some after newline'), '<p>somes before newline <br />\n some after newline</p>')

  def test_links(self):
    self.assertEqual(convert_markdown('<https://github.com/wingleungchoi/python-markdown-slack>'), '<p><a href="https://github.com/wingleungchoi/python-markdown-slack">https://github.com/wingleungchoi/python-markdown-slack</a></p>')
    self.assertEqual(convert_markdown('the link: <https://github.com/wingleungchoi/python-markdown-slack>'), '<p>the link: <a href="https://github.com/wingleungchoi/python-markdown-slack">https://github.com/wingleungchoi/python-markdown-slack</a></p>')
    self.assertEqual(convert_markdown('the link: <https://github.com/wingleungchoi/python-markdown-slack|Python Markdown Slack>'), '<p>the link: <a href="https://github.com/wingleungchoi/python-markdown-slack">Python Markdown Slack</a></p>')
    # TODO is the link to image need to have image tag? if yes, how to? by options?
    self.assertEqual(convert_markdown('the link: <https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-02-15/316074573012_6e20e900d2366268a877_512.png>'), '<p>the link: <a href="https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-02-15/316074573012_6e20e900d2366268a877_512.png">https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-02-15/316074573012_6e20e900d2366268a877_512.png</a></p>')

  def test_combinations(self):
    self.assertEqual(convert_markdown("*_bold italics_*"), '<p><strong><em>bold italics</em></strong></p>')
    self.assertEqual(convert_markdown("_*bold italics*_"), '<p><em><strong>bold italics</strong></em></p>')
    self.assertEqual(convert_markdown('~*_bold italics strikeout_*~'), '<p><del><strong><em>bold italics strikeout</em></strong></del></p>')
    self.assertEqual(convert_markdown('_*~bold italics strikeout~*_'), '<p><em><strong><del>bold italics strikeout</del></strong></em></p>')

  def test_username(self):
    self.assertEqual(convert_markdown(' <@UBG4243ME>'), '<p><span class="username">UBG4243ME</span></p>')
    self.assertEqual(convert_markdown('Hi <@UBG4243ME> how is the project?'), '<p>Hi <span class="username">UBG4243ME</span> how is the project?</p>')
    # TODO fix the following case as there '<@' is in the start of string
    # it might be related to https://github.com/Python-Markdown/markdown/blob/2.6/markdown/__init__.py#L383
    # self.assertEqual(convert_markdown('<@UBG4243ME>'), '<p><span class="username">UBG4243ME</span></p>')

  def test_username_with_options(self):
    self.assertEqual(convert_markdown_with_options(' <@UBG4243ME>', {'data_for_replacing_text': data_for_replacing_text}), '<p><span class="username">John Doe</span></p>')
    self.assertEqual(convert_markdown_with_options(' <@UBG4243ME>: hello world', {'data_for_replacing_text': data_for_replacing_text}), '<p><span class="username">John Doe</span>: hello world</p>')
    # Warning in Markdonw of version 2.6 is not relevant. https://github.com/Python-Markdown/markdown/blob/2.6/markdown/extensions/__init__.py#L31
    self.assertEqual(convert_markdown_with_options('Hi <@UBG4243ME> how is the project?', {'data_for_replacing_text': data_for_replacing_text}), '<p>Hi <span class="username">John Doe</span> how is the project?</p>')
    # TODO fix the following case as there '<@' is in the start of string
    # self.assertEqual(convert_markdown_with_options('<@UBG4243ME>', {'data_for_replacing_text': data_for_replacing_text}), '<p><span class="username">John Doe</span></p>')
    # self.assertEqual(convert_markdown_with_options('<@UBG4243ME>: hello world', {'data_for_replacing_text': data_for_replacing_text}), '<p><span class="username">John Doe</span>: hello world</p>')

  def test_channel(self):
    self.assertEqual(convert_markdown('<#CBHSFG3T9|general>'), '<p><span class="channel">general</span></p>')
    self.assertEqual(convert_markdown('<#ChannelSlackId>'), '<p><span class="channel">ChannelSlackId</span></p>')
    self.assertEqual(convert_markdown('channel: I refer to channel <#CBHSFG3T9|general>'), '<p>channel: I refer to channel <span class="channel">general</span></p>')
    # case: no channel name is returned.
    self.assertEqual(convert_markdown('channel: I refer to channel <#CBHSFG3T9>'), '<p>channel: I refer to channel <span class="channel">CBHSFG3T9</span></p>')

  def test_channel(self):
    # as channel_name i.e. genenral will be used CHANNEL_RE case, therefore return channel_name instead of data of in channel_data_for_replacing_text i.e. Random Channel
    self.assertEqual(convert_markdown_with_options('<#CBHSFG3T9|general>', {'data_for_replacing_text': channel_data_for_replacing_text}), '<p><span class="channel">general</span></p>')
    self.assertEqual(convert_markdown_with_options('<#ChannelSlackId>', {'data_for_replacing_text': channel_data_for_replacing_text}), '<p><span class="channel">ChannelSlackId</span></p>')
    self.assertEqual(convert_markdown_with_options('channel: I refer to channel <#CBHSFG3T9|general>', {'data_for_replacing_text': channel_data_for_replacing_text}), '<p>channel: I refer to channel <span class="channel">general</span></p>')
    # case: no channel name is returned.
    self.assertEqual(convert_markdown_with_options('channel: I refer to channel <#CBHSFG3T9>', {'data_for_replacing_text': channel_data_for_replacing_text}), '<p>channel: I refer to channel <span class="channel">Random Channel</span></p>')

  def test_preformatted(self):
    # TODO unexpected behaviour, \n shall not exist after convert
    self.assertEqual(convert_markdown('```preformatted```'), '<p>\n<pre>preformatted</pre>\n</p>')
    self.assertEqual(convert_markdown('```\npreformatted\n```'), '<p>\n<pre>\npreformatted\n</pre>\n</p>')
    self.assertEqual(convert_markdown('preformatted: ```\npreformatted\n```'), '<p>preformatted: <pre>\npreformatted\n</pre>\n</p>')
  
  # def test_quote(self):
  #   self.assertEqual(convert_markdown('quote'), '')

if __name__ == '__main__':
    unittest.main()