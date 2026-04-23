import math
import random


# =========================
# 固定 k_max 模式
# =========================
def build_pmf_fixed(lam, k_max):
    """
    建立 Poisson(lam) 在 k = 0, 1, ..., k_max 的 PMF（機率質量函數）列表。

    參數：
        lam   : Poisson 分配的參數 λ
        k_max : 只計算到哪一個 k 為止

    回傳：
        pmf   : 一個 list，其中 pmf[k] = P(X = k)
    """

    pmf = []   # 用來儲存每個 k 對應的機率 P(X=k)

    # Poisson 分配在 k = 0 時：
    # P(X=0) = e^{-λ}
    pk = math.exp(-lam)
    pmf.append(pk)

    # 利用遞推公式：
    # P(X=k) = P(X=k-1) * λ / k
    # 這樣就不用每次都重新算階乘，效率比較好
    for k in range(1, k_max + 1):
        pk = pmf[-1] * lam / k
        pmf.append(pk)

    return pmf


def build_cdf(pmf):
    """
    根據 PMF 建立 CDF（累積分配函數）列表。

    例如：
        pmf = [p0, p1, p2]
    則：
        cdf = [p0, p0+p1, p0+p1+p2]

    參數：
        pmf : 機率質量函數列表

    回傳：
        cdf : 累積機率列表
    """

    cdf = []   # 用來存累積後的機率
    total = 0.0

    # 逐步把 pmf 的機率加總起來
    for p in pmf:
        total += p
        cdf.append(total)

    return cdf


def sample_from_cdf(cdf):
    """
    使用反函數抽樣（inverse transform sampling）的想法，
    從給定的 CDF 中抽出一個樣本值 k。

    作法：
        1. 先產生 U ~ Uniform(0,1)
        2. 找最小的 k，使得 U <= CDF[k]
        3. 回傳該 k

    參數：
        cdf : 累積機率列表

    回傳：
        k   : 抽到的樣本值
    """

    u = random.random()   # 產生 [0,1) 之間的均勻亂數

    # enumerate(cdf) 會同時拿到：
    # k     = 索引值
    # right = cdf[k]，也就是目前區間的右端點
    for k, right in enumerate(cdf):
        if u <= right:
            return k

    # 理論上如果 CDF 最後一項等於 1，前面就應該 return 了。
    # 這裡保留是為了避免浮點數誤差，作為保底。
    return len(cdf) - 1


def generate_samples_fixed(lam, k_max, n_samples):
    """
    用「固定 k_max」的方法產生多個 Poisson 樣本。

    流程：
        1. 先建立 PMF
        2. 再建立 CDF
        3. 重複從 CDF 抽樣 n_samples 次

    參數：
        lam       : Poisson 分配參數 λ
        k_max     : PMF/CDF 計算到的最大 k
        n_samples : 要產生幾個樣本

    回傳：
        samples   : 抽樣結果 list
    """

    pmf = build_pmf_fixed(lam, k_max)
    cdf = build_cdf(pmf)

    samples = []

    # _ 是 Python 常見寫法，表示：
    # 「這個迴圈變數我不需要真的使用，只是單純重複做 n_samples 次」
    for _ in range(n_samples):
        samples.append(sample_from_cdf(cdf))

    return samples


# =========================
# 動態右端點模式
# =========================
def sample_poisson_dynamic(lam):
    """
    使用「動態擴張右端點」的方法抽一個 Poisson 樣本。

    核心想法：
        不先固定 k_max，也不先把整個 CDF 算完，
        而是邊算 PMF、邊累加右端點，直到覆蓋亂數 u 為止。

    流程：
        1. 先抽一個 U ~ Uniform(0,1)
        2. 從 k=0 開始，先算 P(X=0)
        3. 如果 U 已經落在目前累積區間內，就回傳 k
        4. 否則就往下一個 k 推進，繼續累加

    這種方法的好處是：
        只算到「真的需要的地方」，不用預先決定 k_max
    """

    u = random.random()   # 先抽一個 [0,1) 的均勻亂數

    k = 0

    # 先從 P(X=0) 開始
    pk = math.exp(-lam)

    # right 表示目前累積到的右端點
    # 一開始只有 P(X=0)，所以 right = P(X=0)
    right = pk

    # 如果 u 還比目前累積右端點大，
    # 代表樣本還不在目前區間內，要繼續往右擴張
    while u > right:

        k += 1

        # 用遞推公式由上一項算下一項
        pk = pk * lam / k

        # 將新的機率加到右端點上
        right += pk

    return k


def generate_samples_dynamic(lam, n_samples):
    """
    用「動態右端點」的方法產生多個 Poisson 樣本。

    參數：
        lam       : Poisson 分配參數 λ
        n_samples : 要產生的樣本數

    回傳：
        samples   : 抽樣結果 list
    """

    samples = []

    for _ in range(n_samples):
        samples.append(sample_poisson_dynamic(lam))

    return samples


# =========================
# 畫圖用 PMF
# =========================
def build_pmf_for_plot(lam, x_max):
    """
    建立畫圖時使用的 PMF。

    這個函式和 build_pmf_fixed 很像，
    差別主要在命名用途上：
    build_pmf_fixed 偏向抽樣流程使用
    build_pmf_for_plot 偏向視覺化畫圖使用

    參數：
        lam   : Poisson 分配參數 λ
        x_max : 畫圖時 x 軸顯示到哪裡

    回傳：
        pmf   : 從 0 到 x_max 的 PMF list
    """

    pmf = []

    # P(X=0)
    pk = math.exp(-lam)
    pmf.append(pk)

    # 遞推計算後續各點機率
    for k in range(1, x_max + 1):
        pk = pk * lam / k
        pmf.append(pk)

    return pmf