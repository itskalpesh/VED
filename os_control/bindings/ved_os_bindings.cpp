/**
 * VED OS Control — Python bindings (pybind11)
 * Exposed as module: ved_os
 * Brain calls these only after permission checks.
 */

#include "../api/ved_os_api.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(ved_os, m) {
    m.doc() = "VED OS Control — open/close apps, find files, open file/folder, shutdown/restart/sleep/lock. Use from brain only after permission check.";

    m.def("open_software", &ved::os::open_software,
          py::arg("path_or_name"),
          "Launch an application by path or executable name.");

    m.def("close_software", &ved::os::close_software,
          py::arg("name_or_title"),
          "Close an application by window title or process name.");

    m.def("get_running_apps", &ved::os::get_running_apps,
          "Get list of running application window titles.");

    m.def("find_files", &ved::os::find_files,
          py::arg("directory"), py::arg("pattern"),
          "Find files under directory matching pattern (e.g. *.txt).");

    m.def("open_file", &ved::os::open_file,
          py::arg("path"),
          "Open a file with default application.");

    m.def("open_folder", &ved::os::open_folder,
          py::arg("path"),
          "Open a folder in explorer.");

    m.def("request_shutdown", &ved::os::request_shutdown,
          "Request system shutdown. Must confirm in Python first.");

    m.def("request_restart", &ved::os::request_restart,
          "Request system restart. Must confirm in Python first.");

    m.def("request_sleep", &ved::os::request_sleep,
          "Put system to sleep.");

    m.def("lock_workstation", &ved::os::lock_workstation,
          "Lock the workstation.");
}
