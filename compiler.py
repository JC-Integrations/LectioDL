import PyInstaller.__main__
from shutil import rmtree
from os import remove

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--distpath=.',
    '--name=LectioDL',
    '--icon=LectioDL.ico'
])

# Cleanup build deps
rmtree("build")
remove("LectioDL.spec")

input("\nLectioDL.exe er nu oprettet, dette vindue kan lukkes.")