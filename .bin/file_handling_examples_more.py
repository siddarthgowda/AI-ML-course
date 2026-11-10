"""Remaining file-handling example programs (Q51–Q227)."""
from file_handling_examples import add

add(51, '''
from pathlib import Path

path = Path("file_demo/why_with.txt")
path.parent.mkdir(exist_ok=True)
with path.open("w") as file:
    file.write("safe close\\n")
print("no need to call close(); closed =", file.closed)
''')

add(52, '''
from pathlib import Path

Path("file_demo").mkdir(exist_ok=True)
manual = open("file_demo/manual.txt", "w")
manual.write("remember to close\\n")
manual.close()
print("manual closed:", manual.closed)

with open("file_demo/auto.txt", "w") as auto:
    auto.write("closes itself\\n")
print("with closed:", auto.closed)
''')

add(53, '''
from pathlib import Path

path = Path("file_demo/crash.txt")
path.parent.mkdir(exist_ok=True)
try:
    with path.open("w") as file:
        file.write("partial\\n")
        raise RuntimeError("stopped while writing")
except RuntimeError as error:
    print(error)
print("file still closed:", file.closed)
print(path.read_text())
''')

add(54, '''
from pathlib import Path

class Demo:
    def __enter__(self):
        print("enter")
        return "resource"

    def __exit__(self, exc_type, exc, tb):
        print("exit")
        return False

with Demo() as value:
    print("inside", value)
''')

add(55, '''
class Guard:
    def __enter__(self):
        self.file = open("file_demo/exit_demo.txt", "w")
        return self.file

    def __exit__(self, exc_type, exc, tb):
        self.file.close()
        print("exit closed the file:", self.file.closed)
        return False

from pathlib import Path
Path("file_demo").mkdir(exist_ok=True)
with Guard() as file:
    file.write("hello from custom exit\\n")
''')

add(56, '''
from pathlib import Path

class open_demo:
    def __init__(self, path, mode):
        self.path = path
        self.mode = mode

    def __enter__(self):
        self.file = open(self.path, self.mode)
        return self.file

    def __exit__(self, exc_type, exc, tb):
        self.file.close()
        return False

Path("file_demo").mkdir(exist_ok=True)
with open_demo("file_demo/own_cm.txt", "w") as file:
    file.write("custom context manager\\n")
print(Path("file_demo/own_cm.txt").read_text())
''')

add(57, '''
try:
    open("file_demo/no_such_file.txt", "r")
except FileNotFoundError as error:
    print("caught", type(error).__name__)
''')

add(58, '''
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
try:
    open(folder / "missing.txt")
except OSError as error:
    print("FileNotFoundError ->", type(error).__name__)
taken = folder / "taken.txt"
taken.write_text("x")
try:
    open(taken, "x")
except OSError as error:
    print("FileExistsError ->", type(error).__name__)
''')

add(59, '''
try:
    open("file_demo/absent.txt", "r")
except FileNotFoundError as error:
    print(type(error).__name__, ":", error)
''')

add(60, '''
import os
from pathlib import Path

path = Path("file_demo/locked.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("secret\\n")
os.chmod(path, 0)
try:
    open(path, "r")
except PermissionError as error:
    print(type(error).__name__)
finally:
    os.chmod(path, 0o644)
''')

add(61, '''
from pathlib import Path

path = Path("file_demo/only_once.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("exists\\n")
try:
    open(path, "x")
except FileExistsError as error:
    print(type(error).__name__)
''')

add(62, '''
from pathlib import Path

path = Path("file_demo/latin.txt")
path.parent.mkdir(exist_ok=True)
path.write_bytes("café".encode("latin-1"))
try:
    path.read_text(encoding="ascii")
except UnicodeDecodeError as error:
    print(type(error).__name__)
print(path.read_text(encoding="latin-1"))
''')

add(63, '''
try:
    open("file_demo/does_not_exist.txt", "r")
except OSError as error:
    print(type(error).__name__, "is an", OSError.__name__)
''')

add(64, '''
from pathlib import Path

path = Path("file_demo/handled.txt")
try:
    with path.open() as file:
        print(file.read())
except FileNotFoundError:
    path.parent.mkdir(exist_ok=True)
    path.write_text("created after the error\\n")
    print(path.read_text())
''')

add(65, '''
from pathlib import Path

path = Path("file_demo/try_flow.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("ok\\n")
try:
    text = path.read_text()
except FileNotFoundError:
    print("except")
else:
    print("else:", text.strip())
finally:
    print("finally: cleanup always runs")
''')

add(66, '''
from pathlib import Path

Path("file_demo").mkdir(exist_ok=True)
file = open("file_demo/close_me.txt", "w")
file.write("done\\n")
print("before:", file.closed)
file.close()
print("after:", file.closed)
''')

add(67, '''
from pathlib import Path

path = Path("file_demo/flush_me.txt")
path.parent.mkdir(exist_ok=True)
file = path.open("w")
file.write("visible after flush")
file.flush()
print(path.read_text())
file.close()
''')

add(68, '''
from pathlib import Path

path = Path("file_demo/readable.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("hi\\n")
with path.open("r") as file:
    print("r readable:", file.readable())
with path.open("w") as file:
    print("w readable:", file.readable())
''')

