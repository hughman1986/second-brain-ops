---
name: capture-excel
description: 將 Excel (.xlsx/.xlsm/.xls) 抽取為 Markdown，含工作表總覽、欄位對齊表格、內嵌圖片
when_to_use:
  - 使用者提供 .xlsx / .xlsm / .xls 檔
  - 廠商回填表、規格 checklist、BOM、排程表、E9/EAP 規格表等結構化表格
inputs:
  - Excel 檔案路徑（.xlsx / .xlsm / .xls）
  - out_dir（必須手動指定）
outputs:
  - <out_dir>/<stem>_extract.md
  - <out_dir>/assets/<stem>/sheetXX_N.<ext>
related:
  - toolbox/xlsx_extract.py
  - skills/toc-sync.md
---

# Capture Excel

## 觸發情境

使用者提供 Excel 檔要保存內容。Excel 內容（廠商回填表、規格 checklist、BOM、排程、E9 自動化檢查表等）轉成 PDF 或 CSV 後通常會失去欄位對齊、合併儲存格、隱藏工作表，請一律優先用本工具。

## 執行步驟

1. **確認 out_dir**（不會自動放 Inbox，需手動指定）：
   - 一般 capture → `00_Inbox/`
   - 專案素材 → `10_Projects/<machine-model>/<work-order-id>/source/`
2. **執行工具**：
   ```powershell
   & 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/xlsx_extract.py "<src.xlsx|src.xlsm|src.xls>" "<out_dir>"
   ```
3. 工具行為：
   - `.xlsx` / `.xlsm` → 用 `openpyxl` 直接解析（跨平台、首選，`data_only=True` 取得公式快取值）
   - `.xls` → 用 Excel COM (`pywin32`) 轉成暫存 `.xlsx` 再解析（**需 Windows + Office**）
   - 輸出 `<out_dir>/<stem>_extract.md`，含：
     - 工作表總覽（名稱 / used range / visible 或 hidden）
     - 每張工作表渲染成 Markdown 表格
       - 第一欄 `_row_` 是原 Excel 列號
       - 欄頭是 Excel 欄字母 A / B / ... / AA / AB ...
       - 合併儲存格的非錨點位置留白，維持欄位對齊
       - 儲存格內換行轉為 `<br>`、`|` 已 escape
   - 內嵌圖片放 `<out_dir>/assets/<stem>/sheetXX_N.<ext>`
4. **手動更新對應 `目錄.md`**（工具**不會**自動更新）：
   - 走 [toc-sync](toc-sync.md)

## 完成條件

- `<stem>_extract.md` 已產生
- 圖片已落地（如有）
- 對應 `目錄.md` 已手動同步

## 注意事項

- `.xls` 在無 Windows + Office 的環境無法處理，回報使用者
- 公式以快取值輸出；若檔案從未在 Excel 開啟過，公式儲存格可能為空（提醒使用者重存一次）
- 大型工作表（數百欄 × 數千列）會產生很長的 markdown；屬正常 raw extract
- 只做 raw extraction，不解圖表 (charts)、不做 AI 視覺解讀、不產生摘要或行動項
- 後續整理走 [code-distill-note](code-distill-note.md) + [para-classify](para-classify.md)
