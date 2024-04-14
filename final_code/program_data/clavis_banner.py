#!/usr/bin/env python3

def print_colored_bordered_message(message, border_char='=', border_length=130, color_code=32):
    border_line = border_char * border_length
    formatted_message = f"\033[{color_code}m{border_line}\n{message}\n{border_line}\033[0m"
    print(formatted_message)


ascii_art = """
 ██████ ██       █████  ██    ██ ██ ███████     ███████ ███    ██  ██████ ██████  ██    ██ ██████  ████████ ██  ██████  ███    ██ 
██      ██      ██   ██ ██    ██ ██ ██          ██      ████   ██ ██      ██   ██  ██  ██  ██   ██    ██    ██ ██    ██ ████   ██ 
██      ██      ███████ ██    ██ ██ ███████     █████   ██ ██  ██ ██      ██████    ████   ██████     ██    ██ ██    ██ ██ ██  ██ 
██      ██      ██   ██  ██  ██  ██      ██     ██      ██  ██ ██ ██      ██   ██    ██    ██         ██    ██ ██    ██ ██  ██ ██ 
 ██████ ███████ ██   ██   ████   ██ ███████     ███████ ██   ████  ██████ ██   ██    ██    ██         ██    ██  ██████  ██   ████ 
                                                                                                                                  
                                                                                                                                  
"""
print_colored_bordered_message(ascii_art, color_code=33)