add(69, '''
from pathlib import Path

path = Path("file_demo/writable.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("hi\\n")
with path.open("r") as file:
    print("r writable:", file.writable())
with path.open("a") as file:
    print("a writable:", file.writable())
''')

add(70, '''
from pathlib import Path

path = Path("file_demo/seekable.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("seek me\\n")
with path.open() as file:
    print("disk file seekable:", file.seekable())
''')

add(71, '''
from pathlib import Path

Path("file_demo").mkdir(exist_ok=True)
with open("file_demo/fd.txt", "w") as file:
    print("file descriptor:", file.fileno())
''')

add(72, '''
from pathlib import Path

Path("file_demo").mkdir(exist_ok=True)
with open("file_demo/tty.txt", "w") as file:
    print("regular file isatty:", file.isatty())
''')

add(73, '''
from pathlib import Path

Path("file_demo").mkdir(exist_ok=True)
file = open("file_demo/closed_flag.txt", "w")
print(file.closed)
file.close()
print(file.closed)
''')

add(74, '''
from pathlib import Path

Path("file_demo").mkdir(exist_ok=True)
with open("file_demo/name_attr.txt", "w") as file:
    print(file.name)
''')

add(75, '''
from pathlib import Path

path = Path("file_demo/mode_attr.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("x")
with path.open("r") as file:
    print(file.mode)
''')

add(76, '''
import os

print("module file:", os.__file__)
print("getcwd is a function:", callable(os.getcwd))
''')

add(77, '''
import os
from pathlib import Path

folder = Path("file_demo/os_demo")
folder.mkdir(parents=True, exist_ok=True)
(folder / "note.txt").write_text("hi\\n")
print(os.listdir(folder))
''')

add(78, '''
import os
from pathlib import Path

folder = Path("file_demo/os_tour")
folder.mkdir(parents=True, exist_ok=True)
note = folder / "a.txt"
note.write_text("hi\\n")
print("exists", os.path.exists(note))
print("isfile", os.path.isfile(note))
print("size", os.path.getsize(note))
print("names", os.listdir(folder))
''')

add(79, '''
import os

print(os.getcwd())
''')

add(80, '''
import os
from pathlib import Path

folder = Path("file_demo/chdir_demo").resolve()
folder.mkdir(parents=True, exist_ok=True)
previous = os.getcwd()
try:
    os.chdir(folder)
    print(os.getcwd())
finally:
    os.chdir(previous)
''')

add(81, '''
import os
from pathlib import Path

target = Path("file_demo/one_dir")
target.parent.mkdir(exist_ok=True)
if target.exists():
    target.rmdir()
os.mkdir(target)
print(target.is_dir())
''')

add(82, '''
import os
import shutil
from pathlib import Path

target = Path("file_demo/nested/a/b")
if target.exists():
    shutil.rmtree(Path("file_demo/nested"))
os.makedirs(target)
print(target.is_dir())
''')

add(83, '''
import os
from pathlib import Path

folder = Path("file_demo/listing")
folder.mkdir(parents=True, exist_ok=True)
(folder / "a.txt").write_text("a")
(folder / "b.txt").write_text("b")
print(sorted(os.listdir(folder)))
''')

add(84, '''
import os
from pathlib import Path

path = Path("file_demo/delete_me.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("bye\\n")
os.remove(path)
print("still there:", path.exists())
''')

add(85, '''
import os
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
old = folder / "old_name.txt"
new = folder / "new_name.txt"
new.unlink(missing_ok=True)
old.write_text("renamed\\n")
os.rename(old, new)
print(new.read_text().strip(), "old exists:", old.exists())
''')

add(86, '''
import os
from pathlib import Path

folder = Path("file_demo/empty_dir")
folder.mkdir(parents=True, exist_ok=True)
os.rmdir(folder)
print("removed:", not folder.exists())
''')

add(87, '''
import os
from pathlib import Path

path = Path("file_demo/exists_check.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("yes\\n")
print(os.path.exists(path))
print(os.path.exists("file_demo/nope.txt"))
''')

add(88, '''
import os
from pathlib import Path

folder = Path("file_demo/kind")
folder.mkdir(parents=True, exist_ok=True)
path = folder / "note.txt"
path.write_text("x")
print("file", os.path.isfile(path), "dir", os.path.isdir(path))
print("file", os.path.isfile(folder), "dir", os.path.isdir(folder))
''')

add(89, '''
import shutil
from pathlib import Path

src = Path("file_demo/src_copy.txt")
dst = Path("file_demo/dst_copy.txt")
src.parent.mkdir(exist_ok=True)
src.write_text("copied by shutil\\n")
shutil.copy(src, dst)
print(dst.read_text())
''')

add(90, '''
import shutil
from pathlib import Path

root = Path("file_demo/shutil_tour")
if root.exists():
    shutil.rmtree(root)
(root / "inner").mkdir(parents=True)
(root / "inner" / "a.txt").write_text("A")
shutil.copy(root / "inner" / "a.txt", root / "a_copy.txt")
shutil.copytree(root / "inner", root / "inner_copy")
print(sorted(p.name for p in root.rglob("*")))
shutil.rmtree(root / "inner_copy")
print("disk", shutil.disk_usage(root).total > 0)
''')

