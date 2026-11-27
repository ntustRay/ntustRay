# AGENTS.md

- [README.md](README.md) 是 GitHub 公開個人頁。保留 Full-Stack Engineer 定位，專案、文章和圖片使用可公開查證的資料。
- `scripts/update_profile.py` 用 Python 標準函式庫更新 README 內有標記的段落，以及 `assets/stats.svg` 和 `assets/top-langs.svg`。變更自動產生的內容時，調整產生器並保留 README 的起訖標記。
- 先用 `python -m py_compile scripts/update_profile.py` 檢查語法。需要檢查產生結果時，使用 Python 3.12 執行 `python scripts/update_profile.py`，再檢閱 README 與 SVG 的 diff。此步驟會讀取線上公開資料並更新本機檔案。
