from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
from sentence.lexer import SentenceLexer
from sentence.style import SentenceStyle
 
# read input file
with open("./../test/input.sentence", "r", encoding="utf-8") as f:
    code = f.read()

lexer = SentenceLexer()

formatter = HtmlFormatter(
    full=True,        # corresponds to -O full
    style=SentenceStyle,
    verbose=True      # corresponds to -v
)

#for t in lexer.get_tokens_unprocessed(code):
    #print(t)

result = highlight(code, lexer, formatter)

file_path = "output.html"
with open(file_path, 'w') as f:
    f.write(result)
