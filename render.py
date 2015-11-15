from sys import argv

from font_basic import ord_matrix


try:
    import logi
except ImportError:
    has_logi = False
else:
    has_logi = True

FONT_HEIGHT = FONT_WIDTH = len(ord_matrix[0])
# FONT_HEIGHT *= 2
MAT_ADDR = 0x0000
PIXEL_ROWS = 32
PIXEL_COLS = 32
ON_SYMBOL = 'X'
OFF_SYMBOL = ' '


def buffer_from_pixels(pixels):
    frame_buffer = [0] * (PIXEL_ROWS * PIXEL_COLS * 8)
    i = 0
    for p in pixels:
        frame_buffer[i] = p & 0x00FF
        frame_buffer[i + 1] = p >> 8
        i += 2
    return tuple(frame_buffer)


def write_pixels(pixels):
    frame_buffer = buffer_from_pixels(pixels)
    if has_logi:
        logi.logiWrite(MAT_ADDR, frame_buffer)


def render_character(character_bytes, on_symbol=ON_SYMBOL):
    print_buffer = ''
    character_matrix = []

    for x in range(FONT_WIDTH):
        character_row = []
        for y in range(FONT_HEIGHT):
            pixel = character_bytes[x] & 1 << y

            if pixel:
                print_buffer += on_symbol
                character_row.append(on_symbol)
            else:
                print_buffer += OFF_SYMBOL
                character_row.append(OFF_SYMBOL)

        print_buffer += '\n'
        character_matrix.append(character_row)

    return character_matrix


def flatten_row_buffers(row_buffers):
    flattened_rows = []
    for row_buffer in row_buffers:
        flattened_rows.extend(row_buffer)
    return flattened_rows


def make_frame_pixels(ordinals, column_limit=-1):
    COLOR = 755

    bitmaps = [render_character(ord_matrix[ordinal]) for ordinal in ordinals]

    row_buffers = []
    for grouped_rows in zip(*bitmaps):
        flattened_row = []

        for index in range(len(grouped_rows)):
            flattened_row.extend(grouped_rows[index])
            flattened_row = flattened_row[:column_limit]

        row_characters = ''.join(str(t) for t in flattened_row)
        row_characters = row_characters.ljust(PIXEL_COLS, '0')
        print row_characters

        row_buffers.append([COLOR if symbol != OFF_SYMBOL else 0 for symbol in row_characters])

        # Work in progress to get colored characters- ignore...
        # symbol_color_map = {'G': 755, 'B': 255, ' ': 0}
        # row_buffers.append([symbol_color_map[symbol] for symbol in row_characters])

    while len(row_buffers) < PIXEL_ROWS - 1:
        row_buffers.append([0] * PIXEL_COLS)

    return flatten_row_buffers(row_buffers)


if __name__ == '__main__':
    write_pixels(
        make_frame_pixels(
            [ord(letter) for letter in argv[1]],
            column_limit=PIXEL_COLS
        )
    )
