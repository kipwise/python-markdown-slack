# -*- coding: utf-8 -*-
import re
from markdown import util
from markdown.blockprocessors import BlockProcessor


class OListProcessor(BlockProcessor):
    """ Process ordered list blocks. """

    TAG = 'ol'
    # The integer (python string) with which the lists starts (default=1)
    # Eg: If list is intialized as)
    #   3. Item
    # The ol tag will get starts="3" attribute
    STARTSWITH = '1'
    # List of allowed sibling tags.
    SIBLING_TAGS = ['ol', 'ul']

    def __init__(self, parser):
        super(OListProcessor, self).__init__(parser)
        # Detect an item (``1. item``). ``group(1)`` contains contents of item.
        self.RE = re.compile(r'^.*?[\n\r]{1,2}[ ]{0,%d}\d+\.[ ]+(.*)' % (self.tab_length - 1), re.MULTILINE | re.DOTALL)
        # Detect items on secondary lines. they can be of either list type.
        self.CHILD_RE = re.compile(r'^[ ]{0,%d}((\d+\.)|[*+-])[ ]+(.*)' %
                                   (self.tab_length - 1))
        # Detect indented (nested) items of either type
        self.INDENT_RE = re.compile(r'^[ ]{%d,%d}((\d+\.)|[*+-])[ ]+.*' %
                                    (self.tab_length, self.tab_length * 2 - 1))

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        # Check fr multiple items in one block.
        prevTextLines, items = self.get_items(blocks.pop(0))

        if parent.tag in ['ol', 'ul']:
            # this catches the edge case of a multi-item indented list whose
            # first item is in a blank parent-list item:
            # * * subitem1
            #     * subitem2
            # see also ListIndentProcessor
            lst = parent
        else:
            # This is a new list so create parent with appropriate tag.

            if len(prevTextLines) > 0:
                textnode = util.etree.SubElement(parent, 'p')
                textnode.text = "\n".join(prevTextLines)

            lst = util.etree.SubElement(parent, self.TAG)
            # Check if a custom start integer is set
            if not self.parser.markdown.lazy_ol and self.STARTSWITH != '1':
                lst.attrib['start'] = self.STARTSWITH

        self.parser.state.set('list')
        # Loop through items in block, recursively parsing each with the
        # appropriate parent.
        for item in items:
            if item.startswith(' '*self.tab_length):
                # Item is indented. Parse with last item as parent
                self.parser.parseBlocks(lst[-1], [item])
            else:
                # New item. Create li and parse with it as parent
                li = util.etree.SubElement(lst, 'li')
                self.parser.parseBlocks(li, [item])
        self.parser.state.reset()

    def get_items(self, block):
        """ Break a block into list items. """
        items = []
        prevTextLines = []
        for line in block.split('\n'):
            m = self.CHILD_RE.match(line)
            if self.INDENT_RE.match(line):
                # This is an indented (possibly nested) item.
                if items[-1].startswith(' ' * self.tab_length):
                    # Previous item was indented. Append to that item.
                    items[-1] = '%s\n%s' % (items[-1], line)
                else:
                    items.append(line)
            elif m:
                # This is a new list item
                # Check first item for the start index
                if not items and self.TAG == 'ol':
                    # Detect the integer value of first list item
                    INTEGER_RE = re.compile('(\d+)')
                    match = INTEGER_RE.match(m.group(1))
                    if match:
                        self.STARTSWITH = match.group()
                    else:
                        BULLET_RE = re.compile('([•*+-])')
                        self.STARTSWITH = BULLET_RE.match(m.group(1)).group()
                # Append to the list
                items.append(m.group(3))
            else:
                # This is non list items
                if len(items) > 0:
                    items[-1] = '%s\n%s' % (items[-1], line)
                # This is another line of previous item. Append to that item.
                else:
                    prevTextLines.append(line)
        return prevTextLines, items


class UListProcessor(OListProcessor):
    """ Process unordered list blocks. """

    TAG = 'ul'

    def __init__(self, parser):
        super(UListProcessor, self).__init__(parser)
        # Detect an item (``1. item``). ``group(1)`` contains contents of item.
        self.RE = re.compile(r'^.*?[\n\r]{0,2}[ ]{0,%d}[•*+-][ ]+(.*)' % (self.tab_length - 0), re.MULTILINE | re.DOTALL)
        self.CHILD_RE = re.compile(r'^[ ]{0,%d}((\d+\.)|[•*+-])[ ]+(.*)' %
                                   (self.tab_length - 1))
        # Detect indented (nested) items of either type
        self.INDENT_RE = re.compile(r'^[ ]{%d,%d}((\d+\.)|[•*+-])[ ]+.*' %
                                    (self.tab_length, self.tab_length * 2 - 1))