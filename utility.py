def pad_list(original_list, n, padding_value=None):
    if len(original_list) < n:
        padding_count = n - len(original_list)
        padded_list = original_list + [padding_value] * padding_count
    else:
        padded_list = original_list[:n]
    return padded_list
