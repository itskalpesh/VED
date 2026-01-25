import re

# Advanced blocking patterns
BLOCKED_PATTERNS = [
    r"rm\s+-rf",          # Linux force delete
    r"format\s+[a-zA-Z]:", # Drive formatting
    r"shutdown\s+/[s|r]",  # System shutdown
    r"del\s+/f\s+/s",      # Windows force delete
    r"drop\s+table",       # SQL Injection attempt
]

def safe(text: str) -> bool:
    """
    Returns True if the input is safe, False if it contains dangerous commands.
    """
    text_l = text.lower().strip()
    
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, text_l):
            return False
            
    return True