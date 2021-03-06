import copy
import xml.etree.cElementTree as ET

from parse.Block import Block
from parse.print_color_line import print_color_line


def check_block(block, tag):
    if block is not None:
        if tag == 'column':
            block = copy.deepcopy(block)
            block.current_rows = 0
        elif tag == 'row':
            block = copy.deepcopy(block)
            block.current_cols = 0
    return block


def syntax_analyzer(root: ET.Element, block: Block):
    ans_ = True
    block = check_block(block, root.tag)

    if root.tag == 'block':
        # Проверяем, что размеры вложенного блока не выходят за размеры исходного
        col = int(root.attrib['columns'])
        row = int(root.attrib['rows'])
        if block is not None:
            err = block.check_new_rows_cols(row, col)
            if err:
                print_color_line("1", f'Wrong shape of Block! Wrong count {err}')
                return False
        block = Block(col, row)

    for elem in root:
        # Проверяем соответствие допустимых строк и столбцов
        if block is not None:
            ans = block.add_rows_cols(elem.tag)
            if ans:
                print_color_line("1", f'Wrong count of {ans}')
                return False

        ans_ = ans_ and syntax_analyzer(elem, block)
    return ans_
