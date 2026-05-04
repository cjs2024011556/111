import random
import tkinter as tk
from tkinter import messagebox


class Minesweeper:
    def __init__(self, root, rows=10, cols=10, mines=15):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines_count = mines
        self.buttons = []
        self.board = []
        self.revealed = set()
        self.flagged = set()
        self.mine_positions = set()
        self.first_click = True
        self.game_over = False

        self.root.title("扫雷")
        self.root.resizable(False, False)

        self.status_var = tk.StringVar()
        self.status_var.set("左键翻开，右键插旗")

        top = tk.Frame(root, padx=10, pady=8)
        top.pack(fill="x")

        self.status_label = tk.Label(top, textvariable=self.status_var, anchor="w")
        self.status_label.pack(side="left")

        restart_btn = tk.Button(top, text="重新开始", command=self.reset_game)
        restart_btn.pack(side="right")

        self.grid_frame = tk.Frame(root, padx=10, pady=10)
        self.grid_frame.pack()

        self.build_ui()
        self.reset_game()

    def build_ui(self):
        self.buttons = []
        for r in range(self.rows):
            row_buttons = []
            for c in range(self.cols):
                btn = tk.Button(
                    self.grid_frame,
                    text="",
                    width=3,
                    height=1,
                    font=("Arial", 12, "bold"),
                    relief="raised",
                    bg="#d9d9d9",
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                btn.bind("<Button-1>", lambda e, rr=r, cc=c: self.on_left_click(rr, cc))
                btn.bind("<Button-3>", lambda e, rr=r, cc=c: self.on_right_click(rr, cc))
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def reset_game(self):
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = set()
        self.flagged = set()
        self.mine_positions = set()
        self.first_click = True
        self.game_over = False
        self.status_var.set("左键翻开，右键插旗")

        for r in range(self.rows):
            for c in range(self.cols):
                btn = self.buttons[r][c]
                btn.config(
                    text="",
                    state="normal",
                    relief="raised",
                    bg="#d9d9d9",
                    fg="black",
                )

    def place_mines(self, safe_r, safe_c):
        forbidden = {(safe_r, safe_c)}
        for nr in range(max(0, safe_r - 1), min(self.rows, safe_r + 2)):
            for nc in range(max(0, safe_c - 1), min(self.cols, safe_c + 2)):
                forbidden.add((nr, nc))

        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols) if (r, c) not in forbidden]
        self.mine_positions = set(random.sample(all_cells, self.mines_count))

        for r, c in self.mine_positions:
            self.board[r][c] = -1
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == -1:
                    continue
                count = 0
                for nr in range(max(0, r - 1), min(self.rows, r + 2)):
                    for nc in range(max(0, c - 1), min(self.cols, c + 2)):
                        if (nr, nc) in self.mine_positions:
                            count += 1
                self.board[r][c] = count

    def on_left_click(self, r, c):
        if self.game_over or (r, c) in self.flagged:
            return

        if self.first_click:
            self.place_mines(r, c)
            self.first_click = False

        if (r, c) in self.mine_positions:
            self.reveal_mines((r, c))
            self.end_game(False)
            return

        self.reveal_cell(r, c)
        if self.check_win():
            self.end_game(True)

    def on_right_click(self, r, c):
        if self.game_over or (r, c) in self.revealed:
            return

        btn = self.buttons[r][c]
        if (r, c) in self.flagged:
            self.flagged.remove((r, c))
            btn.config(text="", fg="black")
        else:
            self.flagged.add((r, c))
            btn.config(text="🚩", fg="red")

    def reveal_cell(self, r, c):
        if (r, c) in self.revealed or (r, c) in self.flagged:
            return

        self.revealed.add((r, c))
        btn = self.buttons[r][c]
        btn.config(relief="sunken", bg="#f0f0f0", state="disabled")

        value = self.board[r][c]
        if value > 0:
            colors = {
                1: "blue",
                2: "green",
                3: "red",
                4: "navy",
                5: "maroon",
                6: "teal",
                7: "black",
                8: "gray",
            }
            btn.config(text=str(value), fg=colors.get(value, "black"))
        elif value == 0:
            btn.config(text="")
            for nr in range(max(0, r - 1), min(self.rows, r + 2)):
                for nc in range(max(0, c - 1), min(self.cols, c + 2)):
                    if (nr, nc) != (r, c):
                        self.reveal_cell(nr, nc)

    def reveal_mines(self, exploded_cell):
        for r, c in self.mine_positions:
            btn = self.buttons[r][c]
            btn.config(text="💣", fg="black", bg="#ffb3b3", relief="sunken")
        er, ec = exploded_cell
        self.buttons[er][ec].config(bg="#ff6666")

    def check_win(self):
        safe_cells = self.rows * self.cols - self.mines_count
        return len(self.revealed) >= safe_cells

    def end_game(self, won):
        self.game_over = True
        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].config(state="disabled")
        if won:
            self.status_var.set("你赢了！")
            messagebox.showinfo("扫雷", "恭喜你，成功排雷！")
        else:
            self.status_var.set("游戏结束")
            messagebox.showerror("扫雷", "踩到地雷了！")


if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root, rows=10, cols=10, mines=15)
    root.mainloop()
