"""
对C++文件增加nammespace
"""
import argparse
import os
from typing import List

import toml


def read_isort_config(filepath="pyproject.toml"):
    """Reads isort configuration from pyproject.toml."""

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            config = toml.load(f)

        isort_config = config.get("tool", {}).get("isort", {})
        known_other_party = isort_config.get("known_other_party", [])
        known_first_party = isort_config.get("known_first_party", [])
        known_third_party = isort_config.get("known_third_party", [])

        return known_other_party, known_first_party, known_third_party

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return [], []
    except toml.TomlDecodeError:
        print(f"Error: Failed to decode TOML in '{filepath}'.")
        return [], []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return [], []


def is_in_party(line: str, known_party: List[str],
                target_headers: List[str]) -> bool:
    is_in_party_flag = False
    for header_name in known_party:
        if header_name in line:
            target_headers.append(line)
            is_in_party_flag = True
            break
    return is_in_party_flag


def handle_sort_skip(line: str, headers: List[str], headers_skip: List[str]):
    if 'sort:skip' in line or 'isort:skip' in line:
        headers.pop()
        headers_skip.append(line)


def append_headers(sorted_includes: List[str], libraries_headers: List[str],
                   libraries_headers_skip: List[str]):
    """
    把排序好的头文件，添加到sorted_includes中
    """

    # 存在 "isort:skip,top isort:skip, top"注释的头文件，排到该group最开头的位置
    for header in libraries_headers_skip:
        if ',top' in header or ', top' in header:
            sorted_includes.append(header)

    if libraries_headers:
        sorted_includes.extend(libraries_headers)
    # 默认情况,skip的内容，放到所属组的最末位置
    if libraries_headers_skip:
        for header in libraries_headers_skip:
            if not (',top' in header or ', top' in header):
                sorted_includes.append(header)

    if len(libraries_headers) > 0 or len(libraries_headers_skip) > 0:
        sorted_includes.append('')


# known_other_party, known_first_party, known_third_party


def sort_includes(lines: List[str], known_other_party: List[str],
                  known_first_party: List[str], known_third_party: List[str],
                  input_file: str):
    """对头文件内容，进行排序
    """
    c_system_header_group = [
        "<assert.h>", "<complex.h>", "<ctype.h>", "<errno.h>", "<fenv.h>",
        "<float.h>", "<inttypes.h>", "<iso646.h>", "<limits.h>", "<locale.h>",
        "<math.h>", "<setjmp.h>", "<signal.h>", "<stdalign.h>", "<stdarg.h>",
        "<stdatomic.h>", "<stdbit.h>", "<stdbool.h>", "<stdckdint.h>",
        "<stddef.h>", "<stdint.h>", "<stdio.h>", "<stdlib.h>", "<stdmchar.h>",
        "<stdnoreturn.h>", "<string.h>", "<tgmath.h>", "<threads.h>",
        "<time.h>", "<uchar.h>", "<wchar.h>", "<wctype.h>"
    ]
    c_system_headers = []
    cpp_std_headers = []

    other_libraries_headers = []
    other_libraries_headers_skip = []

    third_party_libraries_headers = []

    project_headers = []
    project_headers_skip = []

    main_header = None
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    if base_name.endswith('_test'):
        base_name = base_name[:-5]
    elif base_name.endswith('_unittest'):
        base_name = base_name[:-9]

    for line in lines:
        line = line.strip()
        if not line.startswith('#include'):
            continue
        if f'{base_name}.h' in line or f'{base_name}.hpp' in line:
            main_header = line

        is_in_c_system_header = is_in_party(line, c_system_header_group,
                                            c_system_headers)
        if is_in_c_system_header:
            continue

        is_in_other_party = is_in_party(line, known_other_party,
                                        other_libraries_headers)
        if is_in_other_party:
            handle_sort_skip(line, other_libraries_headers,
                             other_libraries_headers_skip)
            continue

        is_in_first_party = is_in_party(line, known_first_party,
                                        project_headers)
        if is_in_first_party:
            handle_sort_skip(line, project_headers, project_headers_skip)
            continue

        is_in_third_party = is_in_party(line, known_third_party,
                                        third_party_libraries_headers)
        if is_in_third_party:
            continue

        if '.h>' in line or '.hpp>' in line:
            other_libraries_headers.append(line)
            handle_sort_skip(line, other_libraries_headers,
                             other_libraries_headers_skip)
        if line.endswith('>') and '.' not in line:
            # C++ 标准库头文件
            cpp_std_headers.append(line)
        # elif line.endswith('.h"') or line.endswith('.hpp"'):
        # elif line.endswith('.h"') or line.endswith('.hpp"'):
        elif '.h"' in line or '.hpp"' in line:
            project_headers.append(line)
            handle_sort_skip(line, project_headers, project_headers_skip)

    # 对每个部分的头文件进行排序
    c_system_headers.sort()
    cpp_std_headers.sort()
    other_libraries_headers.sort()
    third_party_libraries_headers.sort()
    project_headers.sort()

    sorted_includes = []
    if main_header:
        sorted_includes.append(main_header)
        sorted_includes.append('')

    if c_system_headers:
        sorted_includes.extend(c_system_headers)
        sorted_includes.append('')

    if cpp_std_headers:
        sorted_includes.extend(cpp_std_headers)
        sorted_includes.append('')

    append_headers(sorted_includes=sorted_includes,
                   libraries_headers=other_libraries_headers,
                   libraries_headers_skip=other_libraries_headers_skip)

    if third_party_libraries_headers:
        sorted_includes.extend(third_party_libraries_headers)
        sorted_includes.append('')

    append_headers(sorted_includes=sorted_includes,
                   libraries_headers=project_headers,
                   libraries_headers_skip=project_headers_skip)

    return sorted_includes


