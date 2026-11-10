"""Runnable example program for each file-handling interview question."""

EXAMPLES = {}

def add(n, code):
    EXAMPLES[n] = code.strip("\n")


add(1, '''
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
notes = folder / "students.txt"

notes.write_text("Rahul\\nPriya\\nAmit\\n")
print(notes.read_text())
notes.unlink()
print("deleted:", not notes.exists())
''')

add(2, '''
from pathlib import Path

path = Path("file_demo/marks.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Math 80\\nPython 95\\n")
print("saved, then read back:")
print(path.read_text())
''')

add(3, '''
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
text_file = folder / "notes.txt"
binary_file = folder / "pixels.bin"
text_file.write_text("Hello Python\\n")
binary_file.write_bytes(bytes([0, 255, 10, 20]))
print("text :", text_file.read_text())
print("bytes:", list(binary_file.read_bytes()))
''')

add(4, '''
from pathlib import Path

path = Path("file_demo/report.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Name,Score\\nAmit,90\\n")
print(path.read_text())
''')

add(5, '''
from pathlib import Path

path = Path("file_demo/photo.bin")
path.parent.mkdir(exist_ok=True)
path.write_bytes(b"\\x89PNG\\r\\n\\x1a\\n")
print(path.read_bytes())
''')

add(6, '''
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
text_file = folder / "hello.txt"
binary_file = folder / "hello.bin"
text_file.write_text("Hello")
binary_file.write_bytes(b"Hello")
print(type(text_file.read_text()), text_file.read_text())
print(type(binary_file.read_bytes()), binary_file.read_bytes())
''')

add(7, '''
from pathlib import Path

Path("file_demo").mkdir(exist_ok=True)
file = open("file_demo/open_demo.txt", "w")
file.write("opened with open()\\n")
file.close()
file = open("file_demo/open_demo.txt", "r")
print(file.read())
file.close()
''')

add(8, '''
from pathlib import Path

Path("file_demo").mkdir(exist_ok=True)
file = open(
    "file_demo/args.txt",
    mode="w",
    buffering=1,
    encoding="utf-8",
    errors="strict",
    newline="\\n",
)
file.write("name,city\\nAmit,Bengaluru\\n")
file.close()
print(Path("file_demo/args.txt").read_text(encoding="utf-8"))
''')

add(9, '''
from pathlib import Path

Path("file_demo").mkdir(exist_ok=True)
file = open("file_demo/object.txt", "w+")
print(type(file).__name__)
file.write("file object\\n")
file.seek(0)
print(file.read())
print("name:", file.name)
print("mode:", file.mode)
file.close()
''')

add(10, '''
from pathlib import Path

path = Path("file_demo/default_mode.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("already here\\n")
file = open(path)  # mode defaults to "r"
print("mode:", file.mode)
print(file.read())
file.close()
''')

add(11, '''
try:
    open("file_demo/missing_student.txt", "r")
except FileNotFoundError as error:
    print(type(error).__name__)
    print(error)
''')

add(12, '''
from pathlib import Path

Path("file_demo").mkdir(exist_ok=True)
Path("file_demo/auto_new.txt").unlink(missing_ok=True)
file = open("file_demo/auto_new.txt", "w")
file.write("created because mode is w\\n")
file.close()
print(Path("file_demo/auto_new.txt").read_text())
''')

add(13, '''
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
path = folder / "modes.txt"
path.write_text("old\\n")

with path.open("r") as file:
    print("r :", file.read().strip())
with path.open("a") as file:
    file.write("added\\n")
print("after a:", path.read_text().replace("\\n", " | "))
with path.open("w") as file:
    file.write("replaced\\n")
print("after w:", path.read_text().strip())
''')

add(14, '''
from pathlib import Path

path = Path("file_demo/read_only.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Rahul\\nPriya\\n")
with path.open("r") as file:
    print(file.read())
''')

add(15, '''
from pathlib import Path

path = Path("file_demo/write_mode.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Rahul\\nPriya\\n")
with path.open("w") as file:
    file.write("Mary\\nTom\\n")
print(path.read_text())
''')

add(16, '''
from pathlib import Path

path = Path("file_demo/append_mode.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello Python\\n")
with path.open("a") as file:
    file.write("Good morning\\n")
print(path.read_text())
''')

add(17, '''
from pathlib import Path

path = Path("file_demo/exclusive.txt")
path.parent.mkdir(exist_ok=True)
path.unlink(missing_ok=True)
with path.open("x") as file:
    file.write("created only once\\n")
print("first:", path.read_text().strip())
try:
    path.open("x").close()
except FileExistsError as error:
    print(type(error).__name__)
''')

