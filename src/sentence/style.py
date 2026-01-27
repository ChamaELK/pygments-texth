from pygments.style import Style
from pygments.token import Token
class SentenceStyle(Style):
    name = "SentenceStyle"
    aliases = ["sstyle"]
    styles = {
        Token.Sentence.One  : "#000000",  # 
        Token.Sentence.Two  : "#aa6600",  # 
        Token.Sentence.Three: "#336699",
        Token.Sentence.Four: "#bb0066",

        Token.Sentence.NP     : "bold",
        Token.Sentence.NP.One     : "bold #000000",
        Token.Sentence.NP.Two    : "bold #aa6600",
        Token.Sentence.NP.Three   : "bold #336699",
        Token.Sentence.NP.Four   : "bold #bb0066",
        Token.Sentence.Percent        : "bold #008800",  # PERCENT
        Token.Sentence.Currency : "bold #FF0000",  # CURRENCY

        
    }

"""

                #bbbbbb
#888888
#cc0000
#fff0f0 #cc0000

#fff0f0 #dd2200
#fff0ff #008800
#f0fff0 #22bb22
#aa6600
#3333bb
#0044dd

#008800

#008800
#888888

#bb0066
#bb0066
#0066bb
#336699
#bb0066
#003388
#336699
#336699
#3333bb
#dd7700
#003366
#bb0066
#336699
#555555
#336699

#0000DD

#333
#666
#ffdddd #000000
#ddffdd #000000
#aa0000

#555555
#888888
#aa0000

#e3d2d2 #a61717
"""

"""

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace


__all__ = ['PastieStyle']


class PastieStyle(Style):
    

    name = 'pastie'
    
    styles = {
        Whitespace:             '#bbbbbb',
        Comment:                '#888888',
        Comment.Preproc:        'bold #cc0000',
        Comment.Special:        'bg:#fff0f0 bold #cc0000',

        String:                 'bg:#fff0f0 #dd2200',
        String.Regex:           'bg:#fff0ff #008800',
        String.Other:           'bg:#f0fff0 #22bb22',
        String.Symbol:          '#aa6600',
        String.Interpol:        '#3333bb',
        String.Escape:          '#0044dd',

        Operator.Word:          '#008800',

        Keyword:                'bold #008800',
        Keyword.Pseudo:         'nobold',
        Keyword.Type:           '#888888',

        Name.Class:             'bold #bb0066',
        Name.Exception:         'bold #bb0066',
        Name.Function:          'bold #0066bb',
        Name.Property:          'bold #336699',
        Name.Namespace:         'bold #bb0066',
        Name.Builtin:           '#003388',
        Name.Variable:          '#336699',
        Name.Variable.Class:    '#336699',
        Name.Variable.Instance: '#3333bb',
        Name.Variable.Global:   '#dd7700',
        Name.Constant:          'bold #003366',
        Name.Tag:               'bold #bb0066',
        Name.Attribute:         '#336699',
        Name.Decorator:         '#555555',
        Name.Label:             'italic #336699',

        Number:                 'bold #0000DD',

        Generic.Heading:        '#333',
        Generic.Subheading:     '#666',
        Generic.Deleted:        'bg:#ffdddd #000000',
        Generic.Inserted:       'bg:#ddffdd #000000',
        Generic.Error:          '#aa0000',
        Generic.Emph:           'italic',
        Generic.Strong:         'bold',
        Generic.EmphStrong:     'bold italic',
        Generic.Prompt:         '#555555',
        Generic.Output:         '#888888',
        Generic.Traceback:      '#aa0000',

        Error:                  'bg:#e3d2d2 #a61717'
    }



    """