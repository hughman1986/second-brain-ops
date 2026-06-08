---
name: capture-pptx
description: 將 PPTX 逐張投影片抽取為 Markdown（失真度遠低於 PDF）
when_to_use:
  - 使用者提供 PPTX 檔
  - 同時有 PPTX 與 PDF 來源時，優先用本 skill
inputs:
  - PPTX 檔案路徑
  - out_dir（必須手動指定，通常是 00_Inbox/ 或對應專案的 source/）
outputs:
  - <out_dir>/<pptx-stem>_extract.md
  - <out_dir>/assets/<pptx-stem>/slideXX_N.<ext>
related:
  - toolbox/pptx_extract.py
  - skills/capture-pdf.md
  - skills/toc-sync.md
---

# Capture PPTX

## 觸發情境

PPTX 原生格式失真度遠低於 PDF 轉檔（結構、表格、講者備忘稿、原解析度圖片皆可保留）。**若同時有 PPTX 和 PDF，一律優先用 PPTX。**

## 執行步驟

1. **確認 out_dir**（不像 PDF/YouTube 會自動放 Inbox，需手動指定）：
   - 一般 capture → `00_Inbox/`
   - 屬於特定專案的素材 → `10_Projects/<machine-model>/<work-order-id>/source/`
2. **執行工具**（優先使用固定工具，不手寫一次性腳本）：
   ```powershell
   & 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/pptx_extract.py "<src.pptx>" "<out_dir>"
   ```
3. 工具行為：
   - 用 `python-pptx` 逐張投影片抽文字、表格、講者備忘稿
   - 處理 group shapes (recursive) 與內嵌圖片
   - 輸出 `<out_dir>/<pptx-stem>_extract.md`
   - 圖片放 `<out_dir>/assets/<pptx-stem>/slideXX_N.<ext>`
4. **手動更新對應 `目錄.md`**（工具**不會**自動更新）：
   - 走 [toc-sync](toc-sync.md)

## 完成條件

- `<pptx-stem>_extract.md` 已產生，含每張投影片內容
- assets 圖片已落地
- 對應 `目錄.md` 已手動同步

## 注意事項

- 只做 raw extraction，不做 AI 視覺解讀、不產生摘要或行動項
- 後續整理走 [code-distill-note](code-distill-note.md) + [para-classify](para-classify.md)