def sort_include_entry(input_file: str,
                       toml_file_path: str,
                       output_file: str,
                       encoding: str = 'utf-8') -> None:
    """Formats a C++ source file's include directives and writes the result.

    The function reads the entire input file, extracts the include lines at
    the beginning, sorts them according to the rules (using known_first_party
    and known_third_party from the TOML file if provided), and writes the sorted
    include block (followed by a blank line) and the remaining code to the output file.

    Args:
        input_file: Path to the input C++ source file.
        toml_file_path: Path to the TOML configuration file.
        output_file: Path to the output file.
        encoding: File encoding (default 'utf-8').
    """
    known_first_party = []
    known_third_party = []
    if toml_file_path != '':
        known_other_party, known_first_party, known_third_party = read_isort_config(
            toml_file_path)

    lines = []
    with open(input_file, encoding=encoding) as f:
        for line in f:
            lines.append(line)

    include_lines = []
    include_row_idxs = []
    non_include_lines = []

    is_preprocessor_condition_met = False
    for row_idx, line in enumerate(lines):
        if line.startswith('#if '):
            is_preprocessor_condition_met = True
        if is_preprocessor_condition_met:
            non_include_lines.append(line)
            continue

        if line.startswith('#include'):
            include_lines.append(line.strip())
            include_row_idxs.append(row_idx)
        else:
            non_include_lines.append(line)

    sorted_includes = sort_includes(include_lines, known_other_party,
                                    known_first_party, known_third_party,
                                    input_file)  # res_list = []

    for line in sorted_includes:
        print(line)

    # 追加写
    with open(output_file, 'w', encoding=encoding) as f:
        for row in range(0, include_row_idxs[0]):
            f.write(lines[row])

        for line in sorted_includes:
            f.write(line + '\n')

        for row in range(include_row_idxs[-1] + 1, len(lines)):
            f.write(lines[row])


# def read_filenames(file_path):
#     """
#     从指定的文本文件中读取每一行的文件名，并去掉前后的空格和换行符，返回文件名列表。

#     :param file_path: str, 文本文件的路径
#     :return: list, 每一行文件名组成的列表
#     """
#     filenames = []
#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             filenames.append(line.strip())
#     return filenames

# def format_cpp_dir_entry(dir_, encoding):
#     """
#     format_cpp_dir_entry
#     """
#     cpp_ignores = read_filenames('D:\\zhusc\\PycharmProjects\\python_basic\\my_format\\cpp_ignore.txt')

#     tmp_dir = os.path.join(dir_, 'format_cpp_dir_entry')
#     os.makedirs(tmp_dir, exist_ok=True)
#     files = os.listdir(dir_)
#     files.sort()
#     for file_name in files:
#         if file_name in cpp_ignores:
#             continue

#         suffix = file_name.split('.')[-1]
#         if suffix not in ['h', 'cpp', 'hpp']:
#             continue

#         file_path = os.path.join(dir_, file_name)
#         tmp_path = os.path.join(dir_, 'del_cpp_debug_code_dir_entry.hpp')
#         sort_include_entry(file_path, tmp_path, encoding)

#         shutil.move(file_path, tmp_dir)
#         os.rename(tmp_path, file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', help="input cpp file", required=False)
    parser.add_argument('--toml',
                        help="toml file's path",
                        default='',
                        required=False)
    parser.add_argument('--dst', help="output cpp file", required=False)
    parser.add_argument('--dir',
                        help="output cpp file",
                        required=False,
                        default='')
    parser.add_argument('--encoding',
                        help="encoding",
                        default='utf-8',
                        required=False)
    args = parser.parse_args()
    if args.dir.strip() == '':
        sort_include_entry(args.src, args.toml, args.dst, args.encoding)
    # else:
    #     format_cpp_dir_entry(args.dir, args.encoding)
