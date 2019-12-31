from commands import *
from givenumber import script_dir


def check_archive(integer):
    string = str(integer)
    sub_archive = string[:-4]+"0k"
    archive_file = Path.combine(script_dir, 'archive', f"starting_'{sub_archive}'.txt")

    if not File.exist(archive_file):
        File.create(archive_file)

    all_strings = Str.nl(File.read(archive_file))

    if string in all_strings:
        return False
    File.write(archive_file, string+newline)
    return True