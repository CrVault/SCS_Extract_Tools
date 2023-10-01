import zipfile
import os

def list_zip_contents(zip_filepath):
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        all_files = zip_ref.namelist()
        file_list = [file for file in all_files if not file.endswith('/')]
        return file_list

def list_directory_contents(directory_path):
    file_list = []
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(full_path, directory_path)
            # Convertendo o caminho para a notação com "/"
            formatted_path = "/" + relative_path.replace(os.sep, "/")
            file_list.append(formatted_path)
    return file_list

def save_to_file(file_list, output_file):
    with open(output_file, 'w') as out:
        for file in file_list:
            out.write(file + "\n")

if __name__ == "__main__":
    choice = input("Você deseja listar um (1) arquivo .zip ou (2) diretório do Windows? ")
    
    if choice == "1":
        zip_filepath = input("Digite o caminho do arquivo .zip: ")
        files = list_zip_contents(zip_filepath)
    elif choice == "2":
        dir_path = input("Digite o caminho do diretório: ")
        files = list_directory_contents(dir_path)
    else:
        print("Opção inválida.")
        exit()

    files.sort()
    save_to_file(files, "list.sii")
    print(f'Lista de arquivos salvos em "list.sii"')
