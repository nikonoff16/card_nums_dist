from commands import Str, File, Path, Print, newline
from givenumber import script_dir

archive_file = Path.combine(script_dir, "archive.txt")


def check_archive(integer):
    string = str(integer)

    if not File.exist(archive_file):
        File.create(archive_file)

    if string in Str.nl(File.read(archive_file)):
        Print.colored(f"Уже использовано: {string}", "red")
    else:
        File.write(archive_file, string+newline)
        Print.colored(f"Добавлено в архив: {string}", "green")


if __name__ == '__main__':
    while True:
        check_archive(Str.input_int())
