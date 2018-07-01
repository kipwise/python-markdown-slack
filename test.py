import unittest
import markdown
from myextension import MyExtension

def convert_markdown(txt):
  return markdown.markdown(txt, extensions=[MyExtension()])

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
    self.assertEqual(convert_markdown('somes before newline\n some after newline'), '<p>somes before newline<br />\n some after newline</p>')
    self.assertEqual(convert_markdown('somes before newline \n some after newline'), '<p>somes before newline <br />\n some after newline</p>')
    self.assertEqual(convert_markdown('somes before newline  \n some after newline'), '<p>somes before newline<br />\n some after newline</p>')
    self.assertEqual(convert_markdown('somes before newline   \n some after newline'), '<p>somes before newline <br />\n some after newline</p>')

  def test_links(self):
    self.assertEqual(convert_markdown('<https://github.com/wingleungchoi/myextension>'), '<p><a href="https://github.com/wingleungchoi/myextension">https://github.com/wingleungchoi/myextension</a></p>')
    self.assertEqual(convert_markdown('the link: <https://github.com/wingleungchoi/myextension>'), '<p>the link: <a href="https://github.com/wingleungchoi/myextension">https://github.com/wingleungchoi/myextension</a></p>')
    # TODO is the link to image need to have image tag? if yes, how to? by options?
    self.assertEqual(convert_markdown('the link: <https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-02-15/316074573012_6e20e900d2366268a877_512.png>'), '<p>the link: <a href="https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-02-15/316074573012_6e20e900d2366268a877_512.png">https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-02-15/316074573012_6e20e900d2366268a877_512.png</a></p>')

  def test_combinations(self):
    self.assertEqual(convert_markdown("*_bold italics_*"), '<p><strong><em>bold italics</em></strong></p>')
    self.assertEqual(convert_markdown("_*bold italics*_"), '<p><em><strong>bold italics</strong></em></p>')
    self.assertEqual(convert_markdown('~*_bold italics strikeout_*~'), '<p><del><strong><em>bold italics strikeout</em></strong></del></p>')
    self.assertEqual(convert_markdown('_*~bold italics strikeout~*_'), '<p><em><strong><del>bold italics strikeout</del></strong></em></p>')

  def test_username(self):
    # TODO fix the following case as there '<@' is in the start of string
    # self.assertEqual(convert_markdown('<@UBG4243ME>'), '<p><span>UBG4243ME</span></p>')
    self.assertEqual(convert_markdown('Hi <@UBG4243ME> how is the project?'), '<p>Hi <span>UBG4243ME</span> how is the project?</p>')

  # def test_preformatted(self):
  #   self.assertEqual(convert_markdown('```preformatted```'), '<p><code class="is-pre">preformatted</code></p>')
  
  # def test_quote(self):
  #   self.assertEqual(convert_markdown('quote'), '')

if __name__ == '__main__':
    unittest.main()