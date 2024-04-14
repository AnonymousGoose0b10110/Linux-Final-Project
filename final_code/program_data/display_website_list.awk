#!/usr/bin/awk -f

BEGIN {
    FS = "|"
    yellow_bold = "\033[1;33m"  # ANSI escape code for bold yellow text
    border_char = "*"            # Border character
    border_length = 60           # Border length
    content_width = 58           # Width of content area
    reset = "\033[0m"            # ANSI escape code to reset formatting

    # Print the top border
    print yellow_bold repeat(border_length, border_char) reset

    # Print the header with border
    header = " List of websites/applications with stored passwords: "
    print yellow_bold border_char " " header " " repeat(border_length - length(header) - 4, " ") border_char reset

    # Print the separator line
    print yellow_bold border_char " " repeat(content_width - 2, "-") " " border_char reset
}

# Read the database file directly and print the website names
FNR == 1 {
    cmd = "sqlite3 " FILENAME " \"SELECT website FROM passwords\""
    while ((cmd | getline website) > 0) {
        print yellow_bold border_char " " website " " repeat(content_width - length(website) - 2, " ") border_char reset
    }
    close(cmd)
}

# Print the bottom border
END {
    print yellow_bold repeat(border_length, border_char) reset
}

function repeat(n, str, result) {
    while (n > 0) {
        result = result str
        n--
    }
    return result
}