add(91, '''
import os
import shutil
from pathlib import Path

folder = Path("file_demo/os_vs_shutil")
folder.mkdir(parents=True, exist_ok=True)
src = folder / "a.txt"
src.write_text("data\\n")
print("os lists:", os.listdir(folder))
shutil.copy(src, folder / "b.txt")
print("shutil copied:", (folder / "b.txt").read_text().strip())
''')

add(92, '''
import os
import shutil
from pathlib import Path

folder = Path("file_demo/copy_meta")
folder.mkdir(parents=True, exist_ok=True)
src = folder / "original.txt"
src.write_text("meta\\n")
os.chmod(src, 0o640)
plain = shutil.copy(src, folder / "plain.txt")
full = shutil.copy2(src, folder / "full.txt")
print("copy mode ", oct(os.stat(plain).st_mode & 0o777))
print("copy2 mode", oct(os.stat(full).st_mode & 0o777))
''')

add(93, '''
from pathlib import Path

path = Path("file_demo/pathlib_intro.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("path object\\n")
print(path.name, path.suffix, path.exists())
''')

add(94, '''
from pathlib import Path

folder = Path("file_demo/path_methods")
folder.mkdir(parents=True, exist_ok=True)
path = folder / "notes.txt"
path.write_text("hello pathlib\\n")
print(path.read_text().strip())
print("is_file", path.is_file())
for child in folder.iterdir():
    print(child.name)
''')

add(95, '''
import os
from pathlib import Path

path = Path("file_demo/both.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("x")
print("os.path", os.path.isfile(path))
print("pathlib", path.is_file())
''')

add(96, '''
import tempfile

with tempfile.TemporaryDirectory() as folder:
    path = tempfile.NamedTemporaryFile("w", dir=folder, delete=False)
    path.write("temp data\\n")
    path.close()
    print(open(path.name).read().strip())
''')

add(97, '''
from io import StringIO

stream = StringIO()
stream.write("in memory\\n")
stream.seek(0)
print(stream.read())
''')

add(98, '''
from io import StringIO

file = StringIO()
file.write("Hello Python")
file.seek(0)
print(file.read())
''')

add(99, '''
from io import BytesIO

file = BytesIO()
file.write(b"Hello")
file.seek(0)
print(file.read())
''')

add(100, '''
from io import BytesIO, StringIO

text = StringIO("Hello")
binary = BytesIO(b"Hello")
text.seek(0)
binary.seek(0)
print(text.read(), binary.read())
''')

add(131, '''
for encoding in ("utf-8", "utf-16", "ascii", "latin-1"):
    print(encoding, "Hi".encode(encoding))
''')

add(132, '''
print("utf-8 ", "Amit".encode("utf-8"))
print("utf-16", "Amit".encode("utf-16"))
print("ascii ", "Amit".encode("ascii"))
print("latin1", "Amit".encode("latin-1"))
''')

add(133, '''
from pathlib import Path

path = Path("file_demo/buffer.txt")
path.parent.mkdir(exist_ok=True)
file = path.open("w", buffering=1)
file.write("line\\n")
file.flush()
print("flushed early:", path.read_text().strip())
file.close()
''')

add(134, '''
from pathlib import Path

path = Path("file_demo/buffer_why.txt")
path.parent.mkdir(exist_ok=True)
with path.open("w", buffering=8192) as file:
    for n in range(3):
        file.write(f"row {n}\\n")
print(path.read_text())
''')

add(135, '''
from pathlib import Path

path = Path("file_demo/text_vs_bin.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hi\\n")
print(path.read_text(), type(path.read_text()).__name__)
print(path.read_bytes(), type(path.read_bytes()).__name__)
''')

add(136, '''
from pathlib import Path

path = Path("file_demo/encoding_param.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("café\\n", encoding="utf-8")
print(path.read_text(encoding="utf-8"))
''')

add(137, '''
import zipfile
from pathlib import Path

folder = Path("file_demo/zip_demo")
folder.mkdir(parents=True, exist_ok=True)
(folder / "a.txt").write_text("alpha\\n")
(folder / "b.txt").write_text("beta\\n")
archive = folder / "notes.zip"
with zipfile.ZipFile(archive, "w") as zipped:
    zipped.write(folder / "a.txt", "a.txt")
    zipped.write(folder / "b.txt", "b.txt")
with zipfile.ZipFile(archive) as zipped:
    print(zipped.namelist())
    print(zipped.read("a.txt").decode())
''')

add(138, '''
import gzip
from pathlib import Path

path = Path("file_demo/notes.txt.gz")
path.parent.mkdir(exist_ok=True)
with gzip.open(path, "wt") as file:
    file.write("Hello gzip\\n")
with gzip.open(path, "rt") as file:
    print(file.read())
''')

add(139, '''
import bz2
from pathlib import Path

path = Path("file_demo/notes.txt.bz2")
path.parent.mkdir(exist_ok=True)
with bz2.open(path, "wt") as file:
    file.write("Hello bz2\\n")
with bz2.open(path, "rt") as file:
    print(file.read())
''')

add(140, '''
import lzma
from pathlib import Path

path = Path("file_demo/notes.txt.xz")
path.parent.mkdir(exist_ok=True)
with lzma.open(path, "wt") as file:
    file.write("Hello lzma\\n")
with lzma.open(path, "rt") as file:
    print(file.read())
''')

