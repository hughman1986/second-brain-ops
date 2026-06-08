---
name: capture-youtube
description: 將 YouTube 影片字幕擷取為 Inbox 筆記
when_to_use:
  - 使用者貼出 YouTube URL
  - 使用者要求「擷取影片字幕」「把這部影片放進 second brain」
inputs:
  - YouTube URL
outputs:
  - 00_Inbox/YYYY-MM-DD - slug-transcript.md
  - 更新 00_Inbox/目錄.md (status: captured / needs-review)
related:
  - toolbox/youtube_transcript_to_inbox.py
  - skills/toc-sync.md
  - skills/code-distill-note.md
---

# Capture YouTube

## 觸發情境

使用者提供 YouTube URL，想保存影片內容。

## 執行步驟

1. **執行工具**（優先使用固定工具，不手寫一次性腳本）：
   ```powershell
   & 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/youtube_transcript_to_inbox.py "<youtube-url>"
   ```
2. 工具行為：
   - 用 `yt-dlp` 抓 metadata
   - 用 `youtube-transcript-api` 抓公開字幕
   - 語言優先順序：`zh-TW` → `zh-Hant` → `zh` → `en`
   - 輸出到 `00_Inbox/YYYY-MM-DD - slug-transcript.md`
   - 同 source 已存在則更新既有檔
   - 成功時自動更新 `00_Inbox/目錄.md` 為 `captured / needs-review`
3. **字幕不可得時**：不建空檔、不更新目錄；回報使用者並建議手動補資訊

## 完成條件

- Inbox 有逐字稿檔案，含 source URL、title、author、date
- `00_Inbox/目錄.md` 已同步

## 注意事項

- 逐字稿只屬 **Capture 階段**，不在這個 skill 做整理
- 後續整理走 [code-distill-note](code-distill-note.md) + [para-classify](para-classify.md)
- 不要在這步就寫 Summary / Action Items
