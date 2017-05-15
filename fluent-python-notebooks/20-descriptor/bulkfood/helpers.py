def extract_doctsrings(source):
    """ extract the docstrings from an ipython notebook cell

    This will fail if a triple quote is inside a docstring
    Args:
        source (list): python source code as found in an ipynb file (a list of lines)

    Returns:
        A list of docstrings (each represented as a list of lines) and a list
        of the lines that weren't part of docstrings. Docstrings will be
        stripped of enclosing triple quotes.
    """
    docstrings = []
    code = []
    indocstring = False
    target = code
    for line in source:
        if line.startswith("'''") or line.startswith('"""'):
            if indocstring:
                target = code
            else:
                newtarget = list()
                docstrings.append(newtarget)
                target = newtarget
            indocstring = not indocstring
            continue
        target.append(line)
    return docstrings, code


def cell_from_strings(source_strings, **overrides):
    """ build a dict representing an ipython notebook cell

    Args:
        source_strings (list): list of strings to put in cell
        overrides (**kwargs): cell values to override from default

    Returns:
        dictionary representing cell
    """
    cell = {
       "metadata": {
        "collapsed": False
       },
       "source": source_strings,
       }
    cell.update(overrides)
    return cell


def code_cell_from_strings(source_strings, **overrides):
    overrides.update(cell_type="code",
                     execution_count=None,
                     outputs=[],
                     )
    # remove trailing newline from last line in cell
    source_strings[-1] = source_strings[-1].rstrip()
    return cell_from_strings(source_strings, **overrides)


def markdown_cell_from_strings(source_strings, **overrides):
    overrides.update(cell_type="markdown")
    return cell_from_strings(source_strings, **overrides)


CODE_START = "    >>> "
def _is_code(docstring_line):
    return docstring_line.startswith(CODE_START)


def _is_markdown(docstring_line):
    return not docstring_line.startswith(" ")


class CellType:
    markdown = markdown_cell_from_strings
    code = code_cell_from_strings


def carve_up_docstring(docstring_lines):
    """ yields cells from a multiline docstring, using some heuristics """
    current_lines = []
    current_type = None
    for line in docstring_lines:
        if not line.strip():
            if current_type == CellType.markdown:
                current_lines.append(line)
            continue
        if not current_type:
            if not _is_code(line):
                current_type = CellType.markdown
                current_lines.append(line)
            else:
                current_type = CellType.code
                current_lines.append(line[len(CODE_START):])
            continue
        if current_type == CellType.code:
            if not _is_code(line):
                yield current_type(current_lines)
                current_lines = []
                current_type = None
                if _is_markdown(line):
                    current_type = CellType.markdown
                    current_lines.append(line)
            else:
                current_lines.append(line[len(CODE_START):])
            continue
        else:
            assert current_type == CellType.markdown
            if _is_code(line):
                yield current_type(current_lines)
                current_type = CellType.code
                current_lines = []
                current_lines.append(line[len(CODE_START):])
                continue
            current_lines.append(line)
    if current_lines:
        yield current_type(current_lines)


def carve_cell_into_more_cells(orig_cell):
    """ create cells from docstring block comments

    This function determines the order output by carving up a single cell.
    The assumption is that the cell is structured with code that should precede
    the code inside any docstring style block comments.

    Args:
        orig_cell (dict): dictionary representing a cell

    Yields:
        cell dictionaries
    """
    orig_strings = orig_cell['source']
    docstring_blocks, orig_code = extract_doctsrings(orig_strings)
    if orig_code:
        yield code_cell_from_strings(orig_code)

    for docstring_lines in docstring_blocks:
        for new_cell in carve_up_docstring(docstring_lines):
            yield new_cell
