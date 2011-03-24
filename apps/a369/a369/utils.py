from haystack.utils import Highlighter
import re

        
class BorkHighlighter(Highlighter):
    def render_html(self, highlight_locations=None, start_offset=None, end_offset=None):
        # Start by chopping the block down to the proper window.
        #highlighted_chunk = self.text_block[start_offset:end_offset]
        highlighted_chunk = self.text_block
        
        for word in self.query_words:
            for special_char in ('+', '*', '.', '?'):
                word = word.replace(special_char, '\%s' % special_char)
            
            word_re = re.compile("(%s)" % word, re.I)
            
            if self.css_class:
                highlighted_chunk = re.sub(word_re, r'<%s class="%s">\1</%s>' % (self.html_tag, self.css_class, self.html_tag), highlighted_chunk)
            else:
                highlighted_chunk = re.sub(word_re, r'<%s>\1</%s>' % (self.html_tag, self.html_tag), highlighted_chunk)
        
        #if start_offset > 0:
        #    highlighted_chunk = '...%s' % highlighted_chunk
        
        #if end_offset < len(self.text_block):
        #    highlighted_chunk = '%s...' % highlighted_chunk
        
        return highlighted_chunk