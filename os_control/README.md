# VED OS Control (C++)

All OS actions go through this module. No direct OS calls from Python.

## Responsibilities

- Open / close software
- List running apps
- Find files, open file/folder
- Shutdown / restart / sleep / lock (dangerous — brain must confirm first)

## Build (Windows)

Requires: CMake 3.15+, C++17 compiler, Python dev headers.

```bat
cd os_control
cmake -B build -S .
cmake --build build --config Release
```

Output: `build/Release/ved_os.pyd`. Copy to project root or add `build/Release` to `PYTHONPATH` so Python can `import ved_os`.

## Usage from Python (brain only, after permission check)

```python
import ved_os
ved_os.open_software("notepad")
ved_os.open_folder("C:\\Users")
apps = ved_os.get_running_apps()
```

## Architecture

- **api/** — C++ API declarations
- **core/** — Windows implementation (ved_os_win.cpp)
- **bindings/** — pybind11 → Python module `ved_os`
