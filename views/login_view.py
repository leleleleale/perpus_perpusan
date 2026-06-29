import tkinter as tk
from tkinter import ttk, messagebox
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models.database import AdminModel, SiswaModel

COLORS = {
    "bg":         "#F0F4F8",
    "sidebar":    "#1A3C5E",
    "sidebar_h":  "#2A5F8F",
    "accent":     "#E8A020",
    "accent_d":   "#C4841A",
    "card":       "#FFFFFF",
    "text":       "#1C2B3A",
    "text_muted": "#6B7E8F",
    "danger":     "#D94040",
    "success":    "#2E9E5E",
    "warning":    "#E07B1A",
    "border":     "#D0DCE8",
    "header":     "#12263D",
    "siswa_clr":  "#2E9E5E",   # hijau untuk mode siswa
    "admin_clr":  "#1A3C5E",   # biru tua untuk mode admin
}

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_HEAD  = ("Segoe UI", 13, "bold")
FONT_BODY  = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)
FONT_LABEL = ("Segoe UI", 10)
FONT_BTN   = ("Segoe UI", 11, "bold")


# ─────────────────────────────────────────────────────────────────
# Layar pemilihan mode (Admin / Siswa)
# ─────────────────────────────────────────────────────────────────
class ModeSelectWindow:
    def __init__(self, root, on_admin, on_siswa):
        self.root = root
        self.on_admin = on_admin
        self.on_siswa = on_siswa

        root.title("Perpustakaan Digital")
        root.resizable(False, False)
        w, h = 500, 420
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        root.configure(bg=COLORS["bg"])
        self._build()

    def _build(self):
        outer = tk.Frame(self.root, bg=COLORS["bg"])
        outer.pack(expand=True, fill="both", padx=40, pady=30)

        # Top stripe
        tk.Frame(outer, bg=COLORS["sidebar"], height=5).pack(fill="x")

        card = tk.Frame(outer, bg=COLORS["card"],
                        highlightbackground=COLORS["border"],
                        highlightthickness=1)
        card.pack(fill="both", expand=True)

        inner = tk.Frame(card, bg=COLORS["card"])
        inner.pack(padx=36, pady=30, fill="both", expand=True)

        tk.Label(inner, text="📚", font=("Segoe UI", 38),
                 bg=COLORS["card"]).pack()
        tk.Label(inner, text="Perpustakaan Digital",
                 font=FONT_TITLE, bg=COLORS["card"],
                 fg=COLORS["sidebar"]).pack(pady=(6, 2))
        tk.Label(inner, text="Buku Pelajaran SD – SMA",
                 font=FONT_SMALL, bg=COLORS["card"],
                 fg=COLORS["text_muted"]).pack(pady=(0, 28))

        tk.Label(inner, text="Masuk sebagai:",
                 font=FONT_LABEL, bg=COLORS["card"],
                 fg=COLORS["text_muted"]).pack(pady=(0, 12))

        # Dua tombol besar
        row = tk.Frame(inner, bg=COLORS["card"])
        row.pack()

        self._mode_btn(row, "🏫\nAdmin", "Kelola buku & siswa",
                       COLORS["admin_clr"], self.on_admin).pack(
            side="left", padx=10)
        self._mode_btn(row, "🎒\nSiswa", "Pinjam & cek buku",
                       COLORS["siswa_clr"], self.on_siswa).pack(
            side="left", padx=10)

    def _mode_btn(self, parent, title, subtitle, color, cmd):
        frame = tk.Frame(parent, bg=color, cursor="hand2",
                         highlightbackground=color,
                         highlightthickness=2)
        frame.bind("<Button-1>", lambda e: cmd())

        inner = tk.Frame(frame, bg=color)
        inner.pack(padx=22, pady=18)
        inner.bind("<Button-1>", lambda e: cmd())

        lbl_t = tk.Label(inner, text=title, font=("Segoe UI", 14, "bold"),
                         bg=color, fg="#FFFFFF", justify="center")
        lbl_t.pack()
        lbl_t.bind("<Button-1>", lambda e: cmd())

        lbl_s = tk.Label(inner, text=subtitle, font=FONT_SMALL,
                         bg=color, fg="#CCDDCC", justify="center")
        lbl_s.pack(pady=(4, 0))
        lbl_s.bind("<Button-1>", lambda e: cmd())

        # Hover effect
        def on_enter(e):
            darker = self._darken(color)
            for w in [frame, inner, lbl_t, lbl_s]:
                w.configure(bg=darker)
        def on_leave(e):
            for w in [frame, inner, lbl_t, lbl_s]:
                w.configure(bg=color)
        for w in [frame, inner, lbl_t, lbl_s]:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)

        return frame

    def _darken(self, hex_color):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        r = max(0, r - 30)
        g = max(0, g - 30)
        b = max(0, b - 30)
        return f"#{r:02x}{g:02x}{b:02x}"


