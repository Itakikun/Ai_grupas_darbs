import random
from config import MIN_LENGTH, MAX_LENGTH


class GameState:
    """
    Glabā vienas spēles stāvokli.
    Šī ir datu struktūra, kurā tiek uzglabāta spēles informācija.
    """

    def __init__(self, length):
        if length < MIN_LENGTH or length > MAX_LENGTH:
            raise ValueError(f"Virknes garumam jābūt no {MIN_LENGTH} līdz {MAX_LENGTH}.")

        self.sequence = self._generate_sequence(length)
        self.player_names = ["1. spēlētājs", "2. spēlētājs"]
        self.scores = [0, 0]
        self.current_player = 0
        self.move_history = []

    def _generate_sequence(self, length):
        """
        Ģenerē 0 un 1 virkni ar vismaz vienu 0 un vienu 1.
        """
        while True:
            seq = [random.choice(["0", "1"]) for _ in range(length)]
            if "0" in seq and "1" in seq:
                return seq

    def get_sequence_as_text(self):
        return " ".join(self.sequence)

    def get_current_player_name(self):
        return self.player_names[self.current_player]

    def get_scores(self):
        return self.scores[:]

    def is_game_over(self):
        return len(self.sequence) == 1

    def get_final_result_text(self):
        if self.scores[0] > self.scores[1]:
            return f"Uzvarēja {self.player_names[0]}!"
        if self.scores[1] > self.scores[0]:
            return f"Uzvarēja {self.player_names[1]}!"
        return "Rezultāts ir neizšķirts!"

    def get_available_pairs(self):
        """
        Atgriež visus blakus pārus.
        Formāts: [(indekss, '01'), (indekss, '11'), ...]
        """
        pairs = []
        for i in range(len(self.sequence) - 1):
            pair = self.sequence[i] + self.sequence[i + 1]
            pairs.append((i, pair))
        return pairs

    def apply_move(self, index):
        """
        Izpilda vienu gājienu, izvēloties blakus pāri pēc indeksa.
        """
        if index < 0 or index >= len(self.sequence) - 1:
            raise ValueError("Nepareizi izvēlēts pāris.")

        left = self.sequence[index]
        right = self.sequence[index + 1]
        pair = left + right

        score_before = self.scores[self.current_player]

        if pair == "00":
            new_symbol = "1"
            self.scores[self.current_player] += 1
        elif pair == "01":
            new_symbol = "0"
            self.scores[self.current_player] -= 1
        elif pair == "10":
            new_symbol = "1"
            self.scores[self.current_player] -= 1
        elif pair == "11":
            new_symbol = "0"
            self.scores[self.current_player] += 1
        else:
            raise ValueError("Nederīgs pāris.")

        self.sequence[index:index + 2] = [new_symbol]

        score_after = self.scores[self.current_player]

        self.move_history.append({
            "player": self.player_names[self.current_player],
            "index": index,
            "pair": pair,
            "new_symbol": new_symbol,
            "score_before": score_before,
            "score_after": score_after,
            "sequence_after": self.sequence[:]
        })

        if not self.is_game_over():
            self.current_player = 1 - self.current_player
