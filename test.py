import unittest

import markdown

data_for_replacing_text = [{'data_id': 'UBG4243ME', 'text': 'John Doe'}]

channel_data_for_replacing_text = [{'data_id': 'CBHSFG3T9', 'text': 'Random Channel'}]


def convert_markdown(txt):
    # return markdown.markdown(txt, extensions=[PythonMarkdownSlack()])
    return markdown.markdown(txt, extensions=['python_markdown_slack:PythonMarkdownSlack'])


def convert_markdown_with_options(txt, opts):
    # return markdown.markdown(txt, extensions=[PythonMarkdownSlack(opts)])
    return markdown.markdown(txt, extensions=['python_markdown_slack:PythonMarkdownSlack'],
                             extension_configs={'python_markdown_slack:PythonMarkdownSlack': opts})


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_strike(self):
        self.assertEqual(convert_markdown('~strike~'), '<p><del>strike</del></p>')
        self.assertEqual(convert_markdown('this is ~strike~. More text'), '<p>this is <del>strike</del>. More text</p>')
        self.assertEqual(convert_markdown('this is ~strike~a'), '<p>this is ~strike~a</p>')

    def test_bold(self):
        self.assertEqual(convert_markdown('*bold*'), '<p><strong>bold</strong></p>')
        self.assertEqual(convert_markdown('this is *bold*.'), '<p>this is <strong>bold</strong>.</p>')
        self.assertEqual(convert_markdown('*bold Title*foo'), '<p>*bold Title*foo</p>')

    def test_italics(self):
        self.assertEqual(convert_markdown('_italics_'), '<p><em>italics</em></p>')
        self.assertEqual(convert_markdown('this is _italics_.'), '<p>this is <em>italics</em>.</p>')
        self.assertEqual(convert_markdown('this is a_italics_.'), '<p>this is a_italics_.</p>')

        self.assertEqual(convert_markdown(
            'check this out: https://ridebeeline.typeform.com/to/eICKcM?utm_source=Beeline+Newsletter&utm_campaign=f6ee3aa2be-EMAIL_CAMPAIGN_2018_09_14_09_05&utm_medium=email&utm_term=0_57a8b92407-f6ee3aa2be-195694777&mc_cid=f6ee3aa2be&mc_eid=442e296d50'),
            '<p>check this out: https://ridebeeline.typeform.com/to/eICKcM?utm_source=Beeline+Newsletter&amp;utm_campaign=f6ee3aa2be-EMAIL_CAMPAIGN_2018_09_14_09_05&amp;utm_medium=email&amp;utm_term=0_57a8b92407-f6ee3aa2be-195694777&amp;mc_cid=f6ee3aa2be&amp;mc_eid=442e296d50</p>'
        )

    def test_code(self):
        self.assertEqual(convert_markdown('`code`'), '<p><code>code</code></p>')

    def test_links(self):
        self.assertEqual(convert_markdown('<https://github.com/wingleungchoi/python-markdown-slack>'),
                         '<p><a href="https://github.com/wingleungchoi/python-markdown-slack">https://github.com/wingleungchoi/python-markdown-slack</a></p>')
        self.assertEqual(convert_markdown('the link: <https://github.com/wingleungchoi/python-markdown-slack>'),
                         '<p>the link: <a href="https://github.com/wingleungchoi/python-markdown-slack">https://github.com/wingleungchoi/python-markdown-slack</a></p>')
        self.assertEqual(convert_markdown(
            'the link: <https://github.com/wingleungchoi/python-markdown-slack?foo=bar&foo2=bar2|Python Markdown Slack>'),
            '<p>the link: <a href="https://github.com/wingleungchoi/python-markdown-slack?foo=bar&amp;foo2=bar2">Python Markdown Slack</a></p>')
        # TODO is the link to image need to have image tag? if yes, how to? by options?
        self.assertEqual(convert_markdown(
            'the link: <https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-02-15/316074573012_6e20e900d2366268a877_512.png>'),
            '<p>the link: <a href="https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-02-15/316074573012_6e20e900d2366268a877_512.png">https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2018-02-15/316074573012_6e20e900d2366268a877_512.png</a></p>')

    def test_combinations(self):
        self.assertEqual(convert_markdown("*_bold italics_*"), '<p><strong><em>bold italics</em></strong></p>')
        self.assertEqual(convert_markdown("_*bold italics*_"), '<p><em><strong>bold italics</strong></em></p>')
        self.assertEqual(convert_markdown('~*_bold italics strikeout_*~'),
                         '<p><del><strong><em>bold italics strikeout</em></strong></del></p>')
        self.assertEqual(convert_markdown('_*~bold italics strikeout~*_'),
                         '<p><em><strong><del>bold italics strikeout</del></strong></em></p>')

    def test_username(self):
        self.assertEqual(convert_markdown(' <@UBG4243ME>'), '<p><span class="username">UBG4243ME</span></p>')
        self.assertEqual(convert_markdown('Hi <@UBG4243ME> how is the project?'),
                         '<p>Hi <span class="username">UBG4243ME</span> how is the project?</p>')
        self.assertEqual(convert_markdown('Hi <@UBG4243ME|Charlie> how is the project?'),
                         '<p>Hi <span class="username">Charlie</span> how is the project?</p>')
        # TODO fix the following case as there '<@' is in the start of string
        # it might be related to https://github.com/Python-Markdown/markdown/blob/2.6/markdown/__init__.py#L383
        # self.assertEqual(convert_markdown('<@UBG4243ME>'), '<p><span class="username">UBG4243ME</span></p>')

    def test_username_with_options(self):
        self.assertEqual(
            convert_markdown_with_options(' <@UBG4243ME>', {'data_for_replacing_text': data_for_replacing_text}),
            '<p><span class="username">John Doe</span></p>')
        self.assertEqual(convert_markdown_with_options(' <@UBG4243ME>: hello world',
                                                       {'data_for_replacing_text': data_for_replacing_text}),
                         '<p><span class="username">John Doe</span>: hello world</p>')
        # Warning in Markdonw of version 2.6 is not relevant. https://github.com/Python-Markdown/markdown/blob/2.6/markdown/extensions/__init__.py#L31
        self.assertEqual(convert_markdown_with_options('Hi <@UBG4243ME|Charlie> how is the project?',
                                                       {'data_for_replacing_text': data_for_replacing_text}),
                         '<p>Hi <span class="username">Charlie</span> how is the project?</p>')
        # TODO fix the following case as there '<@' is in the start of string
        # self.assertEqual(convert_markdown_with_options('<@UBG4243ME>', {'data_for_replacing_text': data_for_replacing_text}), '<p><span class="username">John Doe</span></p>')
        # self.assertEqual(convert_markdown_with_options('<@UBG4243ME>: hello world', {'data_for_replacing_text': data_for_replacing_text}), '<p><span class="username">John Doe</span>: hello world</p>')

    def test_channel(self):
        self.assertEqual(convert_markdown('<#CBHSFG3T9|general>'), '<p><span class="channel">general</span></p>')
        self.assertEqual(convert_markdown('<#ChannelSlackId>'), '<p><span class="channel">ChannelSlackId</span></p>')
        self.assertEqual(convert_markdown('channel: I refer to channel <#CBHSFG3T9|general>'),
                         '<p>channel: I refer to channel <span class="channel">general</span></p>')
        # case: no channel name is returned.
        self.assertEqual(convert_markdown('channel: I refer to channel <#CBHSFG3T9>'),
                         '<p>channel: I refer to channel <span class="channel">CBHSFG3T9</span></p>')

    def test_channel(self):
        # as channel_name i.e. genenral will be used CHANNEL_RE case, therefore return channel_name instead of data of in channel_data_for_replacing_text i.e. Random Channel
        self.assertEqual(convert_markdown_with_options('<#CBHSFG3T9|general>',
                                                       {'data_for_replacing_text': channel_data_for_replacing_text}),
                         '<p><span class="channel">general</span></p>')
        self.assertEqual(convert_markdown_with_options('<#ChannelSlackId>',
                                                       {'data_for_replacing_text': channel_data_for_replacing_text}),
                         '<p><span class="channel">ChannelSlackId</span></p>')
        self.assertEqual(convert_markdown_with_options('channel: I refer to channel <#CBHSFG3T9|general>',
                                                       {'data_for_replacing_text': channel_data_for_replacing_text}),
                         '<p>channel: I refer to channel <span class="channel">general</span></p>')
        # case: no channel name is returned.
        self.assertEqual(convert_markdown_with_options('channel: I refer to channel <#CBHSFG3T9>',
                                                       {'data_for_replacing_text': channel_data_for_replacing_text}),
                         '<p>channel: I refer to channel <span class="channel">Random Channel</span></p>')

    def test_preformatted(self):
        # TODO unexpected behaviour, \n shall not exist after convert
        self.assertEqual(convert_markdown('```preformatted```'), '<p>\n<pre>preformatted</pre>\n</p>')
        self.assertEqual(convert_markdown('```\npreformatted\n```'), '<p>\n<pre>\npreformatted\n</pre>\n</p>')
        self.assertEqual(convert_markdown('preformatted: ```\npreformatted\n```'),
                         '<p>preformatted: <pre>\npreformatted\n</pre>\n</p>')

        # def test_quote(self):
        #   self.assertEqual(convert_markdown('quote'), '')

    def test_start_bracket_tag(self):
        self.assertEqual(convert_markdown('Hello <Route>'), '<p>Hello <span>&lt;Route&gt;</span></p>')

    def test_close_bracket_tag(self):
        self.assertEqual(convert_markdown('Hello <Link/>'), '<p>Hello <span>&lt;Link/&gt;</span></p>')
        self.assertEqual(convert_markdown('<Link/> Hello'), '<p><span>&lt;Link/&gt;</span> Hello</p>')

    def test_ping_here(self):
        self.assertEqual(convert_markdown(' <!here>'), '<p><span class="here">@here</span></p>')
        self.assertEqual(convert_markdown('Hello <!here>'), '<p>Hello <span class="here">@here</span></p>')
        self.assertEqual(convert_markdown(' <!here> Hello!'), '<p><span class="here">@here</span> Hello!</p>')

    def test_ping_channel(self):
        self.assertEqual(convert_markdown('Hello <!channel>'), '<p>Hello <span class="channel">@channel</span></p>')
        self.assertEqual(convert_markdown(' <!channel> Hello'), '<p><span class="channel">@channel</span> Hello</p>')

    def test_ping_user_group(self):
        self.assertEqual(convert_markdown('Hello <!subteam^SHCNKB1EU|@engineering>'),
                         '<p>Hello <span class="user_group">@engineering</span></p>')
        self.assertEqual(convert_markdown(' <!subteam^SHCNKB1EU|@engineering> Hello'),
                         '<p><span class="user_group">@engineering</span> Hello</p>')