add(141, '''
import gzip
import zipfile
from pathlib import Path

folder = Path("file_demo/zip_vs_gzip")
folder.mkdir(parents=True, exist_ok=True)
(folder / "one.txt").write_text("one\\n")
(folder / "two.txt").write_text("two\\n")
with zipfile.ZipFile(folder / "both.zip", "w") as zipped:
    zipped.write(folder / "one.txt", "one.txt")
    zipped.write(folder / "two.txt", "two.txt")
with gzip.open(folder / "one.txt.gz", "wt") as file:
    file.write((folder / "one.txt").read_text())
print("zip has", zipfile.ZipFile(folder / "both.zip").namelist())
print("gzip has one stream")
''')

add(142, '''
from pathlib import Path

path = Path("file_demo/data.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello Python")
file = path.open()
print(file.read(5))
file.close()
''')

add(143, '''
from pathlib import Path

path = Path("file_demo/data143.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello Python")
file = path.open()
print(repr(file.read()))
print(repr(file.read()))
file.close()
''')

add(144, '''
from pathlib import Path

path = Path("file_demo/data144.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello Python")
file = path.open()
print(file.read(5))
print(file.tell())
file.close()
''')

add(145, '''
from pathlib import Path

path = Path("file_demo/data145.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello Python")
file = path.open()
file.read(5)
file.seek(0)
print(file.read(5))
file.close()
''')

add(146, '''
from pathlib import Path

path = Path("file_demo/data146.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello Python")
file = path.open("w")
file.write("Python")
file.close()
print(path.read_text())
''')

add(147, '''
from pathlib import Path

path = Path("file_demo/data147.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello")
file = path.open("a")
file.write(" Python")
file.close()
print(path.read_text())
''')

add(148, '''
from pathlib import Path

path = Path("file_demo/data148.txt")
path.parent.mkdir(exist_ok=True)
path.unlink(missing_ok=True)
file = path.open("x")
file.write("new")
file.close()
print("created", path.exists())
try:
    path.open("x")
except FileExistsError as error:
    print(type(error).__name__)
''')

add(149, '''
from pathlib import Path

Path("file_demo").mkdir(exist_ok=True)
with open("file_demo/data149.txt", "w") as file:
    file.write("Python")
print(file.closed)
''')

add(150, '''
from pathlib import Path

Path("file_demo").mkdir(exist_ok=True)
with open("file_demo/data150.txt", "w") as file:
    print(file.writable())
    print(file.readable())
''')

add(151, '''
from pathlib import Path

Path("file_demo").mkdir(exist_ok=True)
file = open("file_demo/data151.txt", "w")
file.close()
try:
    print(file.read())
except ValueError as error:
    print(type(error).__name__)
''')

add(152, '''
from pathlib import Path

path = Path("file_demo/data152.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Python\\nJava\\nSQL\\n")
with path.open() as file:
    print(repr(file.readline()))
    print(repr(file.readline()))
''')

add(153, '''
from pathlib import Path

path = Path("file_demo/created.txt")
path.parent.mkdir(exist_ok=True)
with path.open("w") as file:
    file.write("Hello Python")
print(path.read_text())
''')

add(154, '''
from pathlib import Path

path = Path("file_demo/to_read.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello Python")
with path.open() as file:
    print(file.read())
''')

add(155, '''
from pathlib import Path

path = Path("file_demo/to_append.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello Python")
with path.open("a") as file:
    file.write("\\nWelcome Python")
print(path.read_text())
''')

add(156, '''
from pathlib import Path

path = Path("file_demo/lines.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("one\\ntwo\\nthree\\n")
with path.open() as file:
    lines = file.readlines()
print(len(lines))
''')

add(157, '''
from pathlib import Path

path = Path("file_demo/words.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello Python world")
words = path.read_text().split()
print(len(words))
''')

add(158, '''
from pathlib import Path

path = Path("file_demo/chars.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello")
print(len(path.read_text()))
''')

add(159, '''
from pathlib import Path

path = Path("file_demo/vowels.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello Python")
count = sum(1 for char in path.read_text().lower() if char in "aeiou")
print(count)
''')

add(160, '''
from pathlib import Path

path = Path("file_demo/word_count.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Python and python")
print(path.read_text().lower().count("python"))
''')

add(161, '''
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
source = folder / "source.txt"
target = folder / "copy_of_source.txt"
source.write_text("copy this text")
target.write_text(source.read_text())
print(target.read_text())
''')

add(162, '''
import shutil
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
source = folder / "shutil_src.txt"
source.write_text("shutil copy")
shutil.copy(source, folder / "shutil_dst.txt")
print((folder / "shutil_dst.txt").read_text())
''')

add(163, '''
import os
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
old = folder / "before.txt"
new = folder / "after.txt"
new.unlink(missing_ok=True)
old.write_text("renamed file")
os.rename(old, new)
print(new.read_text(), old.exists())
''')

add(164, '''
import os
from pathlib import Path

path = Path("file_demo/remove_this.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("gone soon")
os.remove(path)
print(path.exists())
''')

add(165, '''
import os
from pathlib import Path

path = Path("file_demo/maybe.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("here")
if os.path.exists(path):
    print("File exists")
else:
    print("File does not exist")
''')

add(166, '''
from pathlib import Path

path = Path("file_demo/longest.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("I like Python programming")
words = path.read_text().split()
print(max(words, key=len))
''')

