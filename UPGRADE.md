# VED Tier-4 Upgrade — Summary

This document summarizes the upgrade per the **VED AI Full Upgrade Plan (Master Document)**.

## Architecture (Respected)

- **One brain** — Single Python decision authority via `brain.router`.
- **Separation of concerns** — Python = brain/safety; C++ = OS control only; GUI = interface only; Voice = I/O only.
- **Hybrid AI** — Offline + online LLM; tools before LLM; rule-engine before LLM.
- **Modular** — Each feature in its own file; no monolithic scripts.

## What Was Implemented

### Phase 1 — OS Control (C++)
- **`os_control/`** added: `api/ved_os_api.hpp`, `core/ved_os_win.cpp`, `bindings/ved_os_bindings.cpp`, `CMakeLists.txt`.
- Responsibilities: open/close software, get running apps, find files, open file/folder, shutdown/restart/sleep/lock.
- Windows implementation first; stubs for non-Windows.

### Phase 2 — Python ↔ C++ Bridge
- pybind11 used to expose C++ as Python module **`ved_os`**.
- Brain calls `ved_os` only after permission checks.

### Phase 3 — Brain Routing & Permissions
- **`brain/intent_engine.py`** — Classifies: os_command, file_action, voice_command, normal_query.
- **`brain/permissions.py`** — SAFE_MODE (read-only) vs ACTION_MODE; dangerous actions require confirmation.
- **`brain/router.py`** — Safety → intent → permission → ved_os or existing planner/LLM. **Explainable responses**: [Action], [Why], [Tool], [Result].
- **`kernel.ved`** — Wired to `brain.router.route`; supports `confirmed_danger` for shutdown/restart.

### Phase 4 — Voice
- **`voice/stt.py`** — Speech-to-text (listen → text).
- **`voice/voice_loop.py`** — Optional loop: listen → brain → speak; voice confirmation for dangerous actions.

### Phase 5 — GUI Structure
- **`gui/electron/`** and **`gui/react/`** — Placeholder READMEs; implement when scoped.

### Phase 6 — Doctor
- **`doctor/ved_doctor.py`** — Checks: ved_os, Python, brain, LLM, memory, voice, GUI. Run: `python -m doctor.ved_doctor`.

### Entry & Config
- **`ved_start.py`** — Single entry: `python ved_start.py` (CLI) or `python ved_start.py gui`.
- Config remains in **`config/config.py`** (all imports use `config.config`).

## Current Layout vs Spec “Final Structure”

| Spec (locked)     | Current location        |
|-------------------|-------------------------|
| brain/router.py   | ✅ brain/router.py       |
| brain/intent_engine.py | ✅ brain/intent_engine.py |
| brain/planner.py  | planner/planner.py (used by brain via ai.hybrid_llm) |
| brain/memory.py   | memory/memory.py        |
| brain/model_manager.py | models/model_manager.py |
| brain/offline_llm.py | models/offline/         |
| brain/online_llm.py  | models/online/         |
| tools/*            | ✅ tools/*               |
| os_control/        | ✅ os_control/           |
| voice/*            | ✅ voice/ (stt, tts, voice_loop) |
| gui/electron, react | ✅ placeholders         |
| doctor/ved_doctor.py | ✅ doctor/ved_doctor.py |
| ved_start.py       | ✅ ved_start.py          |
| config.py          | config/config.py        |

Optional next step: move planner, memory, model_manager, offline_llm, online_llm **into** `brain/` and update imports for exact spec layout.

## Build & Run

1. **OS control (optional)**  
   ```bat
   cd os_control && cmake -B build -S . && cmake --build build --config Release
   ```  
   Copy `build/Release/ved_os.pyd` to project root or add to `PYTHONPATH`.

2. **CLI**  
   `python ved_start.py` or `python -m kernel.main`

3. **GUI**  
   `python ved_start.py gui` or `python -m ui.jarvis_ui`

4. **Doctor**  
   `python -m doctor.ved_doctor`

## Notes for Cursor AI

- Do not add extra brains; single authority is `brain.router`.
- Do not mix GUI with logic; GUI only talks to Python brain.
- Phases were applied in order; code kept clean and commented.
