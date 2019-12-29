from commands import *

script_dir = Path.get_parent(Path.safe__file__(__file__))


def check_archive(integer):
    '''
    :param integer: integer, to check that its free
    :return: bool, if its can be used
    '''
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
