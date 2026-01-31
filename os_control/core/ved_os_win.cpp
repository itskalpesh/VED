/**
 * VED OS Control — Windows implementation
 * Responsibilities: open/close software, find files, open file/folder,
 * shutdown/restart/sleep/lock.
 * No logic here — only OS calls. Safety/confirmation is in Python brain.
 */

#include "../api/ved_os_api.hpp"
#include <algorithm>
#include <filesystem>
#include <string>
#include <vector>

#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <shellapi.h>
#include <tlhelp32.h>
#include <powrprof.h>
#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "user32.lib")
#pragma comment(lib, "powrprof.lib")
#pragma comment(lib, "advapi32.lib")
#endif

namespace ved {
namespace os {

#ifdef _WIN32

namespace {

// UTF-8 ⇄ Wide helpers
std::wstring utf8_to_wide(const std::string& s) {
    if (s.empty()) return {};
    int size = MultiByteToWideChar(CP_UTF8, 0, s.c_str(), -1, nullptr, 0);
    if (size <= 0) return {};
    std::wstring w(size - 1, 0);
    MultiByteToWideChar(CP_UTF8, 0, s.c_str(), -1, &w[0], size);
    return w;
}

std::string wide_to_utf8(const std::wstring& w) {
    if (w.empty()) return {};
    int size = WideCharToMultiByte(CP_UTF8, 0, w.c_str(), -1, nullptr, 0, nullptr, nullptr);
    if (size <= 0) return {};
    std::string s(size - 1, 0);
    WideCharToMultiByte(CP_UTF8, 0, w.c_str(), -1, &s[0], size, nullptr, nullptr);
    return s;
}

} // namespace

bool open_software(const std::string& path_or_name) {
    std::wstring w = utf8_to_wide(path_or_name);
    if (w.empty()) return false;
    HINSTANCE h = ShellExecuteW(nullptr, L"open", w.c_str(), nullptr, nullptr, SW_SHOWNORMAL);
    return reinterpret_cast<INT_PTR>(h) > 32;
}

bool close_software(const std::string& name_or_title) {
    std::wstring key = utf8_to_wide(name_or_title);
    if (key.empty()) return false;

    struct FindData {
        std::wstring key;
        HWND found = nullptr;
    } data{ key, nullptr };

    EnumWindows([](HWND h, LPARAM lp) -> BOOL {
        auto* d = reinterpret_cast<FindData*>(lp);
        if (!IsWindowVisible(h)) return TRUE;

        wchar_t title[512]{};
        if (GetWindowTextW(h, title, 512)) {
            if (std::wstring(title).find(d->key) != std::wstring::npos) {
                d->found = h;
                return FALSE;
            }
        }
        return TRUE;
    }, reinterpret_cast<LPARAM>(&data));

    if (!data.found) return false;
    PostMessageW(data.found, WM_CLOSE, 0, 0);
    return true;
}

std::vector<std::string> get_running_apps() {
    std::vector<std::string> out;

    struct EnumData {
        std::vector<std::string>* out;
    } data{ &out };

    EnumWindows([](HWND h, LPARAM lp) -> BOOL {
        if (!IsWindowVisible(h)) return TRUE;

        auto* d = reinterpret_cast<EnumData*>(lp);
        wchar_t title[512]{};

        if (GetWindowTextW(h, title, 512) && title[0]) {
            std::string s = wide_to_utf8(title);
            if (!s.empty())
                d->out->push_back(s);
        }
        return TRUE;
    }, reinterpret_cast<LPARAM>(&data));

    return out;
}

std::vector<std::string> find_files(const std::string& directory, const std::string& pattern) {
    std::vector<std::string> out;
    try {
        std::filesystem::path base(directory);
        if (!std::filesystem::exists(base)) return out;

        for (const auto& e : std::filesystem::recursive_directory_iterator(base)) {
            if (!e.is_regular_file()) continue;

            std::string name = e.path().filename().string();
            if (pattern.empty() || name.find(pattern) != std::string::npos) {
                out.push_back(e.path().string());
            }
        }
    } catch (...) {}
    return out;
}

bool open_file(const std::string& path) {
    std::wstring w = utf8_to_wide(path);
    if (w.empty()) return false;
    HINSTANCE h = ShellExecuteW(nullptr, L"open", w.c_str(), nullptr, nullptr, SW_SHOWNORMAL);
    return reinterpret_cast<INT_PTR>(h) > 32;
}

bool open_folder(const std::string& path) {
    std::wstring w = utf8_to_wide(path);
    if (w.empty()) return false;
    HINSTANCE h = ShellExecuteW(nullptr, L"explore", w.c_str(), nullptr, nullptr, SW_SHOWNORMAL);
    return reinterpret_cast<INT_PTR>(h) > 32;
}

static bool enable_shutdown_privilege() {
    HANDLE hToken{};
    if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken))
        return false;

    TOKEN_PRIVILEGES tp{};
    tp.PrivilegeCount = 1;
    LookupPrivilegeValueW(nullptr, L"SeShutdownPrivilege", &tp.Privileges[0].Luid);
    tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;

    AdjustTokenPrivileges(hToken, FALSE, &tp, 0, nullptr, nullptr);
    CloseHandle(hToken);
    return GetLastError() == ERROR_SUCCESS;
}

bool request_shutdown() {
    if (!enable_shutdown_privilege()) return false;
    return ExitWindowsEx(EWX_SHUTDOWN | EWX_FORCE, SHTDN_REASON_MAJOR_OTHER) != 0;
}

bool request_restart() {
    if (!enable_shutdown_privilege()) return false;
    return ExitWindowsEx(EWX_REBOOT | EWX_FORCE, SHTDN_REASON_MAJOR_OTHER) != 0;
}

bool request_sleep() {
    return SetSuspendState(FALSE, FALSE, FALSE) != 0;
}

bool lock_workstation() {
    return LockWorkStation() != 0;
}

#else
bool open_software(const std::string&) { return false; }
bool close_software(const std::string&) { return false; }
std::vector<std::string> get_running_apps() { return {}; }
std::vector<std::string> find_files(const std::string&, const std::string&) { return {}; }
bool open_file(const std::string&) { return false; }
bool open_folder(const std::string&) { return false; }
bool request_shutdown() { return false; }
bool request_restart() { return false; }
bool request_sleep() { return false; }
bool lock_workstation() { return false; }
#endif

} // namespace os
} // namespace ved
