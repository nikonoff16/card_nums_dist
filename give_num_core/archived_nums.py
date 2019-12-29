from commands import *
from givenumber import script_dir


def check_archive(integer, verbose=True):
    if verbose:
        b = Bench(quiet=False, fraction_digits=3)

    string = str(integer)
    sub_archive = string[:-4]+"0k"
    if not sub_archive:
        sub_archive = "0"
    archive_file = Path.combine(script_dir, 'archive', f"starting_'{sub_archive}'.txt")

    if not File.exist(archive_file):
        File.create(archive_file)

    all_strings = Str.nl(File.read(archive_file))
    if verbose:
        b.prefix = f"Проверка строки '{string}' из {len(all_strings)} строк"

    if string in all_strings:
        if verbose:
            Print.colored(f"Уже использовано: {string}", "red")
            b.end()
        return False
    File.write(archive_file, string+newline)
    if verbose:
        Print.colored(f"Добавлено в архив: {string}", "green")
        b.end()
    return True


if __name__ == '__main__':
    #bm = Bench("create 1m entries", quiet=False)
    #bk = Bench("create 10k entries ", quiet=False)
    #for i in Int.from_to(1, 1*1000*1000):
    #    if i%10000 == 0:
    #        bk.prefix = bk.prefix[:19] + str(i)
    #        bk.end()
    #    check_archive(i, verbose=False)
    #bm.end()
    while True:
        check_archive(Str.input_int())
