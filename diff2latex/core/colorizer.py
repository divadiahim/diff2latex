from pygments import lex
from pygments.lexers import PythonLexer, RustLexer
from pygments.lexers import get_all_lexers, _load_lexers
from pygments.styles import get_style_by_name
from pygments.token import Token

def get_char_colors(code, style_name="monokai"):
    _load_lexers(module
    get_all_lexers()  # Load all lexers to ensure availability
    style = get_style_by_name(style_name)
    token_colors = {
        token: f"{style.styles[token]}" if style.styles[token] else "#000000"
        for token in style.styles
    }

    def resolve_color(ttype):
        while ttype not in token_colors:
            ttype = ttype.parent
        return token_colors.get(ttype, "#000000")

    char_colors = []
    for ttype, value in lex(code, PythonLexer()):
        color = resolve_color(ttype)
        for char in value:
            char_colors.append((char, color))
    return char_colors

# Example usage:
code = '''def greet(name):\n    print(f"Hello, {name}!")'''
char_colors = get_char_colors(code)

# Print results
for c, col in char_colors:
    print(f"'{c}' : {col}")
