import os
import barcode
from barcode.writer import ImageWriter
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Διαθέσιμοι τύποι barcode
BARCODE_TYPES = {
    "EAN-13": "ean13",
    "Code 128": "code128",
}

# Διαθέσιμες μορφές εξαγωγής
OUTPUT_FORMATS = ["SVG", "EPS", "PNG", "JPEG"]

def generate_barcode():
    code = entry_code.get().strip()
    human_type = combo_type.get().strip()
    export_format = combo_format.get().strip()

    if not code:
        messagebox.showerror("Σφάλμα", "Πληκτρολόγησε έναν κωδικό προϊόντος.")
        return

    if not human_type:
        messagebox.showerror("Σφάλμα", "Επίλεξε τύπο barcode.")
        return

    if export_format not in OUTPUT_FORMATS:
        messagebox.showerror("Σφάλμα", "Επίλεξε μορφή αρχείου.")
        return

    bc_type = BARCODE_TYPES.get(human_type, "ean13")

    # Έλεγχος EAN-13
    if bc_type == "ean13" and not (code.isdigit() and len(code) in (12, 13)):
        messagebox.showerror(
            "Σφάλμα",
            "Για EAN-13 πρέπει ο κωδικός να είναι 12 ή 13 ψηφία (μόνο αριθμοί)."
        )
        return

    # Επιλογή extension
    if export_format == "SVG":
        defext = ".svg"
        ftypes = [("SVG file", "*.svg")]
    elif export_format == "EPS":
        defext = ".eps"
        ftypes = [("EPS file", "*.eps")]
    elif export_format == "PNG":
        defext = ".png"
        ftypes = [("PNG image", "*.png")]
    else:  # JPEG
        defext = ".jpg"
        ftypes = [("JPEG image", "*.jpg")]

    filepath = filedialog.asksaveasfilename(
        title=f"Αποθήκευση barcode ως {export_format}",
        defaultextension=defext,
        filetypes=ftypes
    )

    if not filepath:
        return

    try:
        base, _ = os.path.splitext(filepath)
        bc_class = barcode.get_barcode_class(bc_type)

        # ========================
        # SVG -> default writer
        # ========================
        if export_format == "SVG":
            bc = bc_class(code)
            saved_path = bc.save(base)

        else:
            # ========================
            # EPS / PNG / JPEG μέσω ImageWriter
            # ========================
            writer = ImageWriter()

            # Προσπάθεια χρήσης Arial για ασφάλεια σε όλα τα PC
            win_dir = os.environ.get("WINDIR", r"C:\Windows")
            font_path = os.path.join(win_dir, "Fonts", "arial.ttf")

            options = {}

            if os.path.exists(font_path):
                options["font_path"] = font_path

            # Format override
            if export_format == "EPS":
                options["format"] = "EPS"
            elif export_format == "PNG":
                options["format"] = "PNG"
            elif export_format == "JPEG":
                options["format"] = "JPEG"

            bc = bc_class(code, writer=writer)
            saved_path = bc.save(base, options)

        messagebox.showinfo(
            "Επιτυχία",
            f"Το barcode δημιουργήθηκε και αποθηκεύτηκε ως:\n{saved_path}"
        )

    except Exception as e:
        messagebox.showerror(
            "Σφάλμα",
            f"Παρουσιάστηκε σφάλμα κατά τη δημιουργία του barcode:\n{e}"
        )


# ===================== GUI =====================

root = tk.Tk()
root.title("Barcode Generator")

main_frame = ttk.Frame(root, padding=20)
main_frame.grid(row=0, column=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

label_title = ttk.Label(
    main_frame,
    text="Barcode Generator",
    font=("Segoe UI", 14, "bold")
)
label_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

label_code = ttk.Label(main_frame, text="Κωδικός προϊόντος:")
label_code.grid(row=1, column=0, sticky="w", pady=5)

entry_code = ttk.Entry(main_frame, width=30)
entry_code.grid(row=1, column=1, sticky="ew", pady=5)

label_type = ttk.Label(main_frame, text="Τύπος barcode:")
label_type.grid(row=2, column=0, sticky="w", pady=5)

combo_type = ttk.Combobox(
    main_frame,
    values=list(BARCODE_TYPES.keys()),
    state="readonly",
    width=27
)
combo_type.grid(row=2, column=1, sticky="ew", pady=5)
combo_type.set("EAN-13")

label_format = ttk.Label(main_frame, text="Μορφή αρχείου:")
label_format.grid(row=3, column=0, sticky="w", pady=5)

combo_format = ttk.Combobox(
    main_frame,
    values=OUTPUT_FORMATS,
    state="readonly",
    width=27
)
combo_format.grid(row=3, column=1, sticky="ew", pady=5)
combo_format.set("SVG")

btn_generate = ttk.Button(
    main_frame,
    text="Δημιουργία & Αποθήκευση",
    command=generate_barcode
)
btn_generate.grid(row=4, column=0, columnspan=2, pady=15)

main_frame.columnconfigure(0, weight=0)
main_frame.columnconfigure(1, weight=1)

root.mainloop()