add(167, '''
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
source = folder / "forward.txt"
source.write_text("Python")
(folder / "reversed.txt").write_text(source.read_text()[::-1])
print((folder / "reversed.txt").read_text())
''')

add(168, '''
from pathlib import Path

path = Path("file_demo/stream.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("one\\ntwo\\nthree\\n")
with path.open() as file:
    for line in file:
        print(line.strip())
''')

add(169, '''
from pathlib import Path

path = Path("file_demo/blanks.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Amit\\n\\nNeha\\n\\n")
kept = [line for line in path.read_text().splitlines(True) if line.strip()]
path.write_text("".join(kept))
print(repr(path.read_text()))
''')

add(170, '''
from pathlib import Path

path = Path("file_demo/dupes.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Amit\\nNeha\\nAmit\\n")
seen = set()
for line in path.read_text().splitlines():
    if line in seen:
        print("Duplicate:", line)
    else:
        seen.add(line)
''')

add(171, '''
from pathlib import Path

folder = Path("file_demo/box")
folder.mkdir(parents=True, exist_ok=True)
note = folder / "note.txt"
note.write_text("stored in a file\\n")
print("directory", folder.is_dir(), folder)
print("file     ", note.is_file(), note.read_text().strip())
''')

add(172, '''
from pathlib import Path

path = Path("file_demo/abs_demo.txt").resolve()
path.parent.mkdir(exist_ok=True)
path.write_text("absolute\\n")
print(path)
print(path.is_absolute())
''')

add(173, '''
from pathlib import Path

print(Path("file_demo") / "notes.txt")
print((Path("file_demo") / "notes.txt").is_absolute())
''')

add(174, '''
import os
from pathlib import Path

folder = Path("file_demo/remove_vs_rmdir")
folder.mkdir(parents=True, exist_ok=True)
note = folder / "note.txt"
note.write_text("x")
os.remove(note)
os.rmdir(folder)
print("file and empty directory removed", not folder.exists())
''')

add(175, '''
import os
import shutil
from pathlib import Path

single = Path("file_demo/just_one")
nested = Path("file_demo/a/b/c")
single.parent.mkdir(exist_ok=True)
if single.exists():
    single.rmdir()
os.mkdir(single)
if nested.exists():
    shutil.rmtree(Path("file_demo/a"))
os.makedirs(nested)
print(single.is_dir(), nested.is_dir())
''')

add(176, '''
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
(folder / "left.txt").write_text("from left")
with (folder / "left.txt").open() as source, (folder / "right.txt").open("w") as target:
    target.write(source.read())
print((folder / "right.txt").read_text())
''')

add(177, '''
from pathlib import Path

Path("file_demo").mkdir(exist_ok=True)
with open("file_demo/descriptor.txt", "w") as file:
    print(file.fileno())
''')

add(178, '''
from pathlib import Path

path = Path("file_demo/flush_vs_close.txt")
path.parent.mkdir(exist_ok=True)
file = path.open("w")
file.write("saved")
file.flush()
print("after flush, still open:", path.read_text(), "closed", file.closed)
file.close()
print("after close:", file.closed)
''')

add(179, '''
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
trimmed = folder / "trimmed.txt"
trimmed.write_text("Hello Python")
with trimmed.open("r+") as file:
    file.truncate(5)
removed = folder / "removed.txt"
removed.write_text("bye")
removed.unlink()
print(repr(trimmed.read_text()), removed.exists())
''')

add(180, '''
from pathlib import Path

path = Path("file_demo/edit_line.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Rahul\\nPriya\\nAmit\\n")
lines = path.read_text().splitlines()
lines[1] = "Neha"
path.write_text("\\n".join(lines) + "\\n")
print(path.read_text())
''')

add(181, '''
from pathlib import Path

path = Path("file_demo/big_style.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("".join(f"row {n}\\n" for n in range(1000)))
count = 0
with path.open() as file:
    for _ in file:
        count += 1
print(count)
''')

add(182, '''
from pathlib import Path

path = Path("file_demo/newline.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("first\\nsecond\\n")
print(path.read_bytes())
''')

add(183, '''
print(repr("\\n"))
print(repr("\\r\\n"))
print("same text on two lines:" + "\\n" + "next")
''')

add(184, '''
from pathlib import Path

path = Path("file_demo/not_text.bin")
path.parent.mkdir(exist_ok=True)
path.write_bytes(bytes([0xFF, 0xFE, 0x00, 0x80]))
try:
    path.read_text(encoding="utf-8")
except UnicodeDecodeError as error:
    print(type(error).__name__)
''')

add(185, '''
from pathlib import Path

path = Path("file_demo/seek_bin.bin")
path.parent.mkdir(exist_ok=True)
path.write_bytes(b"ABCDEF")
with path.open("rb") as file:
    file.seek(3)
    print(file.read())
''')

add(186, '''
from pathlib import Path

path = Path("file_demo/lakh_style.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("".join(f"id,{n}\\n" for n in range(1, 21)))
total = 0
with path.open() as file:
    next(file)
    for line in file:
        total += int(line.split(",")[1])
print(total)
''')

add(187, '''
from pathlib import Path

path = Path("file_demo/records.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Amit\\n")
with path.open("a") as file:
    file.write("Neha\\n")
print(path.read_text())
''')

