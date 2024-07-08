
import threading
import time
import os

def search_in_file(file_path, keywords, results):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file_path)
    except Exception as e:
        print("Error reading file {file_path}: {e}")

def worker(file_paths, keywords, results):
    for file_path in file_paths:
        search_in_file(file_path, keywords, results)

def threaded_search(file_paths, keywords):
    results={keyword:[] for keyword in keywords}
    jobs = []
    threads = min(10, len(file_paths))
    files_per_thread = len(file_paths) // threads
    for i in range(0, threads):
        start_index = i * files_per_thread
        end_index = None if i + 1 == threads else (i + 1) * files_per_thread
        thread_files = file_paths[start_index:end_index]
        thread = threading.Thread(target=worker, args=(thread_files, keywords, results))
        jobs.append(thread)
        thread.start()

    for thread in jobs:
        thread.join()

    return results

if __name__ == '__main__':
    directory = "test_files"
    file_paths = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    keywords = ["keyword1", "keyword2", "keyword3"]
    
    start_time = time.time()

    results = threaded_search(file_paths, keywords)

    end_time = time.time()

    print("Threading results:")
    for keyword in keywords:
        print(f'{keyword}: {results[keyword]}')
    print("Execution time:", end_time - start_time)