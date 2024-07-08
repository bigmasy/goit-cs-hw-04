import multiprocessing
import time
import os

def search_in_file(file_path, keywords):
    results = {keyword: [] for keyword in keywords}
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file_path)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return results

def worker(file_paths, keywords, queue):
    partial_results = {keyword: [] for keyword in keywords}
    for file_path in file_paths:
        result = search_in_file(file_path, keywords)
        for keyword, files in result.items():
            partial_results[keyword].extend(files)
    queue.put(partial_results)

def multiprocessing_search(file_paths, keywords):
    results = {keyword: [] for keyword in keywords}
    jobs = []
    queue = multiprocessing.Queue()
    num_procs = min(10, len(file_paths))
    files_per_process = len(file_paths) // num_procs

    for i in range(num_procs):
        start_index = i * files_per_process
        end_index = None if (i + 1) == num_procs else (i + 1) * files_per_process
        process_files = file_paths[start_index:end_index]
        process = multiprocessing.Process(target=worker, args=(process_files, keywords, queue))
        jobs.append(process)
        process.start()
        start_index = end_index

    for p in jobs:
        p.join()
    
    while not queue.empty():
        result = queue.get()
        for keyword, files in result.items():
            results[keyword].extend(files)

    return results

if __name__ == '__main__':
    directory = "test_files"
    file_paths = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]
    keywords = ["keyword1", "keyword2", "keyword3"]
    
    start_time = time.time()

    results = multiprocessing_search(file_paths, keywords)

    end_time = time.time()

    print("Multiprocessing results:")
    for keyword in keywords:
        print(f'{keyword}: {results[keyword]}')
    print("Execution time:", end_time - start_time)
