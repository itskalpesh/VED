/**
 * VED OS Control API — C++ header
 * All OS actions go through this API. No direct OS calls from Python.
 * Windows implementation first.
 */

#pragma once

#include <string>
#include <vector>

namespace ved {
namespace os {

// --- Application control ---
/** Launch an application by path or executable name. Returns true on success. */
bool open_software(const std::string& path_or_name);

/** Close an application by window title or process name. Returns true if found and closed. */
bool close_software(const std::string& name_or_title);

/** Get list of running application window titles (user-visible apps). */
std::vector<std::string> get_running_apps();

// --- File / folder ---
/** Find files under a path matching a pattern (e.g. "*.txt"). Returns full paths. */
std::vector<std::string> find_files(const std::string& directory, const std::string& pattern);

/** Open a file with default associated application. */
bool open_file(const std::string& path);

/** Open a folder in explorer. */
bool open_folder(const std::string& path);

// --- System power / session ---
/** Request system shutdown. Caller must ensure user confirmation done in Python. */
bool request_shutdown();

/** Request system restart. Caller must ensure user confirmation done in Python. */
bool request_restart();

/** Put system to sleep. */
bool request_sleep();

/** Lock the workstation (Windows lock screen). */
bool lock_workstation();

}  // namespace os
}  // namespace ved