# ─────────────────────────────────────────────────────────────────
# Login Admin (username + password)
# ─────────────────────────────────────────────────────────────────
class LoginWindow:
    def __init__(self, root, on_success, on_back=None):
        self.root = root
        self.on_success = on_success
        self.on_back = on_back

        root.title("Login Admin – Perpustakaan Digital")
        root.resizable(False, False)
        w, h = 440, 500
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        root.configure(bg=COLORS["bg"])
        self._build()

    def _build(self):
        outer = tk.Frame(self.root, bg=COLORS["bg"])
        outer.pack(expand=True, fill="both", padx=40, pady=30)

        tk.Frame(outer, bg=COLORS["sidebar"], height=5).pack(fill="x")
        card = tk.Frame(outer, bg=COLORS["card"],
                        highlightbackground=COLORS["border"],
                        highlightthickness=1)
        card.pack(fill="both", expand=True)

        inner = tk.Frame(card, bg=COLORS["card"])
        inner.pack(padx=36, pady=32, fill="both", expand=True)

        tk.Label(inner, text="🏫", font=("Segoe UI", 36),
                 bg=COLORS["card"]).pack()
        tk.Label(inner, text="Login Admin",
                 font=FONT_TITLE, bg=COLORS["card"],
                 fg=COLORS["sidebar"]).pack(pady=(6, 2))
        tk.Label(inner, text="Masukkan username dan password",
                 font=FONT_SMALL, bg=COLORS["card"],
                 fg=COLORS["text_muted"]).pack(pady=(0, 22))

        for label, attr, show in [
            ("Username", "ent_user", None),
            ("Password", "ent_pw",   "•"),
        ]:
            tk.Label(inner, text=label, font=FONT_LABEL,
                     bg=COLORS["card"], fg=COLORS["text"],
                     anchor="w").pack(fill="x")
            ent = tk.Entry(inner, font=FONT_BODY,
                           relief="flat", bd=0,
                           highlightthickness=1,
                           highlightbackground=COLORS["border"],
                           highlightcolor=COLORS["accent"],
                           show=show or "")
            ent.pack(fill="x", ipady=8, pady=(2, 12))
            setattr(self, attr, ent)

        tk.Button(inner, text="Masuk", command=self._login,
                  bg=COLORS["admin_clr"], fg="#fff",
                  activebackground=COLORS["sidebar_h"],
                  activeforeground="#fff",
                  font=FONT_BTN, relief="flat", cursor="hand2",
                  pady=9).pack(fill="x", pady=(6, 0))

        if self.on_back:
            tk.Button(inner, text="← Kembali", command=self.on_back,
                      bg=COLORS["card"], fg=COLORS["text_muted"],
                      activebackground=COLORS["border"],
                      font=FONT_SMALL, relief="flat", cursor="hand2",
                      pady=4).pack(fill="x", pady=(8, 0))

        tk.Label(inner, text="Default: admin / admin123",
                 font=FONT_SMALL, bg=COLORS["card"],
                 fg=COLORS["text_muted"]).pack(pady=(10, 0))

        self.ent_user.focus()
        self.root.bind("<Return>", lambda e: self._login())

    def _login(self):
        u = self.ent_user.get().strip()
        p = self.ent_pw.get().strip()
        if not u or not p:
            messagebox.showwarning("Login", "Isi username dan password!")
            return
        admin = AdminModel.login(u, p)
        if admin:
            self.on_success(admin)
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah.")
            self.ent_pw.delete(0, "end")
            self.ent_pw.focus()