add(188, '''
from pathlib import Path

path = Path("file_demo/only_new.txt")
path.parent.mkdir(exist_ok=True)
path.unlink(missing_ok=True)
with path.open("x") as file:
    file.write("first writer wins\\n")
print(path.read_text().strip())
''')

add(189, '''
from pathlib import Path

path = Path("file_demo/crash_safe.txt")
path.parent.mkdir(exist_ok=True)
try:
    with path.open("w") as file:
        file.write("started\\n")
        raise ValueError("boom")
except ValueError:
    print("closed anyway:", file.closed)
''')

add(190, '''
from pathlib import Path

path = Path("file_demo/picture.bin")
path.parent.mkdir(exist_ok=True)
path.write_bytes(b"\\x89PNG\\r\\nfake")
with path.open("rb") as file:
    header = file.read(4)
print(header)
''')

add(191, '''
import shutil
from pathlib import Path

src = Path("file_demo/project")
dst = Path("file_demo/project_copy")
if dst.exists():
    shutil.rmtree(dst)
(src / "data").mkdir(parents=True, exist_ok=True)
(src / "data" / "a.txt").write_text("folder copy")
shutil.copytree(src, dst)
print((dst / "data" / "a.txt").read_text())
''')

add(192, '''
import json
from pathlib import Path

path = Path("file_demo/permanent.json")
path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps({"name": "Amit", "score": 90}, indent=2))
print(json.loads(path.read_text()))
''')

add(193, '''
import csv
from pathlib import Path

path = Path("file_demo/customers193.csv")
path.parent.mkdir(exist_ok=True)
path.write_text("name,city\\nAmit,Bengaluru\\nNeha,Pune\\n")
with path.open(newline="") as file:
    for row in csv.DictReader(file):
        print(row["name"], "from", row["city"])
''')

add(194, '''
from pathlib import Path

path = Path("file_demo/special.txt")
path.parent.mkdir(exist_ok=True)
path.write_bytes("café\\n".encode("utf-8"))
try:
    path.read_text(encoding="ascii")
except UnicodeDecodeError:
    print(path.read_text(encoding="utf-8"))
''')

add(195, '''
import os
from pathlib import Path

folder = Path("file_demo/check_kind")
folder.mkdir(parents=True, exist_ok=True)
note = folder / "note.txt"
note.write_text("x")
print("file", os.path.isfile(note), "dir", os.path.isdir(folder))
''')

add(196, '''
from pathlib import Path

path = Path("file_demo/maybe_missing.txt")
if path.exists():
    print(path.read_text())
else:
    print("create it or skip it; it is not there yet")
''')

add(197, '''
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "scratch.txt"
    path.write_text("temporary\\n")
    print(path.read_text().strip())
print("directory removed after the with block")
''')

add(198, '''
import zipfile
from pathlib import Path

folder = Path("file_demo/pack")
folder.mkdir(parents=True, exist_ok=True)
(folder / "a.txt").write_text("A")
(folder / "b.txt").write_text("B")
archive = folder / "pack.zip"
with zipfile.ZipFile(archive, "w") as zipped:
    zipped.write(folder / "a.txt", "a.txt")
    zipped.write(folder / "b.txt", "b.txt")
print(zipfile.ZipFile(archive).namelist())
''')

add(199, '''
import json

print(json.dumps({"name": "Amit", "active": True, "city": None}))
''')

add(200, '''
import json

sample = {
    "name": "John",
    "age": 25,
    "salary": 30000,
    "active": True,
    "address": None,
    "skills": ["Python", "SQL"],
}
print(json.dumps(sample, indent=2))
''')

add(201, '''
import json

obj = json.loads('{"name": "Amit", "age": 25}')
print(obj["name"], obj["age"])
''')

add(202, '''
import json

data = json.loads('{"skills": ["Python", "NumPy", "Pandas"]}')
print(data["skills"][0])
''')

add(203, '''
import json
from pathlib import Path

data = {"name": "John", "age": 25}
print(json.dumps(data))
path = Path("file_demo/mod.json")
path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps(data))
print(json.loads(path.read_text())["name"])
''')

add(204, '''
import json

data = {"name": "John", "age": 25, "active": True}
print(json.dumps(data))
''')

add(205, '''
import json

data = json.loads('{"name": "John", "age": 25}')
print(data["name"])
''')

add(206, '''
import json
from pathlib import Path

path = Path("file_demo/write_json.json")
path.parent.mkdir(exist_ok=True)
data = {"name": "John", "age": 25}
with path.open("w") as file:
    json.dump(data, file, indent=4)
print(path.read_text())
''')

add(207, '''
import json
from pathlib import Path

path = Path("file_demo/read_json.json")
path.parent.mkdir(exist_ok=True)
path.write_text('{"name": "John", "age": 25}')
with path.open() as file:
    data = json.load(file)
print(data)
''')

add(208, '''
import json

data = {"b": 1, "a": 2}
print(json.dumps(data, indent=4))
print(json.dumps(data, sort_keys=True))
print(json.dumps(data, separators=(",", ":")))
''')

add(209, '''
import json

text = json.dumps({"name": "John"})
print(text)
print(json.loads(text))
''')