class TestListMethods(unittest.TestCase):

    def test_ordered_list(self):
        self.assertEqual(convert_markdown('1. item 1\n2. item 2\n3. item 3'),
                         '<ol>\n<li>item 1</li>\n<li>item 2</li>\n<li>item 3</li>\n</ol>')

    def test_ordered_list_right_after_the_line(self):
        self.assertEqual(convert_markdown('Hello\nWorld\n1. item 1\n2. item 2\n3. item 3\nTesting'),
                         '<p>Hello\nWorld</p>\n<ol>\n<li>item 1</li>\n<li>item 2</li>\n<li>item 3\nTesting</li>\n</ol>')

    def test_multiple_ordered_list_with_numbers(self):
        self.assertEqual(convert_markdown('Part 1 - testing\n1. item 1\n2. item 2\n3. item 3\nTesting'),
                         '<p>Part 1 - testing</p>\n<ol>\n<li>item 1</li>\n<li>item 2</li>\n<li>item 3\nTesting</li>\n</ol>')

    def test_multiple_ordered_list_right_after_the_line(self):
        self.assertEqual(convert_markdown(
            'Hello World\n1. item 1\n2. item 2\n3. item 3\n\nTesting\n1. item a\n2. item b\n3. item c\n- unknown item'),
                         '<p>Hello World</p>\n<ol>\n<li>item 1</li>\n<li>item 2</li>\n<li>item 3</li>\n</ol>\n<p>Testing</p>\n<ol>\n<li>item a</li>\n<li>item b</li>\n<li>item c</li>\n<li>unknown item</li>\n</ol>')

    def test_multiple_ordered_list_with_empty_lines_right_after_the_line(self):
        self.assertEqual(convert_markdown(
            'Hello World\n1. item 1\n2. item 2\n3. item 3\n\n1. item a\n2. item b\n3. item c\n- unknown item'),
                         '<p>Hello World</p>\n<ol>\n<li>item 1</li>\n<li>item 2</li>\n<li>item 3</li>\n</ol>\n<ol>\n<li>item a</li>\n<li>item b</li>\n<li>item c</li>\n<li>unknown item</li>\n</ol>')

    def test_ordered_list_in_different_blocks(self):
        self.assertEqual(convert_markdown('Hello\nWorld\n\n1. item 1\n2. item 2\n3. item 3\nTesting'),
                         '<p>Hello\nWorld</p>\n<ol>\n<li>item 1</li>\n<li>item 2</li>\n<li>item 3\nTesting</li>\n</ol>')

    def test_unordered_list_right_after_the_line(self):
        self.assertEqual(convert_markdown('Hello\nWorld\n- item 1\n- item 2\n- item 3\nhello'),
                         '<p>Hello\nWorld</p>\n<ul>\n<li>item 1</li>\n<li>item 2</li>\n<li>item 3\nhello</li>\n</ul>')

    def test_unordered_list_in_different_blocks(self):
        self.assertEqual(convert_markdown('Hello\nWorld\n\n- item 1\n- item 2\n- item 3\nhello'),
                         '<p>Hello\nWorld</p>\n<ul>\n<li>item 1</li>\n<li>item 2</li>\n<li>item 3\nhello</li>\n</ul>')

    def test_unordered_list(self):
        self.assertEqual(convert_markdown('- item 1\n- item 2\n- item 3'),
                         '<ul>\n<li>item 1</li>\n<li>item 2</li>\n<li>item 3</li>\n</ul>')
        self.assertEqual(convert_markdown('• item 1\n• item 2\n• item 3'),
                         '<ul>\n<li>item 1</li>\n<li>item 2</li>\n<li>item 3</li>\n</ul>')

    def test_nested_unordered_list(self):
        #todo should be nested <ul> instead
        self.assertEqual(convert_markdown('- item 1\n   - item 1.1\n- item 2'),
                         '<ul>\n<li>item 1</li>\n<li>item 1.1</li>\n<li>item 2</li>\n</ul>')

    def test_mixed_list(self):
        self.assertEquals(convert_markdown(
            '- Number of integrations (Guru, Slab)\n 1. Embed (youtube, vimeo, etc.'),
                          '<ol>\n<li>Number of integrations (Guru, Slab)</li>\n<li>Embed (youtube, vimeo, etc.</li>\n</ol>')


if __name__ == '__main__':
    unittest.main()
