import os
from concurrent.futures import ThreadPoolExecutor, as_completed


def search_files(pattern, path):
    def find_files(root):
        for dirpath, dirnames, filenames in os.walk(root):
            for file_name in filenames:
                file_path = os.path.join(dirpath, file_name)
                if pattern.match(file_name):
                    yield file_path

    executor = ThreadPoolExecutor(max_workers=4)

    dirs = [os.path.join(path, name) for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

    futures = [executor.submit(find_files, dir) for dir in dirs]

    files = []
    for future in as_completed(futures):
        files.extend(future.result())

    executor.shutdown()

    return files
