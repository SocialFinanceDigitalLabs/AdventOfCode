from .output import show_test_results, show_test_opener


def display_test_results(results):
    show_test_opener()
    for index, item in enumerate(results):
        show_test_results(item["Value"], item["Expected"], item["Part"])