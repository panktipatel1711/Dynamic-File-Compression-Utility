import os
import sys
import argparse
import time
from colorama import init, Fore, Style
from tabulate import tabulate

import tkinter as tk
from tkinter import font

# Core engine module bindings
from src.compress import execute_compression
from src.verify import execute_decompression, verify_checksum_integrity

init(autoreset=True)

def initialize_workspace_directories():
    """Ensures all repository folders exist."""
    for folder in ["input_files", "compressed_files", "decompressed_files", "outputs", "images", "docs"]:
        os.makedirs(folder, exist_ok=True)

def print_cli_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}====================================================================
 ⚡ DYNAMIC FILE COMPRESSION UTILITY (DFC ENGINE) v1.0.0 ⚡
===================================================================={Style.RESET_ALL}"""
    print(banner)

def generate_and_save_mockup_card(command_text, log_lines, output_filename="mockup_capture"):
    """
    Renders a code mockup card centered on a gorgeous dark blue radial gradient
    inspired directly by the official Gemini UI backdrop.
    """
    root = tk.Tk()
    root.title("DFC Studio - Gemini Blue Aesthetic Console")
    
    # Wide layout tailored perfectly for code showcase images
    w, h = 820, 440
    root.geometry(f"{w}x{h}")
    root.resizable(True, True)  # Fully resizable and maximizable!
    
    # Base dark background color mapping
    base_bg = "#080810"
    root.configure(bg=base_bg)
    root.attributes("-topmost", True)

    canvas = tk.Canvas(root, bg=base_bg, bd=0, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    def draw_ui_elements(event=None):
        """Redraws the layout dynamically whenever the window size changes."""
        canvas.delete("all")
        cw = canvas.winfo_width() if canvas.winfo_width() > 1 else w
        ch = canvas.winfo_height() if canvas.winfo_height() > 1 else h

        # 1. Generate the Gemini Deep Blue Aura / Radial Glow Effect
        # Fills the background with a deep blue base
        canvas.create_rectangle(0, 0, cw, ch, fill="#08070c", outline="", width=0)
        
        # Simulates a soft radial blue ambient light emitting from the bottom center
        center_x = cw // 2
        center_y = ch
        max_radius = max(cw, ch)
        steps = 45  # Iteration count for a silky smooth color transition
        
        for i in range(steps, 0, -1):
            ratio = i / steps
            # Transition color values from rich navy blue to solid near-black
            r = int(8 + (12 * (1 - ratio)))
            g = int(12 + (20 * (1 - ratio)))
            b = int(28 + (65 * (1 - ratio)))
            color_hex = f"#{r:02x}{g:02x}{b:02x}"
            
            radius = max_radius * ratio
            canvas.create_oval(
                center_x - radius, center_y - (radius * 0.7),
                center_x + radius, center_y + (radius * 0.7),
                fill=color_hex, outline="", width=0
            )

        # 2. Render the Main Terminal Container Card (The Inside Code Box)
        # Deep matte black window box contrasting against the blue glow
        card_w, card_h = int(cw * 0.85), int(ch * 0.62)
        card_x1 = (cw - card_w) // 2
        card_y1 = (ch - card_h) // 2
        card_x2, card_y2 = card_x1 + card_w, card_y1 + card_h

        canvas.create_rectangle(card_x1, card_y1, card_x2, card_y2, fill="#131314", outline="", width=0)

        # 3. Render Mac-Style Control Bar & Window Dots
        bar_h = 32
        canvas.create_rectangle(card_x1, card_y1, card_x2, card_y1 + bar_h, fill="#1e1e1f", outline="", width=0)

        # Draw Window Decorative Controls (Red, Yellow, Green circles)
        dots = [("#ff5f56", 16), ("#ffbd2e", 32), ("#27c93f", 48)]
        for color, offset in dots:
            cx = card_x1 + offset
            cy = card_y1 + (bar_h // 2)
            canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill=color, outline="")

        # Window header moniker
        canvas.create_text(card_x1 + (card_w // 2), card_y1 + (bar_h // 2), 
                           text="dfc-production-metrics", fill="#8e918f", font=("Consolas", 9, "bold"))

        # 4. Inject Console Text Log Stream
        text_x = card_x1 + 25
        text_y = card_y1 + bar_h + 25

        # Command Line Code Prompt Row
        canvas.create_text(text_x, text_y, text=f"python {command_text}", fill="#e3e3e3", 
                           font=("Consolas", 11, "bold"), anchor="w")
        
        # Performance Analytics Logs Grid Rows
        current_y = text_y + 30
        for label, val, is_highlight in log_lines:
            val_color = "#34a853" if is_highlight else "#c4c7c5"
            
            # Draw Structured Metric Labels
            canvas.create_text(text_x, current_y, text=label, fill="#8e918f", font=("Consolas", 10, "bold"), anchor="w")
            # Draw Structured Data Values next to keys
            canvas.create_text(text_x + 240, current_y, text=val, fill=val_color, font=("Consolas", 10, "bold"), anchor="w")
            current_y += 22

    # Bind the resize configure event to adapt color layers dynamically on screen expansion
    canvas.bind("<Configure>", draw_ui_elements)

    def export_canvas_to_portfolio():
        """Saves out the custom vector blueprint file smoothly to your workspace disk."""
        output_path = os.path.join("images", f"{output_filename}.ps")
        canvas.postscript(file=output_path, colormode="color", width=root.winfo_width(), height=root.winfo_height())
        print(f"{Fore.GREEN}[+] Gemini dark blue ambient mockup saved to: {output_path}")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", export_canvas_to_portfolio)
    root.mainloop()

def main():
    initialize_workspace_directories()
    print_cli_banner()
    
    parser = argparse.ArgumentParser(prog="dfc")
    subparsers = parser.add_subparsers(dest="command")

    c_parser = subparsers.add_parser("compress")
    c_parser.add_argument("path")
    c_parser.add_argument("--mode", choices=["auto", "fast", "max", "huffman"], default="auto")

    d_parser = subparsers.add_parser("decompress")
    d_parser.add_argument("path")

    v_parser = subparsers.add_parser("verify")
    v_parser.add_argument("manifest")

    args = parser.parse_args()

    if args.command == "compress":
        print(f"{Fore.YELLOW}[*] Executing dataset compression sequence...")
        try:
            m = execute_compression(args.path, mode=args.mode)
            cmd_text = f"main.py compress {args.path} --mode={args.mode}"
            logs = [
                ["Allocated Codec Stream ", f": {m['codec'].upper()} (Level {m['level']})", False],
                ["Original Payload Size  ", f": {m['orig_bytes']:,} Bytes", False],
                ["Compressed Output Target", f": {m['out_bytes']:,} Bytes", False],
                ["INTEGRITY CONSOLE METRIC", f": {m['ratio']}x EFFICIENCY RATIO", True]
            ]
            generate_and_save_mockup_card(cmd_text, logs, "gemini_blue_compression_card")
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {e}")

    elif args.command == "decompress":
        print(f"{Fore.YELLOW}[*] Triggering algorithmic file restoration...")
        try:
            execute_decompression(args.path)
            cmd_text = f"main.py decompress {args.path}"
            logs = [
                ["Target Extraction File ", f": {os.path.basename(args.path)}", False],
                ["Decompression Engine   ", f": Lossless Pipeline Decode Build", False],
                ["INTEGRITY RESTORE STATE ", f": COMPLETED SAFELY", True]
            ]
            generate_and_save_mockup_card(cmd_text, logs, "gemini_blue_decompression_card")
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {e}")

    elif args.command == "verify":
        print(f"{Fore.YELLOW}[*] Auditing checksum verification loops...")
        cmd_text = f"main.py verify --manifest {args.manifest}"
        if verify_checksum_integrity(args.manifest):
            logs = [
                ["Target Audit Manifest  ", f": {os.path.basename(args.manifest)}", False],
                ["Extraction Stream Audit ", f": Checksum Integrity Sequence Initialized", False],
                ["INTEGRITY HASH CHECK    ", f": PASSED (SHA-256 MATCH)", True]
            ]
            generate_and_save_mockup_card(cmd_text, logs, "gemini_blue_verification_passed_card")
        else:
            logs = [["INTEGRITY HASH CHECK    ", f": FAILED / DATA CORRUPTED", True]]
            generate_and_save_mockup_card(cmd_text, logs, "gemini_blue_verification_failed_card")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()