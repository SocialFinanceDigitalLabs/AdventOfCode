from .output import show_test_results, show_test_opener

def run_tests(results):
    show_test_opener()
    for index, item in enumerate(results):
        show_test_results(item["Value"], item["Expected"], item["Part"])