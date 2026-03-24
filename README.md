# Python Scientific Calculator (PySide6 GUI)

Aplikasi **scientific calculator modern** berbasis **PySide6** dengan tema dark, tampilan clean, dan kontrol yang mudah.

## Fitur utama
- UI modern + dark theme
- Evaluasi ekspresi aman (AST allowlist, tanpa `eval` bebas)
- Tombol fungsi scientific yang lengkap (sin/cos/tan/log/sqrt/exp/factorial/dll)
- Keyboard-friendly: Enter untuk hitung, Backspace untuk hapus, Esc untuk clear
- Riwayat perhitungan (double click untuk pakai ulang ekspresi)

## Install dependency
```bash
python3 -m pip install PySide6
```

## Menjalankan aplikasi GUI
```bash
python3 scientific_calculator_gui.py
```

## Menjalankan tes evaluator
```bash
python3 -m unittest -v
```

## Contoh ekspresi
- `sin(pi/2)`
- `sqrt(49) + log(100, 10)`
- `2**10 + factorial(4)`
