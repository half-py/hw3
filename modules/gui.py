import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

from modules.sampler import (
    generate_samples_fixed,
    generate_samples_dynamic,
    build_pmf_for_plot,
)

from modules.stats_utils import (
    estimate_ex3,
    sample_mean,
    true_ex3_poisson,
    calc_errors,
)

from modules.plot_utils import draw_plot


class PoissonSimulatorApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Poisson 模擬器")
        self.root.geometry("1100x720")

        self.canvas_widget = None
        self.mode_var = tk.StringVar(value="dynamic")
        self.result_text = tk.StringVar()
        self.result_text.set("請輸入參數後開始模擬")
        self.result_value_labels = {}
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

        self.build_widgets()
        self.update_kmax_state()
        

    # ==================================================
    # 建立介面
    # ==================================================
    def build_widgets(self):

        # ======================
        # 主標題
        # ======================
        tk.Label(
            self.root,
            text="Poisson 雙模式模擬器",
            font=("Microsoft JhengHei", 18, "bold"),
        ).pack(pady=(10, 5))

        # ======================
        # 主版面：左控制 / 右圖表
        # ======================
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        frame_left = tk.Frame(main_frame)
        frame_left.pack(side="left", fill="y", padx=10, pady=10)

        frame_right = tk.Frame(main_frame)
        frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        frame_left.config(width=340)
        frame_left.pack_propagate(False)

        self.frame_left = frame_left
        self.frame_right = frame_right

        # ======================
        # 左側：參數設定區
        # ======================
        frame_input = tk.LabelFrame(
            self.frame_left,
            text="參數設定",
            font=("Microsoft JhengHei", 11, "bold"),
            padx=12,
            pady=10,
        )
        frame_input.pack(fill="x", pady=8)

        # 第一列：輸入框
        tk.Label(frame_input, text="lambda", font=("Microsoft JhengHei", 10)).grid(
            row=0, column=0, padx=8, pady=8, sticky="w"
        )

        self.entry_lambda = tk.Entry(frame_input, width=12, font=("Arial", 10))
        self.entry_lambda.grid(row=0, column=1, padx=8, pady=8)
        self.entry_lambda.insert(0, "3")

        tk.Label(frame_input, text="樣本數 n", font=("Microsoft JhengHei", 10)).grid(
            row=1, column=0, padx=8, pady=8, sticky="w"
        )

        self.entry_samples = tk.Entry(frame_input, width=12, font=("Arial", 10))
        self.entry_samples.grid(row=1, column=1, padx=8, pady=8)
        self.entry_samples.insert(0, "1000")

        tk.Label(frame_input, text="k_max", font=("Microsoft JhengHei", 10)).grid(
            row=2, column=0, padx=8, pady=8, sticky="w"
        )

        self.entry_kmax = tk.Entry(frame_input, width=12, font=("Arial", 10))
        self.entry_kmax.grid(row=2, column=1, padx=8, pady=8)
        self.entry_kmax.insert(0, "15")

        # 第二列：模式選擇
        tk.Label(frame_input, text="抽樣模式", font=("Microsoft JhengHei", 10)).grid(
            row=3, column=0, padx=8, pady=8, sticky="w"
        )

        tk.Radiobutton(
            frame_input,
            text="固定 k_max",
            variable=self.mode_var,
            value="fixed",
            command=self.update_kmax_state,
            font=("Microsoft JhengHei", 10),
        ).grid(row=3, column=1, padx=8, pady=4, sticky="w")

        tk.Radiobutton(
            frame_input,
            text="動態右端點",
            variable=self.mode_var,
            value="dynamic",
            command=self.update_kmax_state,
            font=("Microsoft JhengHei", 10),
        ).grid(row=4, column=1, padx=8, pady=4, sticky="w")

        # 第三列：按鈕
        frame_buttons = tk.Frame(frame_input)
        frame_buttons.grid(row=5, column=0, columnspan=2, pady=(12, 4))

        tk.Button(
            frame_buttons,
            text="開始模擬",
            command=self.run_simulation,
            font=("Microsoft JhengHei", 11),
            width=12,
            bg="#4F81BD",
            fg="white",
        ).pack(side="left", padx=8)

        tk.Button(
            frame_buttons,
            text="退出程式",
            command=self.exit_app,
            font=("Microsoft JhengHei", 11),
            width=12,
        ).pack(side="left", padx=8)

        # ======================
        # 左側：模擬結果區
        # ======================
        frame_result = tk.LabelFrame(
            self.frame_left,
            text="模擬結果",
            font=("Microsoft JhengHei", 11, "bold"),
            padx=12,
            pady=10,
        )
        frame_result.pack(fill="x", pady=8)

        result_inner = tk.Frame(frame_result, bg="#FAFAFA")
        result_inner.pack(fill="x", padx=4, pady=4)

        rows = [
            ("模擬模式", "mode"),
            ("樣本平均", "mean"),
            ("估計的 E(X^3)", "est_ex3"),
            ("真實的 E(X^3)", "true_ex3"),
            ("絕對誤差", "abs_err"),
            ("相對誤差", "rel_err"),
        ]

        for i, (label_text, key) in enumerate(rows):
            tk.Label(
                result_inner,
                text=label_text,
                font=("Microsoft JhengHei", 10),
                bg="#f7f7f7",
                anchor="w",
                width=14,
            ).grid(row=i, column=0, sticky="w", padx=(8, 4), pady=4)

            value_label = tk.Label(
                result_inner,
                text="--",
                font=("Consolas", 10, "bold"),
                bg="#f7f7f7",
                anchor="e",
                width=14,
                fg="#222222",
            )
            value_label.grid(row=i, column=1, sticky="e", padx=(4, 8), pady=4)

            self.result_value_labels[key] = value_label

        # ======================
        # 右側：圖表區
        # ======================
        frame_chart = tk.LabelFrame(
            self.frame_right,
            text="分布圖比較",
            font=("Microsoft JhengHei", 11, "bold"),
            padx=10,
            pady=10,
        )
        frame_chart.pack(fill="both", expand=True)

        self.frame_plot = tk.Frame(frame_chart)
        self.frame_plot.pack(fill="both", expand=True)

    # ==================================================
    # 更新 k_max 輸入框狀態
    # ==================================================
    def update_kmax_state(self):

        if self.mode_var.get() == "fixed":
            self.entry_kmax.config(state="normal")
        else:
            self.entry_kmax.config(state="disabled")

    # ==================================================
    # 執行模擬
    # ==================================================
    def run_simulation(self):

        try:
            lam = float(self.entry_lambda.get())
            n = int(self.entry_samples.get())
            mode = self.mode_var.get()

            if lam <= 0:
                raise ValueError("lambda 必須大於 0")

            if n <= 0:
                raise ValueError("樣本數必須大於 0")

            if mode == "fixed":
                k_max = int(self.entry_kmax.get())

                if k_max < 0:
                    raise ValueError("k_max 必須大於等於 0")

                samples = generate_samples_fixed(lam, k_max, n)
                x_max = k_max

            else:
                samples = generate_samples_dynamic(lam, n)
                x_max = max(samples) + 2

            true_pmf = build_pmf_for_plot(lam, x_max)

            est = estimate_ex3(samples)
            true = true_ex3_poisson(lam)
            abs_err, rel_err = calc_errors(est, true)
            mean = sample_mean(samples)

            mode_name = "固定 k_max" if mode == "fixed" else "動態右端點"

            self.result_value_labels["mode"].config(text=mode_name, fg="#222222")
            self.result_value_labels["mean"].config(text=f"{mean:.6f}", fg="#222222")
            self.result_value_labels["est_ex3"].config(text=f"{est:.6f}", fg="#1B5E20")   # 深綠
            self.result_value_labels["true_ex3"].config(text=f"{true:.6f}", fg="#0D47A1") # 深藍
            self.result_value_labels["abs_err"].config(text=f"{abs_err:.6f}", fg="#B23A48") # 深紅
            self.result_value_labels["rel_err"].config(text=f"{rel_err:.2%}",fg="#B23A48")

            self.canvas_widget = draw_plot(
                self.frame_plot,
                self.canvas_widget,
                samples,
                true_pmf,
                lam,
                n,
                x_max,
            )

        except Exception as e:
            messagebox.showerror("錯誤", str(e))

    # ==================================================
    # 退出程式
    # ==================================================
    def exit_app(self):

        if messagebox.askyesno("exit", "確定離開？"):

            if self.canvas_widget is not None:
                self.canvas_widget.get_tk_widget().destroy()
                self.canvas_widget = None

            plt.close("all")
            self.root.quit()
            self.root.destroy()