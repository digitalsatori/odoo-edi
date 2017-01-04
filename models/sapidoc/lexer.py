"""IDoc Lexer

Parse a SAP IDoc syntax description (as generated by SAP transaction
WE63) into a series of tokens.
"""

from ply import lex
from model import Requirement, Type

states = (
    ('string', 'exclusive'),
    ('number', 'exclusive'),
    ('typename', 'exclusive'),
    ('requirement', 'exclusive'),
    )

keywords = {
    'BEGIN_FIELDS': None,
    'END_FIELDS': None,
    'NAME': 'string',
    'TEXT': 'string',
    'TYPE': 'typename',
    'LENGTH': 'number',
    'FIELD_POS': 'number',
    'CHARACTER_FIRST': 'number',
    'CHARACTER_LAST': 'number',
    'BEGIN_RECORD_SECTION': None,
    'END_RECORD_SECTION': None,
    'BEGIN_CONTROL_RECORD': None,
    'END_CONTROL_RECORD': None,
    'BEGIN_DATA_RECORD': None,
    'END_DATA_RECORD': None,
    'BEGIN_STATUS_RECORD': None,
    'END_STATUS_RECORD': None,
    'BEGIN_SEGMENT_SECTION': None,
    'END_SEGMENT_SECTION': None,
    'BEGIN_IDOC': 'string',
    'END_IDOC': None,
    'BEGIN_SEGMENT': 'string',
    'END_SEGMENT': None,
    'SEGMENTTYPE': 'string',
    'LEVEL': 'number',
    'STATUS': 'requirement',
    'LOOPMIN': 'number',
    'LOOPMAX': 'number',
    'QUALIFIED': None,
    'BEGIN_GROUP': 'number',
    'END_GROUP': None,
    }

tokens = ['STRING', 'NUMBER', 'TYPENAME', 'REQUIREMENT'] + keywords.keys()

t_ANY_ignore = ' \t'

def t_ANY_newline(t):
    r'(\r?\n)'
    t.lexer.lineno += 1
    t.lexer.begin('INITIAL')

def t_KEYWORD(t):
    r'\S+'
    if t.value in keywords:
        t.type = t.value
        state = keywords[t.type]
        if state:
            t.lexer.begin(state)
        return t
    else:
        raise SyntaxError('Unrecognised keyword "%s" on line %d' %
                          (t.value, t.lineno))

def t_string_STRING(t):
    r'[^\r\n]+'
    t.lexer.begin('INITIAL')
    return t

def t_number_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    t.lexer.begin('INITIAL')
    return t

def t_typename_TYPENAME(t):
    r'\S+'
    try:
        t.value = getattr(Type, t.value)
    except KeyError:
        raise SyntaxError('Invalid type "%s"' % t.value)
    t.lexer.begin('INITIAL')
    return t

def t_requirement_REQUIREMENT(t):
    r'\S+'
    try:
        t.value = Requirement[t.value]
    except KeyError:
        raise SyntaxError('Invalid requirement level "%s"' % t.value)
    t.lexer.begin('INITIAL')
    return t

def t_ANY_error(t):
    # There is no way to reach this, but we define it to avoid a
    # spurious warning.
    pass

lexer = lex.lex()
