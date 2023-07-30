import logging
import os


def pad_list(original_list, n, padding_value=None):
    if len(original_list) < n:
        padding_count = n - len(original_list)
        padded_list = original_list + [padding_value] * padding_count
    else:
        padded_list = original_list[:n]
    return padded_list


def create_directories(directory_names):
    for name in directory_names:
        if not os.path.exists(name):
            try:
                os.mkdir(name)
                print(f"디렉토리 '{name}'가 생성되었습니다.")
            except Exception as e:
                logging.exception(e)
