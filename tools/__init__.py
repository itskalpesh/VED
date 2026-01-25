from . import math_tool, time_tool, system_tool, memory_tool, file_tool

TOOLS = [
    (math_tool.can_handle, math_tool.run),
    (time_tool.can_handle, time_tool.run),
    (system_tool.can_handle, system_tool.run),
    (memory_tool.can_handle, memory_tool.run),
    (file_tool.can_handle, file_tool.run),
]