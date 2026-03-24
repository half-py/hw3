# Poisson 雙模式模擬器

Python GUI 模擬工具，用於 Poisson 分布抽樣與統計估計。

本程式提供：

- 固定右端點抽樣
- 動態右端點抽樣
- PMF 與樣本分布比較
- E(X³) 估計
- 誤差分析
- GUI 操作介面

---

## GUI Preview

![GUI](docs/gui.png)

---

## 功能

✔ Poisson 隨機變數模擬  
✔ 固定 k_max 模式  
✔ 動態右端點模式  
✔ 母體 PMF vs Sample  
✔ λ 顯示  
✔ Sample mean 顯示  
✔ E(X³) 估計  
✔ 絕對誤差  
✔ 相對誤差  
✔ Matplotlib 嵌入 GUI  
✔ 模組化設計  

---

## 理論

Poisson:

P(X=k) = e^{-λ} λ^k / k!

E(X³) = λ³ + 3λ² + λ

逐步 PMF 更新：

P(k+1) = P(k) * λ / (k+1)

---



## 專案結構

```
hw3/
├─ main.py
├─ modules/
│  ├─ gui.py
│  ├─ sampler.py
│  ├─ stats.py
│  ├─ plot_utils.py
├─ docs/
│  └─ gui.png
├─ requirements.txt
├─ .gitignore
└─ README.md
```


---

## 執行

python main.py

---

## 需求

pip install -r requirements.txt


---

## 作者

m1144401王旭昌

Statistics / Probability / GUI / Python