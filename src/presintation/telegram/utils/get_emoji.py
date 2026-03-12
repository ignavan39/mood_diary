def get_mood_emoji(value: int) -> str:
    if value <= 2:
        return "😢"
    elif value <= 4:
        return "😟"
    elif value <= 6:
        return "😐"
    elif value <= 8:
        return "🙂"
    else:
        return "😄"
