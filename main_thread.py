import re
from pathlib import Path
import sys
import shutil
from threading import Thread

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for t, c in zip(TRANSLATION, CYRILLIC_SYMBOLS):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()

dict_sort = {
    'images': ['jpeg', 'png', 'jpg', 'svg'],
    'audio': ['mp3', 'ogg', 'wav', 'amr'],
    'documents': ['dov', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
    'videos': ['avi', 'mp4', 'mov', 'mkv'],
    'archives': ['zip', 'gz', 'tar'],
    'others': []
    }

unknown_extensions = []
extensions = []
image_files_list = []
video_files_list = []
document_files_list = []
audio_files_list = []
archive_files_list = []
other_files_list = []
folders = []

def normalize(namefile):
   
    name_file, extension = namefile.split('.')
    name_file = name_file.translate(TRANS)
    name_file = re.sub(r'\W', "_", name_file)
    return f"{name_file}.{extension}"


def get_extensions(file_name):
    
    return Path(file_name).suffix[1:]


def hands_file(file_name, folder, dist):
    
    target_folder = folder / dist
    target_folder.mkdir(exist_ok=True)
    file_name.rename(target_folder / normalize(file_name.name))


def handle_archive(path, folder, dist):
   
    target_folder = folder / dist
    target_folder.mkdir(exist_ok=True)

    norm_name = normalize(path.name).replace(".zip", '').replace(".gz", '').replace(".tar", '')

    archive_folder = target_folder / norm_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), archive_folder)
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def list_folder(folder):
    
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in dict_sort.keys():
                folders.append(item)
                list_folder(item)


def group_files(folder):
    
    for item in folder.iterdir():
        if item.is_file():
            extension = get_extensions(file_name=item.name)
            new_name = folder / item.name
            if extension in dict_sort['images']:
                image_files_list.append(new_name)
                hands_file(new_name, folder, 'images')
            elif extension in dict_sort['videos']:
                video_files_list.append(new_name)
                hands_file(new_name, folder, 'videos')
            elif extension in dict_sort['documents']:
                document_files_list.append(new_name)
                hands_file(new_name, folder, 'documents')
            elif extension in dict_sort['audio']:
                audio_files_list.append(new_name)
                hands_file(new_name, folder, 'audio')
            elif extension in dict_sort['archives']:
                archive_files_list.append(new_name)
                handle_archive(new_name, folder, "archives")
            else:
                other_files_list.append(new_name)
                hands_file(new_name, folder, "others")


def remove_empty_folders(path):

    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def main():
    path = sys.argv[1]
    print(f"Start in {path}")

    folders.append(Path(path))
    list_folder(Path(path))
    print(f"All folders: {folders}\n")

    threads = [] # потоки
    for folder in folders:
        thread = Thread(target=group_files, args=(folder,))
        thread.start()
        threads.append(thread)

    [thread.join() for thread in threads]

    remove_empty_folders(Path(path))

    print(f"Image files: {image_files_list}\n")
    print(f"Video files: {video_files_list}\n")
    print(f"Document files: {document_files_list}\n")
    print(f"Audio files: {audio_files_list}\n")
    print(f"Archive files: {archive_files_list}\n")
    print(f"Unknown files: {other_files_list}\n")
   

if __name__ == '__main__':
    main()
