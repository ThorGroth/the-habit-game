# einfache XP/Level-Logik
def xp_to_next(level: int) -> int:
    # einfache lineare Funktion (anpassbar)
    return level * 100

def add_xp(current_xp: int, current_level: int, gained: int):
    new_xp = current_xp + gained
    leveled = False
    new_level = current_level
    while new_xp >= xp_to_next(new_level):
        new_xp -= xp_to_next(new_level)
        new_level += 1
        leveled = True
    return new_xp, new_level, leveled