# ─────────────────────────────────────────────────────────────────
# Login Siswa (nama saja, tanpa password)
# ─────────────────────────────────────────────────────────────────
class LoginSiswaWindow:
    def __init__(self, root, on_success, on_back=None):
        self.root = root
        self.on_success = on_success
        self.on_back = on_back
        self._hasil = []   # list siswa yang cocok (jika >1 nama sama)

        root.title("Login Siswa – Perpustakaan Digital")
        root.resizable(False, False)
        w, h = 460, 500
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        root.configure(bg=COLORS["bg"])
        self._build()

    def _build(self):
        outer = tk.Frame(self.root, bg=COLORS["bg"])
        outer.pack(expand=True, fill="both", padx=40, pady=30)

        tk.Frame(outer, bg=COLORS["siswa_clr"], height=5).pack(fill="x")
        card = tk.Frame(outer, bg=COLORS["card"],
                        highlightbackground=COLORS["border"],
                        highlightthickness=1)
        card.pack(fill="both", expand=True)

        inner = tk.Frame(card, bg=COLORS["card"])
        inner.pack(padx=36, pady=32, fill="both", expand=True)

        tk.Label(inner, text="🎒", font=("Segoe UI", 36),
                 bg=COLORS["card"]).pack()
        tk.Label(inner, text="Login Siswa",
                 font=FONT_TITLE, bg=COLORS["card"],
                 fg=COLORS["siswa_clr"]).pack(pady=(6, 2))
        tk.Label(inner, text="Ketik namamu untuk masuk",
                 font=FONT_SMALL, bg=COLORS["card"],
                 fg=COLORS["text_muted"]).pack(pady=(0, 22))

        tk.Label(inner, text="Nama Lengkap", font=FONT_LABEL,
                 bg=COLORS["card"], fg=COLORS["text"],
                 anchor="w").pack(fill="x")
        self.ent_nama = tk.Entry(inner, font=FONT_BODY,
                                  relief="flat", bd=0,
                                  highlightthickness=1,
                                  highlightbackground=COLORS["border"],
                                  highlightcolor=COLORS["siswa_clr"])
        self.ent_nama.pack(fill="x", ipady=8, pady=(2, 6))
        self.ent_nama.bind("<KeyRelease>", self._on_type)

        # Dropdown muncul jika ada >1 hasil dengan nama yang sama
        self.v_pilih = tk.StringVar()
        self.cb_pilih = ttk.Combobox(inner, textvariable=self.v_pilih,
                                      state="readonly", font=FONT_BODY)
        # Disembunyikan dulu, muncul kalau ada ambiguitas nama

        self.lbl_hint = tk.Label(inner, text="",
                                  font=FONT_SMALL, bg=COLORS["card"],
                                  fg=COLORS["text_muted"], anchor="w",
                                  wraplength=340)
        self.lbl_hint.pack(fill="x", pady=(2, 14))

        tk.Button(inner, text="Masuk", command=self._login,
                  bg=COLORS["siswa_clr"], fg="#fff",
                  activebackground="#247A4A",
                  activeforeground="#fff",
                  font=FONT_BTN, relief="flat", cursor="hand2",
                  pady=9).pack(fill="x")

        if self.on_back:
            tk.Button(inner, text="← Kembali", command=self.on_back,
                      bg=COLORS["card"], fg=COLORS["text_muted"],
                      activebackground=COLORS["border"],
                      font=FONT_SMALL, relief="flat", cursor="hand2",
                      pady=4).pack(fill="x", pady=(8, 0))

        tk.Label(inner, text="Nama harus sesuai dengan yang didaftarkan admin.",
                 font=FONT_SMALL, bg=COLORS["card"],
                 fg=COLORS["text_muted"]).pack(pady=(12, 0))

        self.ent_nama.focus()
        self.root.bind("<Return>", lambda e: self._login())

    def _on_type(self, e=None):
        nama = self.ent_nama.get().strip()
        if not nama:
            self._hasil = []
            self.cb_pilih.pack_forget()
            self.lbl_hint.configure(text="")
            return

        self._hasil = SiswaModel.login_by_nama(nama)
        if len(self._hasil) > 1:
            # Tampilkan combobox pilih jika nama ganda
            opts = [f"{s['nama']} – {s['jenjang']} {s['kelas']} (NIS: {s['nis']})"
                    for s in self._hasil]
            self.cb_pilih.configure(values=opts)
            self.cb_pilih.current(0)
            self.cb_pilih.pack(fill="x", pady=(0, 8))
            self.lbl_hint.configure(
                text=f"Ditemukan {len(self._hasil)} siswa dengan nama ini. Pilih yang sesuai.",
                fg=COLORS["warning"])
        else:
            self.cb_pilih.pack_forget()
            if len(self._hasil) == 1:
                s = self._hasil[0]
                self.lbl_hint.configure(
                    text=f"✓  {s['jenjang']} {s['kelas']}  |  NIS: {s['nis']}",
                    fg=COLORS["success"])
            else:
                self.lbl_hint.configure(text="Nama tidak ditemukan di sistem.",
                                         fg=COLORS["danger"])

    def _login(self):
        nama = self.ent_nama.get().strip()
        if not nama:
            messagebox.showwarning("Login", "Ketik namamu terlebih dahulu!")
            return

        if not self._hasil:
            messagebox.showerror("Login Gagal",
                                  "Namamu belum terdaftar di perpustakaan.\n"
                                  "Minta admin untuk mendaftarkan namamu terlebih dahulu.")
            return

        if len(self._hasil) > 1:
            idx = self.cb_pilih.current()
            if idx < 0:
                messagebox.showwarning("Pilih Akun",
                                        "Ada beberapa siswa dengan nama yang sama.\n"
                                        "Pilih akunmu dari daftar yang tersedia.")
                return
            siswa = self._hasil[idx]
        else:
            siswa = self._hasil[0]

        self.on_success(siswa)
