from typing import List, Any


async def build_text_day(
    day: str, items: List[Any]
) -> str:
    text = f"-- {day} --\n\n"
    
    if not items:
        text += "No tasks for this day😪"
    else:
        for item in items:
            start = item.time_start.strftime("%H:%M")
            end = item.time_end.strftime("%H:%M")
            desc = f"({item.description})" if item.description else ""
            text += f"🕐 {start}:{end} - {item.title}{desc}\n"
    
    return text