import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
from tkinter import filedialog
import time

from click import command

from Ida_algorithm import *

class NPuzzleGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.timer_after_id = None
        self.small_img = None
        self.img_label = None
        self.board_size_var = None
        self.game_frame = None
        self.img_table = None
        self.tile_images_map = None
        self.title("N-Puzzle Game")
        self.geometry("900x600")
        self.configure(bg="white")
        self.board_size = 3
        self.tile_size = 100
        self.image_path = "images/img.png"
        self.tiles = []
        self.blank_pos = (2, 2)
        self.show_numbers = tk.BooleanVar(value=False)
        self.board_state = []
        self.build_ui()
        self.heuristic="manhattan"


    def change_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])

        if path:
            self.image_path = path
            self.load_image_tiles()
            try:
                img = Image.open(self.image_path).resize((250, 250))
                self.small_img = ImageTk.PhotoImage(img)

                for widget in self.image_frame.winfo_children():
                    widget.destroy()

                tk.Label(self.image_frame, text="Ảnh gốc", bg="white").pack()
                self.img_label = tk.Label(self.image_frame, image=self.small_img, bg="white")
                self.img_label.pack(pady=5)

            except:
                for widget in self.image_frame.winfo_children():
                    widget.destroy()
                tk.Label(self.image_frame, text="[Không có ảnh]", bg="white").pack()
            self.draw_board()
            self.new_game()


    def build_ui(self):

        outer_left_frame = tk.Frame(self, bg="white")
        outer_left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        control_frame = tk.LabelFrame(outer_left_frame, text="Các lựa chọn", padx=10, pady=10, bg="white")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.time_elapsed = 0
        self.timer_running = False
        self.timer_label = tk.Label(outer_left_frame, text="🕒 Thời gian: 0 giây", bg="white",
                                    font=("Arial", 10, "bold"))
        self.timer_label.pack(side=tk.RIGHT, anchor="n", padx=(10, 0), pady=(5, 0))

        self.board_size_var = self.add_radio_section(control_frame, "Board size", ["3x3", "4x4"])

        self.heuristic_var = self.add_radio_section(control_frame, "Heuristic",
                                                    ["manhattan", "misplaced", "linear_conflict", "diagonal","euclidean","custom"])

        tk.Label(control_frame, text="Kích thước ô:", bg="white").pack(pady=(10, 0))
        self.tile_size_var = tk.IntVar(value=120)
        tile_size_combo = ttk.Combobox(control_frame, textvariable=self.tile_size_var,
                                       values=[60, 80, 100, 120, 150], state="readonly")
        tile_size_combo.bind("<<ComboboxSelected>>", lambda e: self.draw_board())

        tile_size_combo.pack()

        show_numbers_checkbox = ttk.Checkbutton(control_frame, text="Hiển thị số thứ tự", variable=self.show_numbers, command=self.draw_board)

        show_numbers_checkbox.pack(pady=5)

        bottom_frame = tk.LabelFrame(control_frame, text="Lịch sử trạng thái", bg="white")
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 5))

        self.output = tk.Text(bottom_frame, wrap="word", height=12, width=28)
        self.output.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        solution_frame = tk.LabelFrame(control_frame, text="Lời giải", bg="white")
        solution_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 5))

        self.solution_entry = tk.Text(solution_frame, height=3, width=28, wrap="word")
        self.solution_entry.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        tk.Label(control_frame, text="", bg="white").pack(expand=True)
        ttk.Button(control_frame, text="Đổi ảnh", command=self.change_image).pack(pady=5, fill=tk.X)
        ttk.Button(control_frame, text="Ván mới", command=self.new_game).pack(pady=5, fill=tk.X)
        ttk.Button(control_frame, text="Giải tự động", command=self.solve).pack(pady=5, fill=tk.X)

        self.game_frame = tk.Frame(self, bg="white")
        self.game_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.game_frame, text="Khung hình chính", bg="white", font=("Arial", 10, "bold")).pack()
        self.canvas = tk.Canvas(self.game_frame, width=400, height=400, bg="white",
                                highlightbackground="green", highlightthickness=2)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.image_frame = tk.Frame(self.game_frame, bg="white")
        self.image_frame.pack()
        self.state("zoomed")

        self.img_label = None

        try:
            img = Image.open(self.image_path).resize((250, 250))
            self.small_img = ImageTk.PhotoImage(img)
            tk.Label(self.image_frame, text="Ảnh gốc", bg="white").pack()
            self.img_label = tk.Label(self.image_frame, image=self.small_img, bg="white")
            self.img_label.pack(pady=5)
        except:
            tk.Label(self.image_frame, text="[Không có ảnh]", bg="white").pack()


    def update_timer(self):
        if self.timer_running:
            minutes = self.time_elapsed // 60
            seconds = self.time_elapsed % 60
            self.timer_label.config(text=f"Thời gian: {minutes:02}:{seconds:02}")
            self.time_elapsed += 1
            self.timer_after_id = self.after(1000, self.update_timer)

    def add_radio_section(self, parent, title, options):
        section = tk.LabelFrame(parent, text=title, bg="white")
        section.pack(fill=tk.X, pady=5)
        var = tk.StringVar()
        var.set(options[0] if "3x3" in options else options[0])
        for opt in options:
            ttk.Radiobutton(section, text=opt, variable=var, value=opt).pack(anchor="w")
        return var

    def on_heuristic_change(self):
        print(self.heuristic_var.get())


    def new_game(self):
        self.output.delete('1.0', tk.END)

        if self.timer_after_id:
            self.after_cancel(self.timer_after_id)
            self.timer_after_id = None

        self.timer_running = False
        self.time_elapsed = 0

        size_str = self.board_size_var.get()
        self.board_size = int(size_str.split('x')[0])
        self.tile_size = self.tile_size_var.get()
        self.canvas.config(width=self.tile_size * self.board_size, height=self.tile_size * self.board_size)
        self.load_image_tiles()
        self.initialize_state()
        self.shuffle_tiles()
        self.draw_board()

        self.output.insert(tk.END,
                           f"Tạo bàn mới {self.board_size}x{self.board_size} - kích thước ô {self.tile_size}px\n")
        self.output.see(tk.END)

        self.timer_running = True
        self.update_timer()

    def initialize_state(self):
        self.board_state = []
        number = 1
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                if (i, j) == (self.board_size - 1, self.board_size - 1):
                    row.append(None)
                else:
                    row.append(number)
                    number += 1
            self.board_state.append(row)

    def load_image_tiles(self):
        try:
            image = Image.open(self.image_path).resize((self.board_size * self.tile_size, self.board_size * self.tile_size))
            self.tiles = []
            for i in range(self.board_size):
                row = []
                for j in range(self.board_size):
                    if (i, j) == (self.board_size - 1, self.board_size - 1):
                        row.append(None)
                        continue
                    box = (j * self.tile_size, i * self.tile_size, (j + 1) * self.tile_size, (i + 1) * self.tile_size)
                    tile_img = ImageTk.PhotoImage(image.crop(box))
                    row.append(tile_img)
                self.tiles.append(row)
            self.blank_pos = (self.board_size - 1, self.board_size - 1)
        except Exception as e:
            self.output.insert(tk.END, f"Lỗi khi tải ảnh: {e}\n")
        self.tile_images_map = {}
        num = 1
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.tiles[i][j] is not None:
                    self.tile_images_map[num] = self.tiles[i][j]
                    num += 1

    def shuffle_tiles(self):
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for _ in range(100):
            r, c = self.blank_pos
            random.shuffle(moves)
            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                    self.tiles[r][c], self.tiles[nr][nc] = self.tiles[nr][nc], self.tiles[r][c]
                    self.board_state[r][c], self.board_state[nr][nc] = self.board_state[nr][nc], self.board_state[r][c]
                    self.blank_pos = (nr, nc)
                    break

    def draw_board(self):
        self.canvas.delete("all")

        for i in range(self.board_size):
            for j in range(self.board_size):
                tile = self.tiles[i][j]
                x0, y0 = j * self.tile_size, i * self.tile_size
                if tile:
                    self.canvas.create_image(x0, y0, anchor="nw", image=tile)
                    if self.show_numbers.get():
                        number = self.board_state[i][j]
                        self.canvas.create_text(
                            x0 + self.tile_size // 2,
                            y0 + self.tile_size // 2,
                            text=str(number),
                            font=("Arial", 12, "bold"),
                            fill="red"
                        )
                else:
                    self.canvas.create_rectangle(
                        x0, y0, x0 + self.tile_size, y0 + self.tile_size, fill="green"
                    )

    def is_solved(self):
        expected = list(range(1, self.board_size * self.board_size)) + [None]
        flat_state = [num for row in self.board_state for num in row]
        self.timer_running = False
        return flat_state == expected

    def on_canvas_click(self, event):
        row, col = event.y // self.tile_size, event.x // self.tile_size
        br, bc = self.blank_pos
        if abs(row - br) + abs(col - bc) == 1:
            self.tiles[br][bc], self.tiles[row][col] = self.tiles[row][col], self.tiles[br][bc]
            self.board_state[br][bc], self.board_state[row][col] = self.board_state[row][col], self.board_state[br][bc]
            self.blank_pos = (row, col)
            self.draw_board()
            self.output.insert(tk.END, f"Di chuyển ô ({row},{col})\n")
            self.output.see(tk.END)

            if self.is_solved():
                messagebox.showinfo("Chúc mừng!", "Bạn đã giải thành công N-Puzzle!")

    def solve(self):
        self.heuristic = self.heuristic_var.get()
        self.output.insert(tk.END, "Đang giải...\n")
        self.output.update()
        start = time.time()
        path = ida_star(self)
        end = time.time()
        self.timer_running = False

        if path:
            self.output.insert(
                tk.END,
                f"Đã tìm thấy lời giải cho heuristic {self.heuristic} trong {len(path)} bước, mất {end - start:.2f}s\n"
            )
            self.output.update()

            choice = messagebox.askyesnocancel(
                "Lựa chọn hiển thị",
                f"Đã tìm thấy lời giải cho heuristic {self.heuristic} trong {len(path)} bước.\n\n"
                "Yes: Hiển thị lời giải bằng hoạt ảnh\n"
                "No: Chỉ in ra các bước di chuyển\n"
                "Cancel: Không hiển thị gì cả"
            )

            if choice is True:  # Yes
                self.animate_solution(path)
                self.show_solution_steps(path)
            elif choice is False:  # No
                self.show_solution_steps(path)

        else:
            self.output.insert(tk.END, f"Không tìm thấy lời giải cho heuristic {self.heuristic}.\n")

        self.output.see(tk.END)

    def show_solution_steps(self, path):
        self.solution_entry.delete(1.0, tk.END)
        path = [self.board_state] + path
        for i in range(1, len(path)):
            prev = path[i - 1]
            curr = path[i]
            moved_tile = None

            for r in range(self.board_size):
                for c in range(self.board_size):
                    if prev[r][c] != curr[r][c]:
                        if prev[r][c] is None:
                            moved_tile = curr[r][c]
                        elif curr[r][c] is None:
                            moved_tile = prev[r][c]
                        break
                if moved_tile is not None:
                    break

            self.solution_entry.insert(tk.END, f"{i}. {moved_tile}\n")
            self.solution_entry.update()
            self.solution_entry.see(tk.END)

    def animate_solution(self, path):
        def do_step(i):
            if i >= len(path):
                messagebox.showinfo("Hoàn thành", "Đã giải xong!")
                return
            self.board_state = path[i]
            self.sync_tiles_with_state()
            self.tiles = self.board_to_tiles(path[i])
            self.draw_board()
            self.after(300, lambda: do_step(i + 1))

        do_step(0)

    def board_to_tiles(self, state):
        tiles = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                val = state[i][j]
                if val is None:
                    row.append(None)
                else:
                    row.append(self.tile_images_map[val])
            tiles.append(row)
        return tiles

    def sync_tiles_with_state(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board_state[i][j] is None:
                    self.blank_pos = (i, j)


if __name__ == "__main__":
    app = NPuzzleGUI()
    app.new_game()
    app.mainloop()
