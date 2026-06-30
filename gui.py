import tkinter as tk
from tkinter import ttk
from constants import steamIds
from helpers import calculate_winrate, calculate_average_leetify_rating, calculate_score, calculate_stats
import sv_ttk

def make_gui():
    root = tk.Tk()
    root.title("Interface")
    root.geometry("1280x720")

    sv_ttk.set_theme("dark")

    main = ttk.Frame(root, padding=10)
    main.pack(fill="both", expand=True)

    left = ttk.Frame(main)
    left.pack(side="left", fill="y", padx=10)

    right = ttk.Frame(main)
    right.pack(side="right", fill="both", expand=True)

    title = ttk.Label(left, text="Active Players", font=("Consolas", 12))
    title.pack(pady=10)

    player_vars = {name: tk.BooleanVar(value=False) for name in steamIds}

    def run_calculation():
        active_players = {
            steamIds[name]
            for name, var in player_vars.items()
            if var.get()
        }

        results = calculate_stats(active_players)
        render(results)

    def on_toggle():
        run_calculation()

    for name in steamIds:
        ttk.Checkbutton(
            left,
            text=name,
            variable=player_vars[name],
            command=on_toggle
        ).pack(anchor="w")

    summary = ttk.Label(right, text="Results", font=("Consolas", 12))
    summary.pack(anchor="w")

    best_map_label = ttk.Label(right, text="", font=("Consolas", 12))
    best_map_label.pack(anchor="w", pady=10)

    text_frame = ttk.Frame(right)
    text_frame.pack(fill="both", expand=True)

    output = tk.Text(text_frame, wrap="none", font=("Consolas", 18))
    output.pack(fill="both", expand=True)

    def render(results):
        output.config(state="normal")
        output.delete("1.0", tk.END)

        for map_name, stats in results.items():
            winrate = calculate_winrate(stats) * 100
            rating = calculate_average_leetify_rating(stats)
            score = calculate_score(stats)

            output.insert(
                tk.END,
                f"{map_name:<12} | "
                f"{'WinRate:':<8} {winrate:>6.2f}% | "
                f"{'Rating:':<8} {rating:>6.2f} | "
                f"{'Games:':<4} {stats['games']:>6} | "
                f"{'Score:':<8} {score:>6.2f}\n"
            )
        output.config(state="disabled")

    run_calculation()
    root.mainloop()