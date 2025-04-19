def apply_theme(text_area, theme):
    themes = {
        "light": {"bg": "white", "fg": "black"},
        "dark": {"bg": "black", "fg": "white"},
        }
    text_area.config(bg=themes[theme]["bg"], fg=themes[theme]["fg"], insertbackground=themes[theme]["fg"])
