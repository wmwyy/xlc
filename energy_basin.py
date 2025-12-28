"""消力池计算 GUI（tkinter 版，无外部依赖）。

公式来源：附录 B.1，计算 h_c、h_c''、ΔZ、d、L_j、L_sj。
改用 tkinter，避免 PyQt6 安装在 32 位 Python 3.13 上缺轮子的问题。
"""

import math
import tkinter as tk
from tkinter import messagebox


def cbrt(x: float) -> float:
    """Cubic root that preserves sign."""
    return math.copysign(abs(x) ** (1.0 / 3.0), x)


def solve_cubic(a: float, b: float, c: float, d: float):
    """Solve x^3 + a x^2 + b x + d = 0; return real roots."""
    p = b - (a * a) / 3.0
    q = (2 * a ** 3) / 27.0 - (a * b) / 3.0 + d
    disc = (q / 2.0) ** 2 + (p / 3.0) ** 3
    if disc >= 0:
        sqrt_disc = math.sqrt(disc)
        u = cbrt(-q / 2.0 + sqrt_disc)
        v = cbrt(-q / 2.0 - sqrt_disc)
        return [u + v - a / 3.0]
    r = math.sqrt(-p / 3.0)
    phi = math.acos(-q / (2.0 * r ** 3))
    roots = []
    for k in range(3):
        t = 2.0 * r * math.cos((phi + 2.0 * math.pi * k) / 3.0)
        roots.append(t - a / 3.0)
    return roots


class BasinApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("消力池计算 (tkinter)")
        self.geometry("440x640")

        self.defaults = {
            "sigma0": "1.05",  # 跳跃淹没系数 1.05~1.10
            "alpha": "1.00",   # 动能校正系数 1.0~1.05
            "q": "5.0",        # 单宽流量 m3/s/m
            "b1": "10.0",      # 首端宽度 m
            "b2": "12.0",      # 末端宽度 m
            "T0": "8.0",       # 总势能 m
            "p": "1.0",        # 校正长度参数 m
            "hs": "3.0",       # 出池河床水深 h_s' m
            "Ls": "5.0",       # 斜段水平投影 L_s m
            "beta": "0.75",    # 水跃长度校正 β 0.7~0.8
            "g": "9.81",       # 重力加速度 m/s^2
        }
        self.entries: dict[str, tk.Entry] = {}
        self._build_form()

    def _build_form(self) -> None:
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        fields = [
            ("σ₀ (跳跃淹没系数)", "sigma0"),
            ("α (动能校正系数)", "alpha"),
            ("q (单宽流量 m³/s/m)", "q"),
            ("b₁ (首端宽度 m)", "b1"),
            ("b₂ (末端宽度 m)", "b2"),
            ("T₀ (总势能 m)", "T0"),
            ("p (校正长度参数 m)", "p"),
            ("h′ₛ (出池河床水深 m)", "hs"),
            ("Lₛ (斜段水平投影 m)", "Ls"),
            ("β (水跃长度校正)", "beta"),
            ("g (重力加速度 m/s²)", "g"),
        ]

        for idx, (label, key) in enumerate(fields):
            tk.Label(frame, text=label, anchor="w").grid(row=idx, column=0, sticky="w", pady=4)
            entry = tk.Entry(frame)
            entry.grid(row=idx, column=1, sticky="ew", pady=4)
            entry.insert(0, self.defaults[key])
            self.entries[key] = entry
        frame.columnconfigure(1, weight=1)

        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=8, sticky="ew")
        tk.Button(btn_frame, text="计算", command=self.calculate).pack(side=tk.LEFT, padx=4)
        tk.Button(btn_frame, text="重置", command=self.reset_defaults).pack(side=tk.LEFT, padx=4)

        self.output = tk.Text(frame, height=12, wrap="word", state=tk.DISABLED, bg="#0f172a", fg="#e2e8f0")
        self.output.grid(row=len(fields) + 1, column=0, columnspan=2, sticky="nsew")
        frame.rowconfigure(len(fields) + 1, weight=1)

    def reset_defaults(self) -> None:
        for key, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, self.defaults[key])
        self._set_output("")

    def _set_output(self, text: str) -> None:
        self.output.configure(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)
        self.output.configure(state=tk.DISABLED)

    def _val(self, key: str) -> float:
        text = self.entries[key].get().strip()
        if not text:
            raise ValueError(f"{key} 为空")
        return float(text)

    def calculate(self) -> None:
        try:
            sigma0 = self._val("sigma0")
            alpha = self._val("alpha")
            q = self._val("q")
            b1 = self._val("b1")
            b2 = self._val("b2")
            T0 = self._val("T0")
            p = self._val("p")
            hs = self._val("hs")
            Ls = self._val("Ls")
            beta = self._val("beta")
            g = self._val("g")
        except ValueError as exc:
            messagebox.showerror("输入错误", str(exc))
            return
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("输入错误", f"无法解析输入: {exc}")
            return

        if any(x <= 0 for x in [sigma0, alpha, q, b1, b2, T0, p, hs, g]):
            messagebox.showerror("输入错误", "所有输入需大于 0")
            return

        # Solve h_c from h_c^3 - T0*h_c^2 + α*q^2/(2*g*p^2) = 0
        roots = solve_cubic(a=-T0, b=0.0, c=alpha * q * q / (2.0 * g * p * p), d=0.0)
        positives = [r for r in roots if r > 0]
        hc = max(positives) if positives else max(roots)

        # h_c'' from B.1.1-2
        shrink_factor = (b1 / b2) ** 0.25
        sqrt_term = math.sqrt(1.0 + 8.0 * alpha * q * q / (g * hc ** 3))
        hc2 = (hc / 2.0) * (sqrt_term - 1.0) * shrink_factor

        # ΔZ from B.1.1-4
        delta_z = alpha * q * q / (2.0 * g * p * p * hs ** 2) - alpha * q * q / (2.0 * g * hc2 ** 2)

        # Pool depth d from B.1.1-1
        d = sigma0 * hc2 - hs - delta_z

        # Water jump length Lj (B.1.2-2) and pool length Lsj (B.1.2-1)
        Lj = 6.9 * (hc2 - hc)
        Lsj = Ls + beta * Lj

        lines = [
            f"h_c = {hc:.4f} m",
            f"h_c'' = {hc2:.4f} m",
            f"ΔZ = {delta_z:.4f} m",
            f"d (消力池深度) = {d:.4f} m",
            f"L_j (水跃长度) = {Lj:.4f} m",
            f"L_sj (消力池长度) = {Lsj:.4f} m",
        ]
        self._set_output("\n".join(lines))


def main() -> None:
    app = BasinApp()
    app.mainloop()


if __name__ == "__main__":
    main()
