async def normalize_day_key(day_value) -> str:
    if day_value is None:
        return None
    
    if hasattr(day_value, "name"):
        return day_value.name.upper()
    
    return str(day_value).upper()