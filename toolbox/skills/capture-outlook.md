---
name: capture-outlook
description: 從本機 Outlook 抓取信件批次或 thread 為 Markdown
when_to_use:
  - 使用者要把 Outlook 信件（單封 / thread / 條件批次）納入 second brain
  - 需要保留信件原始 metadata、附件、決策上下文供後續整理
  - 處理客戶 / 廠商 / 主管郵件以便產生會議紀錄、決策紀錄、issue 或 SOP
inputs:
  - 篩選條件（folder / since / until / from / subject / unread）或 EntryID / ConversationID
  - 可選 --out-dir（預設 00_Inbox）、--slug、--html、--no-attachments、--dry-run
outputs:
  - 預設 00_Inbox/YYYY-MM-DD - slug-mail.md（單檔合併多封）
  - 附件 / 嵌入圖 到 <out_dir>/assets/<slug>/
  - 預設情境下更新 00_Inbox/目錄.md (status: captured / needs-review)
related:
  - toolbox/outlook_extract_to_inbox.py
  - skills/toc-sync.md
  - skills/code-distill-note.md
  - skills/para-classify.md
---

# Capture Outlook

## 觸發情境

使用者要把 Outlook 信件（單封、整串 thread 或某資料夾條件批次）保存到 second brain。
本機已登入的 Outlook 即可，不需 Azure App 或 Graph 認證。

## 執行步驟

1. **先 dry-run 確認範圍**（不寫檔，只列出符合條件的信件）：
   ```powershell
   & 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/outlook_extract_to_inbox.py `
       --since 2026-06-08 --limit 20 --dry-run
   ```

2. **抓進 Inbox**（一般 capture）：
   ```powershell
   & 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/outlook_extract_to_inbox.py `
       --since 2026-06-08 --from "boss@company.com" --subject "review" `
       --slug 0608-review-thread
   ```

3. **抓進專案 source/**（已知所屬 project / area，跳過 Inbox 流程）：
   ```powershell
   & 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/outlook_extract_to_inbox.py `
       --conversation-id <ID> --slug cmp-customer-thread `
       --out-dir 10_Projects/cmp-digital-twin/source
   ```

4. **指定 EntryID 抓單封 / 多封**（從 Outlook 取得 EntryID 後）：
   ```powershell
   & 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/outlook_extract_to_inbox.py `
       --entry-id <ID1> --entry-id <ID2> --slug pm-decision
   ```

## 常用旗標

| 旗標 | 用途 |
|---|---|
| `--folder "Inbox/Projects/CMP"` | 指定資料夾（支援巢狀，第一段可省 `Inbox`） |
| `--store "user@domain"` | 多帳號 / PST 時指定 store |
| `--since YYYY-MM-DD` / `--until YYYY-MM-DD` | 日期區間 |
| `--from / --subject` | 寄件人 / 主旨 子字串過濾（可重複） |
| `--unread` | 只抓未讀 |
| `--entry-id` / `--conversation-id` | 精準抓單封或整串 |
| `--html` | 用 HTMLBody 經 html2text 轉 markdown（保留排版） |
| `--no-attachments` | 跳過附件 / 嵌入圖儲存 |
| `--out-dir` | 指定輸出資料夾（非 00_Inbox 時不動 Inbox 目錄） |
| `--dry-run` | 只列出符合條件的信件，不寫檔 |

## 完成條件

- 產出 `<out_dir>/<date> - <slug>-mail.md`，依時間排序、每封信含 metadata 表 + body + 附件連結
- 附件 / 嵌入圖落地到 `<out_dir>/assets/<slug>/`
- 若輸出到 `00_Inbox/`，`00_Inbox/目錄.md` 已同步加入該筆記為 `captured / needs-review`
- 若輸出到專案 / 領域資料夾，依 [toc-sync](toc-sync.md) 更新該資料夾 `目錄.md`

## 注意事項

- 此工具**只做 raw extraction**：不做摘要、AI 解讀、行動項提取
- **不修改 Outlook 內容**：不標已讀、不移動、不刪除、不回信
- 預設用 plain `Body`；若信件排版重要（例如有表格、編號清單）改用 `--html`
- 大批量 (>200 封) 時用 `--limit` 控制，並考慮拆多個 slug 以維持單檔可讀性
- 信件常涉及客戶 / 廠商機密，後續整理依 [safe-commit](safe-commit.md) 嚴禁 commit 知識庫內容
- 後續整理走 [code-distill-note](code-distill-note.md) + [para-classify](para-classify.md)
