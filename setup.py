import sys
from cx_Freeze import setup, Executable

include_files = ['autorun.inf']
base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(name="MiniClient2",
      version="0.1",
      description="A small client",
      options={'build_exe':{'include_files':include_files}},
      executables=[Executable("miniclient.py", base=base)])