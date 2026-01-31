# VED OS Control — C++ module (Windows first)
# Build: cmake -B build -S . && cmake --build build
# Output: build/Release/ved_os.pyd (or build/ved_os*.pyd)

cmake_minimum_required(VERSION 3.15)
project(ved_os_control LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

# pybind11: use FetchContent if not installed
include(FetchContent)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v2.11.1
)
FetchContent_MakeAvailable(pybind11)

# Python extension module
pybind11_add_module(ved_os
  bindings/ved_os_bindings.cpp
  core/ved_os_win.cpp
)
target_include_directories(ved_os PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/api)

if(WIN32)
  target_link_libraries(ved_os PRIVATE shell32 user32 powrprof advapi32)
endif()

# Optional: copy built module to project root for "import ved_os"
# Uncomment and set VED_ROOT if you want automatic copy:
# set(VED_ROOT "${CMAKE_SOURCE_DIR}/..")
# add_custom_command(TARGET ved_os POST_BUILD
#   COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_FILE:ved_os> ${VED_ROOT}/ved_os.pyd
# )
