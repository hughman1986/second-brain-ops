---
name: capture-word
description: 將 Word (.doc/.docx) 抽取為 Markdown，含標題層級、表格、圖片
when_to_use:
  - 使用者提供 .docx 或 .doc 檔
inputs:
  - Word 檔案路徑（.docx 或 .doc）
  - out_dir（必須手動指定）
outputs:
  - <out_dir>/<stem>_extract.md
  - <out_dir>/assets/<stem>/imgN.<ext>
related:
  - toolbox/word_extract.py
  - skills/toc-sync.md
---

# Capture Word

## 觸發情境

使用者提供 Word 檔案要保存內容。**禁止再使用「Word COM SaveAs 純文字 + Big5 重編碼」舊 pattern**（本工具已涵蓋且輸出乾淨 markdown）。

## 執行步驟

1. **確認 out_dir**（不會自動放 Inbox，需手動指定）：
   - 一般 capture → `00_Inbox/`
   - 專案素材 → `10_Projects/<machine-model>/<work-order-id>/source/`
2. **執行工具**：
   ```powershell
   & 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/word_extract.py "<src.docx|src.doc>" "<out_dir>"
   ```
3. 工具行為：
   - `.docx` → 用 `python-docx` 直接解析（跨平台、首選）
   - `.doc` → 用 Word COM (`pywin32`) 轉成暫存 `.docx` 再解析（**需 Windows + Office**）
   - 輸出 `<out_dir>/<stem>_extract.md`，含：
     - Heading 1~6 層級
     - 表格（已處理 horizontal/vertical merged cells 去重，避免合併儲存格內容重複 N 倍 token 浪費）
     - 行內圖片放 `<out_dir>/assets/<stem>/imgN.<ext>`
   - 預設跳過頁首/頁尾避免重複頁碼雜訊
4. **手動更新對應 `目錄.md`**（工具**不會**自動更新）：
   - 走 [toc-sync](toc-sync.md)

## 完成條件

- `<stem>_extract.md` 已產生
- 圖片已落地（如有）
- 對應 `目錄.md` 已手動同步

## 注意事項

- `.doc` 在無 Windows + Office 的環境無法處理，回報使用者
- 只做 raw extraction，不做摘要或行動項
- 後續整理走 [code-distill-note](code-distill-note.md) + [para-classify](para-classify.md)
