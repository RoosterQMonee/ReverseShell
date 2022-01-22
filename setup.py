import sys
from cx_Freeze import setup, Executable

include_files = []
base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(name="MiniClient",
      version="1.0",
      description="A small client",
      options={'build_exe':{'include_files':include_files}},
      executables=[Executable("miniclient.py", base=base)])
