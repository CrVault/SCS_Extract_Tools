import os
import re
import sys
import time
import threading

def loading_animation():
    while True:
        for char in '-\|/':
            sys.stdout.write('\r' + char + ' Parsing directories in the mod files ...')
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 10 + '\r')
    sys.stdout.flush()

loading_thread = threading.Thread(target=loading_animation)
loading_thread.daemon = True  
loading_thread.start()

# code created by CracksVault, if it makes any difference in your insignificant life.

import os
import re

extensions = ['.tga', '.mat', '.tobj', '.pmd', '.pmc', '.pma', '.sii', '.dds', '.ogg', '.jpg', '.sui', '.bank', '.bank.guid', '.mask']

file_extensions_to_read = ['.sii', '.pmd', '.tobj', '.mat', '.soundref', '.sui']

pattern = re.compile(r'(/[^\s]*(' + '|'.join([re.escape(ext) for ext in extensions]) + '))')

def add_redundancies(paths):
    redundant_extensions = ['pmd', 'pmc', 'pmg']
    for path in paths[:]:
        ext = os.path.splitext(path)[-1].lower()
        if ext in ['.pmd', '.pmc', '.pmg']:
            for redundant_ext in redundant_extensions:
                if not path.endswith(redundant_ext):
                    redundant_path = os.path.splitext(path)[0] + '.' + redundant_ext
                    paths.append(redundant_path)
    return paths

def find_paths_in_file(filename):
    with open(filename, 'r', errors='ignore') as file:
        content = file.read()
        matches = [match[0] for match in pattern.findall(content)]
        matches = split_concatenated_paths(matches)
        matches = add_redundancies(matches)
        return matches

def split_concatenated_paths(matches):
    split_matches = []
    for match in matches:
        paths = re.split(r'[\x00-\x1F]+', match)
        for path in paths:
            if any(path.endswith(ext) for ext in extensions):
                split_matches.append(path)
    return split_matches

def find_paths_in_directory(directory):
    results = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions_to_read):
                full_path = os.path.join(root, file)
                matches = find_paths_in_file(full_path)
                if matches:
                    results[full_path] = matches
    return results

def save_results_to_file(results, filename='list.txt'):
    with open(filename, 'w') as file:
        for matches in results.values():
            for match in matches:
                file.write(f"{match.strip()}\n")  

results = find_paths_in_directory('.')
save_results_to_file(results)
