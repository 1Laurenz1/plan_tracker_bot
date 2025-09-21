import re

from datetime import time
from typing import List, Dict

async def parse_user_text(
    raw_text: str,
    day_of_week: str
) -> List[Dict]:
    items = []
    time_pattern = re.compile(r"(\d{2}:\d{2})[–-](\d{2}:\d{2})")
    
    lines = raw_text.strip().splitlines()
    
    for line in lines:
        match = time_pattern.search(line)
        if not match:
            continue
        
        start_str, end_str = match.groups()
        time_start = time.fromisoformat(start_str)
        time_end = time.fromisoformat(end_str)
        
        parts = line.split("—", maxsplit=1)
        if len(parts) < 2:
            continue
        
        title_desc = parts[1].strip()
        
        if "(" in title_desc and title_desc.endswith(")"):
            title, desc = title_desc.split("(", maxsplit=1)
            title = title.strip()
            description = desc.rstrip(")").strip()
        else:
            title = title_desc
            description = ""
        
        items.append({
            "title": title,
            "description": description,
            "day_of_week": day_of_week,
            "time_start": time_start,
            "time_end": time_end
        })
    
    return items
