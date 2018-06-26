from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern

DEL_RE = r'(~)(.*?)~' # Strikeout in slack
INS_RE = r'(__)(.*?)__' # not slack ;-)
STRONG_RE = r'(\*)(.*?)\*' # Bold in slack
EMPH_RE = r'(_)(.*?)_' # Italics in slack
CODE_RE = r'(`)(.*?)`' # code in slack

class MyExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        del_tag = SimpleTagPattern(DEL_RE, 'del')
        md.inlinePatterns.add('del', del_tag, '>not_strong')

        ins_tag = SimpleTagPattern(INS_RE, 'ins')
        md.inlinePatterns.add('ins', ins_tag, '>del')

        strong_tag = SimpleTagPattern(STRONG_RE, 'strong')
        md.inlinePatterns['strong'] = strong_tag

        emph_tag = SimpleTagPattern(EMPH_RE, 'em')
        md.inlinePatterns['em'] = emph_tag

        code_tag = SimpleTagPattern(CODE_RE, 'code')
        md.inlinePatterns['code'] = code_tag

        del md.inlinePatterns['strong_em']
        del md.inlinePatterns['em_strong']
        del md.inlinePatterns['emphasis2']