add(210, '''
import json

data = {"ok": True, "n": None, "tags": ["a", "b"]}
print(json.dumps(data))
print(json.loads(json.dumps(data)))
''')

add(211, '''
data = {
    "employee": {
        "name": "Amit",
        "details": {"age": 25, "city": "Bengaluru"},
    }
}
print(data["employee"]["name"])
print(data["employee"]["details"]["city"])
''')

add(212, '''
import json

try:
    json.loads('{"name": "John"')
except json.JSONDecodeError as error:
    print("Invalid JSON:", error.msg)
''')

add(213, '''
import json
from datetime import datetime

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

data = {"date": datetime(2026, 11, 5, 9, 0, 0)}
print(json.dumps(data, cls=MyEncoder))
''')

add(214, '''
import json

data = {"b": 1, "a": "café"}
print(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))
''')

add(215, '''
import json

record = {"name": "Amit"}
as_text = json.dumps(record)
print(type(record).__name__, record)
print(type(as_text).__name__, as_text)
''')

add(216, '''
import pickle

blob = pickle.dumps({"name": "John"})
print(pickle.loads(blob))
''')

add(217, '''
import pickle
from pathlib import Path

path = Path("file_demo/funcs.pkl")
path.parent.mkdir(exist_ok=True)
blob = pickle.dumps([1, 2, 3])
path.write_bytes(pickle.dumps([1, 2, 3]))
print(pickle.loads(blob))
print(pickle.loads(path.read_bytes()))
''')

add(218, '''
import pickle
from pathlib import Path

path = Path("file_demo/person.pkl")
path.parent.mkdir(exist_ok=True)
data = {"name": "John", "age": 25}
with path.open("wb") as file:
    pickle.dump(data, file)
with path.open("rb") as file:
    print(pickle.load(file))
''')

add(219, '''
import json
import pickle

data = {"name": "John", "age": 25}
print(json.dumps(data))
print(pickle.loads(pickle.dumps(data)))
''')

add(220, '''
import pickle

blob = pickle.dumps({"name": "John"}, protocol=pickle.HIGHEST_PROTOCOL)
print("protocol bytes", blob[0:2])
print(pickle.loads(blob))
''')

add(221, '''
from pathlib import Path

print(Path("file_demo/notes.txt"))
print(Path.cwd().name)
''')

add(222, '''
from pathlib import Path

print(Path("file_demo/data.txt"))
print(Path("file_demo/data.txt").resolve())
print(Path.cwd())
print(Path.home())
''')

add(223, '''
from pathlib import Path

folder = Path("file_demo/checks")
folder.mkdir(parents=True, exist_ok=True)
path = folder / "a.txt"
path.write_text("x")
print(path.exists(), path.is_file(), path.is_dir(), path.is_absolute())
print(folder.is_dir())
''')

add(224, '''
from pathlib import Path

folder = Path("file_demo/ops")
folder.mkdir(parents=True, exist_ok=True)
path = folder / "note.txt"
path.write_text("Hello Python")
print(path.read_text())
path.write_bytes(b"Hello")
print(path.read_bytes())
nested = folder / "a" / "b"
nested.mkdir(parents=True, exist_ok=True)
print(nested.is_dir())
''')

add(225, '''
from pathlib import Path

path = Path("folder/data.csv")
print(path.name)
print(path.stem)
print(path.suffix)
print(path.parent)
print(path.parts)
''')

add(226, '''
from pathlib import Path

folder = Path("file_demo/search")
(folder / "sub").mkdir(parents=True, exist_ok=True)
(folder / "a.csv").write_text("a")
(folder / "b.txt").write_text("b")
(folder / "sub" / "c.csv").write_text("c")
print(sorted(p.name for p in folder.glob("*.csv")))
print(sorted(p.name for p in folder.rglob("*.csv")))
''')

add(227, '''
import os
from pathlib import Path

path = Path("file_demo/compare.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("x")
print(path.suffix)
print(os.path.splitext(path)[1])
''')

from pathlib import Path


add(101, '''
from pathlib import Path

path = Path("file_demo/people.csv")
path.parent.mkdir(exist_ok=True)
path.write_text("name,city\\nAmit,Bengaluru\\nNeha,Pune\\n")
print(path.read_text())
''')

add(102, '''
import csv
from pathlib import Path

path = Path("file_demo/module.csv")
path.parent.mkdir(exist_ok=True)
with path.open("w", newline="") as file:
    csv.writer(file).writerow(["name", "score"])
print("imported csv and wrote", path.name)
''')

add(103, '''
import csv
from pathlib import Path

path = Path("file_demo/reader.csv")
path.parent.mkdir(exist_ok=True)
path.write_text("name,score\\nAmit,90\\nNeha,85\\n")
with path.open(newline="") as file:
    for row in csv.reader(file):
        print(row)
''')

add(104, '''
import csv
from pathlib import Path

path = Path("file_demo/writer.csv")
path.parent.mkdir(exist_ok=True)
with path.open("w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "score"])
    writer.writerow(["Amit", 90])
print(path.read_text())
''')

add(105, '''
import csv
from pathlib import Path

path = Path("file_demo/dict_reader.csv")
path.parent.mkdir(exist_ok=True)
path.write_text("name,city\\nAmit,Bengaluru\\nNeha,Pune\\n")
with path.open(newline="") as file:
    for row in csv.DictReader(file):
        print(row["name"], row["city"])
''')

