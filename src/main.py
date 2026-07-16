import threading

import flet as ft
from flet import Page, Row, Column, Text, Container, Colors, SnackBar, Image, Stack, MainAxisAlignment, Button

try:
    from playsound3 import playsound as _playsound

    def _play_loop():
        import os
        path = os.path.join(os.path.dirname(__file__), "assets", "audiofondo.mp3")
        if not os.path.exists(path):
            return
        try:
            while True:
                _playsound(path, block=True)
        except Exception:
            pass

    threading.Thread(target=_play_loop, daemon=True).start()
except ImportError:
    pass

GRID_SIZE = 8
TILE_COUNT = GRID_SIZE * GRID_SIZE


def main(page: Page):
    page.title = "Puzzle 8x8 - Jeremy Sarmiento"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = 10

    tiles = list(range(1, 64)) + [64]

    board = Column(spacing=2, horizontal_alignment="center")

    def get_tile_size():
        available = page.width if page.width else 400
        tile_w = max(32, min(70, int((available - 24) // 8)))
        tile_h = int(tile_w * 5 / 7)
        return tile_w, tile_h

    def build_tile(val, idx, is_solved, tile_w, tile_h):
        if val == 64:
            return Container(
                width=tile_w,
                height=tile_h,
                bgcolor=Colors.BLACK,
                border_radius=4,
            )
        tile_image_source = f"/{val}.jpg"
        font_size = max(7, int(tile_w * 0.14))
        num_size = int(tile_w * 0.28)
        return Container(
            content=Stack([
                Image(
                    src=tile_image_source,
                    width=tile_w,
                    height=tile_h,
                    fit="cover",
                ),
                Container(
                    content=Text(
                        str(val),
                        size=font_size,
                        color=Colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                    bgcolor=Colors.BLACK54,
                    padding=2,
                    border_radius=2,
                    alignment=ft.alignment.Alignment.CENTER,
                    width=num_size,
                    height=num_size,
                    left=2,
                    top=2,
                ),
            ]),
            width=tile_w,
            height=tile_h,
            border_radius=4,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            ink=True,
            on_click=lambda e, i=idx: on_tile_click(i),
        )

    def rebuild_board():
        board.controls.clear()
        is_solved = tiles == list(range(1, 64)) + [64]
        tile_w, tile_h = get_tile_size()

        for r in range(GRID_SIZE):
            row_children = []
            for c in range(GRID_SIZE):
                idx = r * GRID_SIZE + c
                val = tiles[idx]
                row_children.append(build_tile(val, idx, is_solved, tile_w, tile_h))
            board.controls.append(Row(row_children, spacing=2, alignment=MainAxisAlignment.CENTER))
        page.update()

        if is_solved:
            show_win_message()

    def find_blank():
        return tiles.index(64)

    def adjacent(i, j):
        if abs(i - j) == 1 and (i // GRID_SIZE) == (j // GRID_SIZE):
            return True
        if abs(i - j) == GRID_SIZE:
            return True
        return False

    def on_tile_click(i):
        if tiles == list(range(1, 64)) + [64]:
            return
        blank_index = find_blank()
        if adjacent(i, blank_index):
            tiles[i], tiles[blank_index] = tiles[blank_index], tiles[i]
            rebuild_board()

    def show_win_message():
        page.snack_bar.open = True
        page.snack_bar.content = Text("¡Felicidades! Puzzle de 8x8 resuelto perfectamente.")
        page.update()

    def shuffle_tiles():
        nonlocal tiles
        tiles = list(range(1, 64)) + [64]
        import random
        for _ in range(1000):
            blank = tiles.index(64)
            possible_moves = []
            if blank % GRID_SIZE > 0:
                possible_moves.append(blank - 1)
            if blank % GRID_SIZE < GRID_SIZE - 1:
                possible_moves.append(blank + 1)
            if blank >= GRID_SIZE:
                possible_moves.append(blank - GRID_SIZE)
            if blank < TILE_COUNT - GRID_SIZE:
                possible_moves.append(blank + GRID_SIZE)
            move = random.choice(possible_moves)
            tiles[blank], tiles[move] = tiles[move], tiles[blank]

    def on_shuffle_click(e):
        shuffle_tiles()
        rebuild_board()

    def on_resize(e):
        rebuild_board()

    page.on_resize = on_resize
    page.snack_bar = SnackBar(content=Text(""))

    title_text = Text("Puzzle 8x8 de Jeremy", size=28, weight=ft.FontWeight.BOLD, color=Colors.PRIMARY)
    subtitle_text = Text("Ordena las imágenes del 1 al 63", size=14, color=Colors.SECONDARY)

    control_buttons = Row(
        [
            Image(
                src="/imgcompleta.jpeg",
                width=150,
                height=150,
                fit="contain",
            ),
            Button("Reordenar", on_click=on_shuffle_click),
        ],
        alignment=MainAxisAlignment.CENTER,
        spacing=20,
    )

    page.add(
        Column(
            [
                title_text,
                subtitle_text,
                Container(height=8),
                board,
                Container(height=10),
                control_buttons,
            ],
            horizontal_alignment="center",
            spacing=5,
        )
    )

    rebuild_board()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