add(18, '''
from pathlib import Path

path = Path("file_demo/read_write.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello")
with path.open("r+") as file:
    print("before:", file.read())
    file.seek(0)
    file.write("Hi!!!")
print("after :", path.read_text())
''')

add(19, '''
from pathlib import Path

path = Path("file_demo/write_plus.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("old content")
with path.open("w+") as file:
    file.write("new content")
    file.seek(0)
    print(file.read())
''')

add(20, '''
from pathlib import Path

path = Path("file_demo/append_plus.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello")
with path.open("a+") as file:
    file.write(" Python")
    file.seek(0)
    print(file.read())
''')

add(21, '''
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
write_file = folder / "w_vs_a_w.txt"
append_file = folder / "w_vs_a_a.txt"
write_file.write_text("Rahul\\n")
append_file.write_text("Rahul\\n")
with write_file.open("w") as file:
    file.write("Amit\\n")
with append_file.open("a") as file:
    file.write("Amit\\n")
print("w:", write_file.read_text().replace("\\n", " "))
print("a:", append_file.read_text().replace("\\n", " "))
''')

add(22, '''
from pathlib import Path

path = Path("file_demo/r_vs_rplus.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello")
with path.open("r") as file:
    print("r can read:", file.read())
with path.open("r+") as file:
    print("r+ can read:", file.read())
    file.seek(0)
    file.write("HELLO")
print("r+ also wrote:", path.read_text())
''')

add(23, '''
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
w_plus = folder / "wplus.txt"
a_plus = folder / "aplus.txt"
w_plus.write_text("keep me?\\n")
a_plus.write_text("keep me\\n")
with w_plus.open("w+") as file:
    file.write("fresh\\n")
with a_plus.open("a+") as file:
    file.write("plus more\\n")
print("w+:", w_plus.read_text().strip())
print("a+:", a_plus.read_text().replace("\\n", " | "))
''')

add(24, '''
from pathlib import Path

path = Path("file_demo/image.bin")
path.parent.mkdir(exist_ok=True)
path.write_bytes(b"\\x00\\x01\\x02\\xff")
with path.open("rb") as file:
    data = file.read()
print(data)
print(list(data))
''')

add(25, '''
from pathlib import Path

path = Path("file_demo/sample.bin")
path.parent.mkdir(exist_ok=True)
path.write_bytes(b"Python")
with path.open("rb") as file:
    print(file.read())
    file.seek(0)
    print(file.read(3))
''')

add(26, '''
from pathlib import Path

path = Path("file_demo/exists_x.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("already saved\\n")
try:
    open(path, "x")
except FileExistsError as error:
    print(type(error).__name__)
''')

add(27, '''
from pathlib import Path

path = Path("file_demo/append_seek.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello")
with path.open("a+") as file:
    file.seek(0)
    file.write("!")
print(path.read_text())
''')

add(28, '''
from pathlib import Path

path = Path("file_demo/readers.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Rahul\\nPriya\\nAmit\\n")
with path.open() as file:
    print("read()     :", repr(file.read()))
with path.open() as file:
    print("readline() :", repr(file.readline()))
with path.open() as file:
    print("readlines():", file.readlines())
''')

add(29, '''
from pathlib import Path

path = Path("file_demo/read_method.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Python")
with path.open() as file:
    print(file.read(2))
    print(file.read())
''')

add(30, '''
from pathlib import Path

path = Path("file_demo/readline_method.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Rahul\\nPriya\\nAmit\\n")
with path.open() as file:
    print(repr(file.readline()))
    print(repr(file.readline()))
''')

add(31, '''
from pathlib import Path

path = Path("file_demo/readlines_method.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Rahul\\nPriya\\nAmit\\n")
with path.open() as file:
    rows = file.readlines()
print(rows)
print(len(rows))
''')

add(32, '''
from pathlib import Path

path = Path("file_demo/three_reads.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Py\\nth\\non\\n")
with path.open() as file:
    print("read     ", repr(file.read()))
with path.open() as file:
    print("readline ", repr(file.readline()))
with path.open() as file:
    print("readlines", file.readlines())
''')

add(33, '''
from pathlib import Path

path = Path("file_demo/writers.txt")
path.parent.mkdir(exist_ok=True)
with path.open("w") as file:
    file.write("Rahul\\n")
    file.writelines(["Priya\\n", "Amit\\n"])
print(path.read_text())
''')

