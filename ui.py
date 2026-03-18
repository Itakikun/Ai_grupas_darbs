import tkinter as tk
from ai_algorithms import MinimaxAgent, AlphaBetaAgent
from tkinter import scrolledtext
from tkinter import messagebox

from config import (
    WINDOW_TITLE,
    MIN_LENGTH,
    MAX_LENGTH,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_TEXT,
    FONT_SEQUENCE,
    FONT_BUTTON,
    FONT_RESULT
)
from game_logic import GameState
from helpers import validate_length


class GameUI:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)

        # Pilnekrāna logs
        self.root.state("zoomed")

        self.game = None

        self.main_container = tk.Frame(self.root, padx=20, pady=20)
        self.main_container.pack(fill="both", expand=True)

        self.create_start_screen()

    def clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def create_start_screen(self):
        self.clear_main_container()

        header = tk.Frame(self.main_container)
        header.pack(fill="x", pady=(10, 30))

        title_label = tk.Label(header, text="Skaitļu virknes spēle", font=FONT_TITLE)
        title_label.pack()

        description = tk.Label(
            header,
            text=(
                "Ievadi virknes garumu diapazonā no 15 līdz 25.\n"
                "Programma ģenerēs skaitļu virkni no 0 un 1."
            ),
            font=FONT_TEXT,
            justify="center"
        )
        description.pack(pady=10)

        settings_frame = tk.Frame(self.main_container)
        settings_frame.pack(pady=20)

        tk.Label(settings_frame, text="Virknes garums:", font=FONT_TEXT).grid(row=0, column=0, padx=8, pady=8)
        self.length_entry = tk.Entry(settings_frame, font=FONT_TEXT, width=10)
        self.length_entry.grid(row=0, column=1, padx=8, pady=8)

        tk.Label(settings_frame, text="Kurš sāk spēli:", font=FONT_TEXT).grid(row=1, column=0, padx=8, pady=8)

        self.start_player_var = tk.StringVar(value="human")
        start_player_frame = tk.Frame(settings_frame)
        start_player_frame.grid(row=1, column=1, padx=8, pady=8, sticky="w")

        tk.Radiobutton(
            start_player_frame,
            text="Cilvēks",
            variable=self.start_player_var,
            value="human",
            font=FONT_TEXT
        ).pack(side="left", padx=5)

        tk.Radiobutton(
            start_player_frame,
            text="Dators",
            variable=self.start_player_var,
            value="computer",
            font=FONT_TEXT
        ).pack(side="left", padx=5)

        tk.Label(settings_frame, text="Datora algoritms:", font=FONT_TEXT).grid(row=2, column=0, padx=8, pady=8)

        self.algorithm_var = tk.StringVar(value="minimax")
        algorithm_frame = tk.Frame(settings_frame)
        algorithm_frame.grid(row=2, column=1, padx=8, pady=8, sticky="w")

        tk.Radiobutton(
            algorithm_frame,
            text="Minimakss",
            variable=self.algorithm_var,
            value="minimax",
            font=FONT_TEXT
        ).pack(side="left", padx=5)

        tk.Radiobutton(
            algorithm_frame,
            text="Alfa-beta",
            variable=self.algorithm_var,
            value="alphabeta",
            font=FONT_TEXT
        ).pack(side="left", padx=5)

        info_label = tk.Label(
            self.main_container,
            text=(
                "Piezīme: datora algoritmu sadaļa ir sagatavota, "
                "taču pašlaik vēl nav realizēta."
            ),
            font=FONT_TEXT
        )
        info_label.pack(pady=10)

        button_frame = tk.Frame(self.main_container)
        button_frame.pack(pady=20)

        start_button = tk.Button(
            button_frame,
            text="Sākt spēli",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            font=FONT_BUTTON,
            command=self.start_game
        )
        start_button.pack()

        rules_frame = tk.Frame(self.main_container)
        rules_frame.pack(fill="x", pady=30)

        rules_title = tk.Label(rules_frame, text="Spēles noteikumi", font=FONT_SUBTITLE)
        rules_title.pack()

        rules_text = tk.Label(
            rules_frame,
            text=(
                "00 dod 1 un piešķir 1 punktu spēlētājam\n"
                "01 dod 0 un atņem 1 punktu no spēlētāja punktu skaita\n"
                "10 dod 0 un atņem 1 punktu no spēlētāja punktu skaita\n"
                "11 dod 0 un piešķir 1 punktu spēlētājam\n\n"
                "Vienā gājienā drīkst izvēlēties tikai vienu blakus pāri.\n"
                "Spēle beidzas, kad virknē paliek viens skaitlis."
            ),
            font=FONT_TEXT,
            justify="center"
        )
        rules_text.pack(pady=10)

    def start_game(self):
        length_text = self.length_entry.get().strip()
        if not validate_length(length_text, MIN_LENGTH, MAX_LENGTH):
            messagebox.showerror("Kļūda", f"Ievadi veselu skaitli diapazonā no {MIN_LENGTH} līdz {MAX_LENGTH}.")
            return

        length = int(length_text)
        self.game = GameState(length)
        
        # Determine names based on choice
        if self.start_player_var.get() == "computer":
            self.game.player_names = ["Cilvēks", "Dators"]
            self.game.current_player = 1 # Computer is second in logic, but we can set turn
        else:
            self.game.player_names = ["Cilvēks", "Dators"]
            self.game.current_player = 0

        # Initialize the AI Agent
        if self.algorithm_var.get() == "minimax":
            self.ai_agent = MinimaxAgent(depth=3)
        else:
            self.ai_agent = AlphaBetaAgent(depth=5)

        self.create_game_screen()
        
        # If computer is first, trigger it
        if self.game.current_player == 1:
            self.root.after(1000, self.make_ai_move)

    def create_game_screen(self):
        self.clear_main_container()

        top_frame = tk.Frame(self.main_container)
        top_frame.pack(fill="x", pady=(0, 20))

        title_label = tk.Label(top_frame, text="Spēles process", font=FONT_TITLE)
        title_label.pack()

        self.player_label = tk.Label(self.main_container, text="", font=FONT_SUBTITLE)
        self.player_label.pack(pady=8)

        self.score_label = tk.Label(self.main_container, text="", font=FONT_TEXT)
        self.score_label.pack(pady=8)

        self.sequence_label = tk.Label(
            self.main_container,
            text="",
            font=FONT_SEQUENCE,
            wraplength=1400,
            justify="center"
        )
        self.sequence_label.pack(pady=25)

        self.pairs_title = tk.Label(self.main_container, text="", font=FONT_SUBTITLE)
        self.pairs_title.pack(pady=10)

        self.pairs_frame = tk.Frame(self.main_container)
        self.pairs_frame.pack(pady=10)

        self.bottom_frame = tk.Frame(self.main_container)
        self.bottom_frame.pack(side="bottom", pady=20)

        new_game_button = tk.Button(
            self.bottom_frame,
            text="Jauna spēle",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            font=FONT_BUTTON,
            command=self.create_start_screen
        )
        new_game_button.pack(side="left", padx=10)

        exit_button = tk.Button(
            self.bottom_frame,
            text="Iziet",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            font=FONT_BUTTON,
            command=self.root.destroy
        )
        exit_button.pack(side="left", padx=10)

        self.refresh_game_screen()

    def refresh_game_screen(self):
        if self.game.is_game_over():
            self.show_game_over_screen()
            return

        self.player_label.config(text=f"Gājiens: {self.game.get_current_player_name()}")

        scores = self.game.get_scores()
        self.score_label.config(
            text=f"1. spēlētājs: {scores[0]}    |    2. spēlētājs: {scores[1]}"
        )

        self.sequence_label.config(
            text=f"Pašreizējā virkne:\n{self.game.get_sequence_as_text()}"
        )

        for widget in self.pairs_frame.winfo_children():
            widget.destroy()

        self.pairs_title.config(text="Izvēlies blakus esošo pāri")

        pairs = self.game.get_available_pairs()

        max_columns = 8
        row = 0
        col = 0

        for index, pair in pairs:
            button = tk.Button(
                self.pairs_frame,
                text=f"[{index}] {pair}",
                width=BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                font=FONT_BUTTON,
                command=lambda idx=index: self.make_move(idx)
            )
            button.grid(row=row, column=col, padx=6, pady=6)

            col += 1
            if col >= max_columns:
                col = 0
                row += 1

    def make_move(self, index):
        try:
            self.game.apply_move(index)
            self.refresh_game_screen()
            
            # If the game isn't over and it's now the Computer's turn (index 1)
            if not self.game.is_game_over() and self.game.current_player == 1:
                self.root.after(600, self.make_ai_move) # Small delay for realism
        except ValueError as error:
            messagebox.showerror("Kļūda", str(error))

    def make_ai_move(self):
        if self.game.is_game_over(): return
        
        # The AI looks at the state and picks the best index
        best_index = self.ai_agent.choose_move(self.game)
        self.make_move(best_index)

    def show_game_over_screen(self):
        for widget in self.pairs_frame.winfo_children():
            widget.destroy()

        self.pairs_title.config(text="Spēle beigusies! Gājienu vēsture:")

        history_area = scrolledtext.ScrolledText(
            self.pairs_frame, 
            width=90, 
            height=15, 
            font=("Courier New", 10)
        )
        history_area.grid(row=0, column=0, padx=10, pady=10)

        # Header with alignment
        history_text = f"{'Gājiens':<8} | {'Spēlētājs':<12} | {'Izmaiņa':<12} | {'Punkti':<8} | {'Virknes izmaiņa'}\n"
        history_text += "=" * 95 + "\n"
        
        # We need the starting sequence for the very first move's display
        # We can reconstruct it from move_history[0]
        for i, move in enumerate(self.game.move_history):
            # To show what was replaced, we look at the sequence from the PREVIOUS move
            # or the starting sequence if it's the first move.
            if i == 0:
                # Reconstruct initial sequence: take sequence_after and reverse the move
                prev_seq = list(move['sequence_after'])
                prev_seq[move['index']:move['index']+1] = [move['pair'][0], move['pair'][1]]
            else:
                prev_seq = self.game.move_history[i-1]['sequence_after']

            # Highlight the pair being replaced in the "before" string
            seq_before_list = [str(x) for x in prev_seq]
            idx = move['index']
            # Wrap the pair in brackets for highlighting: e.g., 010[11]0 -> 01000
            seq_before_list[idx] = ">>" + seq_before_list[idx]
            seq_before_list[idx+1] = seq_before_list[idx+1] + "<<"
            highlighted_before = "".join(seq_before_list)
            
            after_str = "".join(move['sequence_after'])

            history_text += (
                f"{i+1:<8} | "
                f"{move['player']:<12} | "
                f"'{move['pair']}' -> {move['new_symbol']:<4} | "
                f"{move['score_before']:>2} -> {move['score_after']:>2} | "
                f"{highlighted_before}  =>  {after_str}\n"
            )

        history_area.insert(tk.INSERT, history_text)
        history_area.configure(state='disabled')

        result_label = tk.Label(
            self.pairs_frame,
            text=self.game.get_final_result_text(),
            font=FONT_RESULT
        )
        result_label.grid(row=1, column=0, padx=10, pady=10)