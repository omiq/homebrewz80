# ANSI escape sequences
reset = "\u001b[0m"
bold = "\u001b[1m"
underline = "\u001b[4m"
reverse = "\u001b[7m"
clear = "\u001b[2J"
clearline = "\u001b[2K"
up = "\u001b[1A"
down = "\u001b[1B"
right = "\u001b[1C"
left = "\u001b[1D"
nextline = "\u001b[1E"
prevline = "\u001b[1F"
top = "\u001b[0;0H"

def gotoxy(x, y):
    return f"\u001b[{y};{x}H"