add(34, '''
from pathlib import Path

path = Path("file_demo/write_method.txt")
path.parent.mkdir(exist_ok=True)
with path.open("w") as file:
    count = file.write("Hello Python\\n")
print("characters written:", count)
print(path.read_text())
''')

add(35, '''
from pathlib import Path

path = Path("file_demo/writelines_method.txt")
path.parent.mkdir(exist_ok=True)
names = ["Rahul\\n", "Priya\\n", "Amit\\n"]
with path.open("w") as file:
    file.writelines(names)
print(path.read_text())
''')

add(36, '''
from pathlib import Path

folder = Path("file_demo")
folder.mkdir(exist_ok=True)
one = folder / "one_write.txt"
many = folder / "many_writes.txt"
with one.open("w") as file:
    file.write("Rahul\\n")
with many.open("w") as file:
    file.writelines(["Rahul\\n", "Priya\\n"])
print(one.read_text())
print(many.read_text())
''')

add(37, '''
from pathlib import Path

path = Path("file_demo/score.txt")
path.parent.mkdir(exist_ok=True)
score = 95
with path.open("w") as file:
    try:
        file.write(score)
    except TypeError as error:
        print(type(error).__name__)
    file.write(str(score) + "\\n")
print(path.read_text())
''')

add(38, '''
from pathlib import Path

path = Path("file_demo/many_lines.txt")
path.parent.mkdir(exist_ok=True)
lines = ["Python\\n", "NumPy\\n", "Pandas\\n"]
with path.open("w") as file:
    file.writelines(lines)
print(path.read_text())
''')

add(39, '''
from pathlib import Path

path = Path("file_demo/line_by_line.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Rahul\\nPriya\\nAmit\\n")
with path.open() as file:
    for line in file:
        print(line.strip())
''')

add(40, '''
from pathlib import Path

path = Path("file_demo/large_style.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("\\n".join(f"record {n}" for n in range(1, 6)) + "\\n")
total = 0
with path.open() as file:
    for line in file:
        total += 1
print("lines processed one by one:", total)
''')

add(41, '''
from pathlib import Path

path = Path("file_demo/pointer.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("PYTHON")
with path.open() as file:
    print("start", file.tell())
    print(file.read(2))
    print("after two characters", file.tell())
''')

add(42, '''
from pathlib import Path

path = Path("file_demo/tell_demo.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello")
with path.open() as file:
    file.read(2)
    print(file.tell())
''')

add(43, '''
from pathlib import Path

path = Path("file_demo/seek_demo.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello Python")
with path.open() as file:
    file.read(6)
    file.seek(0)
    print(file.read(5))
''')

add(44, '''
from pathlib import Path

path = Path("file_demo/seek_tell.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("ABCDEF")
with path.open() as file:
    file.read(3)
    print("tell:", file.tell())
    file.seek(0)
    print("after seek:", file.read(1))
''')

add(45, '''
from pathlib import Path

path = Path("file_demo/seek_zero.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello")
with path.open() as file:
    print("first :", file.read())
    file.seek(0)
    print("second:", file.read())
''')

add(46, '''
from pathlib import Path

path = Path("file_demo/seek_args.bin")
path.parent.mkdir(exist_ok=True)
path.write_bytes(b"ABCDEFGH")
with path.open("rb") as file:
    file.seek(2, 0)
    print("from start :", file.read(1))
    file.seek(1, 1)
    print("from current:", file.read(1))
    file.seek(-1, 2)
    print("from end   :", file.read(1))
''')

add(47, '''
from pathlib import Path

path = Path("file_demo/truncate_demo.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello Python")
with path.open("r+") as file:
    file.truncate(5)
print(repr(path.read_text()))
''')

add(48, '''
from pathlib import Path

path = Path("file_demo/read_twice.txt")
path.parent.mkdir(exist_ok=True)
path.write_text("Hello Python")
with path.open() as file:
    print("first :", repr(file.read()))
    print("second:", repr(file.read()))
    file.seek(0)
    print("after seek:", file.read())
''')

add(49, '''
from pathlib import Path

path = Path("file_demo/context.txt")
path.parent.mkdir(exist_ok=True)
with path.open("w") as file:
    file.write("closed automatically\\n")
print("closed after with:", file.closed)
print(path.read_text())
''')

add(50, '''
from pathlib import Path

path = Path("file_demo/with_open.txt")
path.parent.mkdir(exist_ok=True)
with open(path, "w") as file:
    file.write("Hello Python\\n")
with open(path, "r") as file:
    print(file.read())
''')