add(106, '''
import csv
from pathlib import Path

path = Path("file_demo/dict_writer.csv")
path.parent.mkdir(exist_ok=True)
with path.open("w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "score"])
    writer.writeheader()
    writer.writerow({"name": "Amit", "score": 90})
print(path.read_text())
''')

add(107, '''
import csv
from pathlib import Path

path = Path("file_demo/rows.csv")
path.parent.mkdir(exist_ok=True)
with path.open("w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["one"])
    writer.writerows([["two"], ["three"]])
print(path.read_text())
''')

add(108, '''
import csv
from pathlib import Path

path = Path("file_demo/newline.csv")
path.parent.mkdir(exist_ok=True)
with path.open("w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows([["name"], ["Amit"], ["Neha"]])
print(repr(path.read_text()))
''')

add(109, '''
import csv
from pathlib import Path

path = Path("file_demo/read_csv.csv")
path.parent.mkdir(exist_ok=True)
path.write_text("name,score\\nAmit,90\\nNeha,85\\n")
with path.open(newline="") as file:
    for row in csv.reader(file):
        print(row)
''')

add(110, '''
import csv
from pathlib import Path

path = Path("file_demo/customers.csv")
path.parent.mkdir(exist_ok=True)
path.write_text("name,city\\nAmit,Bengaluru\\n")
with path.open(newline="") as file:
    for row in csv.DictReader(file):
        print(dict(row))
''')

add(111, '''
import json

text = '{"name": "Amit", "active": true, "city": null}'
print(json.loads(text))
''')

add(112, '''
import json

print(json.dumps({"name": "Amit", "score": 90}))
''')

add(113, '''
import json
from pathlib import Path

path = Path("file_demo/load.json")
path.parent.mkdir(exist_ok=True)
path.write_text('{"name": "Amit", "score": 90}\\n')
with path.open() as file:
    data = json.load(file)
print(data["name"], data["score"])
''')

add(114, '''
import json
from pathlib import Path

path = Path("file_demo/dump.json")
path.parent.mkdir(exist_ok=True)
with path.open("w") as file:
    json.dump({"name": "Amit", "score": 90}, file, indent=2)
print(path.read_text())
''')

add(115, '''
import json

data = json.loads('{"name": "Amit", "skills": ["Python", "SQL"]}')
print(data["skills"])
''')

add(116, '''
import json

text = json.dumps({"name": "Amit", "active": True, "city": None})
print(text)
''')

add(117, '''
import json
from pathlib import Path

path = Path("file_demo/load_vs_loads.json")
path.parent.mkdir(exist_ok=True)
path.write_text('{"n": 1}')
with path.open() as file:
    from_file = json.load(file)
from_text = json.loads('{"n": 1}')
print(from_file, from_text)
''')

add(118, '''
import json
from pathlib import Path

path = Path("file_demo/dump_vs_dumps.json")
path.parent.mkdir(exist_ok=True)
with path.open("w") as file:
    json.dump({"n": 1}, file)
print("dump wrote:", path.read_text())
print("dumps returned:", json.dumps({"n": 1}))
''')

add(119, '''
import json

payload = json.dumps({"name": "Amit", "score": 90})
print(payload)
print(type(payload).__name__)
''')

add(120, '''
import json

original = '{"name": "Amit"}'
restored = json.loads(original)
print(restored["name"], type(restored).__name__)
''')

add(121, '''
import json
from pathlib import Path

path = Path("file_demo/student.json")
path.parent.mkdir(exist_ok=True)
student = {"name": "John", "age": 25, "skills": ["Python"]}
path.write_text(json.dumps(student, indent=2))
print(json.loads(path.read_text())["skills"])
''')

add(122, '''
import pickle

blob = pickle.dumps({"name": "John", "scores": [90, 80]})
print(type(blob).__name__, pickle.loads(blob))
''')

add(123, '''
import pickle
from pathlib import Path

path = Path("file_demo/student.pkl")
path.parent.mkdir(exist_ok=True)
with path.open("wb") as file:
    pickle.dump({"name": "John", "age": 25}, file)
print("bytes", path.stat().st_size)
''')

add(124, '''
import pickle
from pathlib import Path

path = Path("file_demo/load.pkl")
path.parent.mkdir(exist_ok=True)
with path.open("wb") as file:
    pickle.dump(["Python", "SQL"], file)
with path.open("rb") as file:
    print(pickle.load(file))
''')

add(125, '''
import pickle

blob = pickle.dumps({"city": "Bengaluru"})
print(blob[:10], "...", len(blob), "bytes")
''')

add(126, '''
import pickle

blob = pickle.dumps({"city": "Bengaluru"})
print(pickle.loads(blob))
''')

add(127, '''
import json
import pickle

data = {"name": "Amit", "active": True}
print("json  ", json.dumps(data))
print("pickle", pickle.dumps(data)[:12])
''')

add(128, '''
import pickle

trusted = pickle.dumps({"ok": True})
print("only load data you created:", pickle.loads(trusted))
print("never pickle.loads() a file from the internet")
''')

add(129, '''
text = "café"
blob = text.encode("utf-8")
print(blob)
''')

add(130, '''
blob = "café".encode("utf-8")
print(blob.decode("utf-8"))
''')
