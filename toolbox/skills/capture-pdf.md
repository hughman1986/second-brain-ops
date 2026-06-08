---
name: capture-pdf
description: 將 PDF 原始內容抽取為 Inbox 筆記
when_to_use:
  - 使用者提供 PDF 路徑，要保存內容
  - 需要把 PDF 文字與圖片納入 second brain
inputs:
  - PDF 檔案路徑
outputs:
  - 00_Inbox/YYYY-MM-DD - slug-extract.md
  - 00_Inbox/assets/<pdf-slug>/ 內嵌圖片
  - 更新 00_Inbox/目錄.md (status: captured / needs-review)
related:
  - toolbox/pdf_extract_to_inbox.py
  - skills/capture-pptx.md (PPTX 失真度更低，同時有就優先 PPTX)
  - skills/toc-sync.md
  - skills/code-distill-note.md
---

# Capture PDF

## 觸發情境

使用者提供 PDF 路徑要保存內容。**若同時有 PPTX 來源檔，優先用 [capture-pptx](capture-pptx.md)**（PDF 轉檔失真度高）。

## 執行步驟

1. **執行工具**（優先使用固定工具，不手寫一次性腳本）：
   ```powershell
   & 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/pdf_extract_to_inbox.py "<pdf-path>"
   ```
2. 工具行為：
   - 用 PyMuPDF 抽 metadata、頁數、文字、內嵌圖片
   - 輸出到 `00_Inbox/YYYY-MM-DD - slug-extract.md`
   - 圖片放 `00_Inbox/assets/<pdf-slug>/`
   - 同 source 已存在則更新既有檔
   - 成功時自動更新 `00_Inbox/目錄.md` 為 `captured / needs-review`

## 完成條件

- Inbox 有抽取檔，含 source 路徑、page count、metadata
- assets 圖片已落地
- `00_Inbox/目錄.md` 已同步

## 注意事項

- 此工具**只做 raw extraction**：不 OCR、不做 AI 視覺解讀、不產生摘要或行動項
- 後續整理走 [code-distill-note](code-distill-note.md) + [para-classify](para-classify.md)
- 掃描型 PDF 文字抽不出來時，回報使用者；不在此 skill 做 OCR
