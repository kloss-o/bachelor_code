from text_diff import text_differences
import random
from Bachelor.Code.extract_func import get_text_diff_colormaps
from Bachelor.Code.func_compare import create_func_graph


def main():
    text_1 = ['9', '2', '5', '7', '3', '9', '2', '4', '6', '1']
    text_2 = ['8', '3', '6', '1', '4', '8', '9', '2', '4', '5']

    text_3 = ['1', '2', '4', '5', '7', '8', '9', '7', '9', '4']
    text_4 = ['1', '2', '3', '4', '5', '7', '8', '7', '9', '9', '4']

    text_5 = [str(random.randint(0, 9)) for _ in range(100)]
    text_6 = [str(random.randint(0, 9)) for _ in range(100)]

    text_7 = ['1', '2', '3', '4', '5']
    text_8 = ['1', '3', '4']

    diff = text_differences(text_1, text_2)
    for line in diff.diff_lines:
        print(line)

    # print('-------------------------------')

    # diff = text_differences(text_8, text_7)
    # for line in diff.diff_lines:
    #     print(line)

    # print(text_differences(text_3, text_4) == text_differences(text_4, text_3))
    # create_func_graph(text_1, text_2, get_text_diff_colormaps(text_1, text_2)[0], get_text_diff_colormaps(text_1, text_2)[1])
    create_func_graph(text_2, text_1,
                      get_text_diff_colormaps(text_2, text_1)[0],
                      get_text_diff_colormaps(text_2, text_1)[1])


if __name__ == '__main__':
    main()
