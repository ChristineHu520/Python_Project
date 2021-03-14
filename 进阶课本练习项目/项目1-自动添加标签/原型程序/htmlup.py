"""
@file_name:
@user:christineHu
"""


def lines(file):
    """
        作用：实现在文件末尾增加一个换行
    :param file:
    :return:
    """
    for line in file: yield line
    yield '\n'


def blocks(file):
    """
        作用：实现将文件中的列表项和文本块合并，去掉缩进和空格
    :param file:
    :return:
    """
    block = []
    for line in file:
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []
