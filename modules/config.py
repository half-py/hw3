from matplotlib import rcParams


def setup_matplotlib():
    """設定 matplotlib 中文字型"""
    rcParams["font.family"] = "sans-serif"

    rcParams["font.sans-serif"] = [
        "Microsoft JhengHei",
        "PMingLiU",
        "MingLiU",
        "SimHei",
    ]

    rcParams["axes.unicode_minus"] = False