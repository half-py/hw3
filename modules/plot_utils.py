import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter


def draw_plot(
    frame_plot,
    old_canvas,
    samples,
    true_pmf,
    lam,
    n_samples,
    x_max,
):
    if old_canvas is not None:
        old_canvas.get_tk_widget().destroy()

    fig, ax = plt.subplots(figsize=(8, 5))

    # 背景設成白色
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    x_values = list(range(x_max + 1))

    # =========================
    # 樣本平均
    # =========================
    sample_avg = sum(samples) / len(samples)

    # =========================
    # 樣本分布：離散分布用 bar
    # =========================
    counts = Counter(samples)
    freq = [counts.get(x, 0) / len(samples) for x in x_values]

    ax.bar(
        x_values,
        freq,
        width=0.8,
        color="#F2C879",
        edgecolor="#6B4F1D",
        linewidth=1.0,
        alpha=0.6,
        label=f"Sample (n={n_samples})",
    )

    # =========================
    # 真實 PMF
    # =========================
    ax.plot(
        x_values,
        true_pmf,
        "o-",
        color="#1E3A8A",
        linewidth=2.0,
        markersize=6,
        markerfacecolor="#1E3A8A",
        markeredgecolor="#1E3A8A",
        label="True PMF",
    )

    # =========================
    # λ 線
    # =========================
    ax.axvline(
        lam,
        color="#C0392B",
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
        label="λ",
    )

    # =========================
    # 樣本平均線
    # =========================
    ax.axvline(
        sample_avg,
        color="#2E8B57",
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
        label="Sample Mean",
    )

    # =========================
    # 標題與座標軸
    # =========================
    ax.set_xlabel("x", fontsize=11)
    ax.set_ylabel("Probability", fontsize=11)
    ax.set_title(f"Poisson({lam})：母體 PMF 與抽樣分布", fontsize=14)

    ax.set_xlim(-0.5, x_max + 0.5)

    # 淡化格線
    ax.grid(
        axis="y",
        linestyle="--",
        linewidth=0.8,
        alpha=0.2,
    )

    # 圖例
    ax.legend(
        loc="upper right",
        frameon=True,
        facecolor="white",
        edgecolor="#CCCCCC",
    )

    # 座標軸顏色不要太黑
    for spine in ax.spines.values():
        spine.set_color("#666666")

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return canvas