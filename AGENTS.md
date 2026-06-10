# 第二大腦 AI 工作規範

本資料夾是 Markdown-based second brain。整理資料時遵循 Tiago Forte《Building a Second Brain》：`CODE`、`PARA`、`Progressive Summarization`，目標是把資料轉成未來可支援行動、決策、創作、專案推進的知識資產。

## 基本原則

- 內容以繁體中文為主，保留必要英文方法名與專有名詞。
- 所有 Markdown 檔案一律用 UTF-8 讀寫；PowerShell 讀檔用 `Get-Content -Encoding UTF8`，寫檔或工具輸出也要確保 UTF-8，避免繁中亂碼。
- 優先保留與使用者目標、責任、興趣、輸出有關的內容。
- 每次整理都判斷：未來用途、所屬 PARA、next action、可否轉成文章/簡報/決策/清單/研究卡片/SOP/其他 output。
- 產出清楚、可搜尋、可重用的 Markdown，避免過度分類。

## PARA 結構

必要時建立並維護：

```text
00_Inbox/      尚未整理、歸類不明、來源不完整、需確認
10_Projects/   有成果、期限、完成條件；完成後封存
20_Areas/      長期維護的責任領域，無明確結束時間
30_Resources/  未來可能有用的主題、研究素材、參考內容
40_Archives/   已完成、暫停、過期、不活躍但可查找
90_Outputs/    由筆記轉化出的文章、簡報、memo、SOP、報告等成果
```

PARA 判斷順序：支援有期限/成果的事 `Project`；長期責任 `Area`；未來素材 `Resource`；完成/暫停/過期 `Archive`；不確定則放 `00_Inbox/` 並標 `needs-review`。不要只因主題相似就放 Resources，先判斷是否支援 active project 或 ongoing area。

## CODE 流程

1. `Capture`：保留來源、作者、網址、日期/上下文；摘要重點、短摘錄、可用數據、問題與靈感，避免大量搬運原文。
2. `Organize`：依 PARA 放到最能促成行動的位置；不確定先進 Inbox。
3. `Distill`：用 Progressive Summarization，留下 `Summary`、`Key Ideas`、`Highlights`、`Distilled Points`、`Implications`。
4. `Express`：產生 `Action Items`、`Possible Outputs`、`Questions`、`Related Notes`；即使無立即行動，也要說明未來用途。

## 筆記格式

新增整理後的筆記優先使用：

```markdown
---
title:
source:
created:
updated:
para:
tags:
status:
---

# Title

## Summary
## Key Ideas
## Highlights
## Distilled Points
## Implications
## Action Items
## Possible Outputs
## Related Notes
## Questions
```

日期用 `YYYY-MM-DD`。`para` 用 `project`、`area`、`resource`、`archive`、`inbox`。`status` 可用 `captured`、`organized`、`distilled`、`expressed`、`needs-review`。檔名用 `YYYY-MM-DD - descriptive-title.md`，英文小寫、數字、hyphen，避免過長。

## 索引規則

每個主要資料夾都必須有 `目錄.md`：

```text
00_Inbox/目錄.md
10_Projects/目錄.md
20_Areas/目錄.md
30_Resources/目錄.md
40_Archives/目錄.md
90_Outputs/目錄.md
```

`目錄.md` 只放高密度摘要，不放全文。格式包含：資料夾用途、瀏覽重點、索引表格（`筆記`、`狀態`、`摘要`、`更新日期`、`可能用途`）、AI 檢索提示。新增、更新、移動、封存、刪除筆記時必須同步更新相關目錄。檢索資料時先讀目錄，只有相關時才讀完整筆記。

## 連結規則

- 只連真正有助回顧或輸出的相關筆記。
- 預設使用標準 Markdown 連結；不依賴 Obsidian 語法。
- 若使用 wikilinks 也要讓知識庫仍可用一般 Markdown 閱讀。

## 原始素材保存 (source/ 慣例)

capture-* 工具預設把 raw extract、原始檔、assets 放到 `00_Inbox/`，那只是 Capture 階段的暫存位置。經過 Organize / Distill 後 (`code-distill-note` 流程)，必須把整組原始素材搬到該筆記所屬資料夾的 `source/` 子資料夾，與 distilled 筆記放在一起。

標準結構 (適用於 `10_Projects/<...>/`、`30_Resources/<...>/`、`20_Areas/<...>/` 等)：

```text
<owner-folder>/
├── 目錄.md
├── <distilled-note>.md            ← 整理後的主筆記
├── (其他 project / resource 檔)
└── source/
    ├── <原始檔>.pdf / .pptx / .docx / .odt / .md / ...
    ├── <YYYY-MM-DD - slug-extract>.md   ← capture-* 抽取的 raw extract
    └── assets/<pdf-slug 或 pptx-stem>/   ← 抽取的圖片、附件
```

操作要點：

- 搬移時 raw extract md 內的 `source:` 路徑與「## Source」段落要一併更新為新位置。
- 圖片相對路徑必須維持 `assets/<slug>/...`，不要攤平到 `assets/` 根目錄；若 `Move-Item` 攤平了要重新巢狀化。
- 搬移後立即更新原 `00_Inbox/目錄.md`「已整理出去的資料」歷史紀錄，並在新位置 `目錄.md` 加 `## Source` 區段列出 PDF / extract / assets 路徑。
- distilled 筆記的 frontmatter `source:` 與「## Related Notes」連結都要指向新的 `source/` 路徑。
- 既有範例：`10_Projects/striper-grinder/source/`、`10_Projects/cmp-digital-twin/source/`、`10_Projects/gsvw-s306/source/`、`30_Resources/tsmc-specs/source/`。

## 版本控制與 commit 規範

- 為避免機密外洩，commit 只能包含規範、模板、工具程式或明確可公開的設定檔；預設只提交本規範相關變更。
- 所有整理過的文件與知識庫內容一律不得 commit，包含 `00_Inbox/`、`10_Projects/`、`20_Areas/`、`30_Resources/`、`40_Archives/`、`90_Outputs/` 及其子資料夾內的檔案。
- 不使用 `git add .`、`git add -A` 或其他會批次加入知識庫內容的命令；只能用明確檔名 stage 可提交的規範檔。
- commit 前必須執行 `git status --short` 與 `git diff --cached --name-only`，確認 staged 檔案沒有任何整理後文件、專案資料、目錄索引、逐字稿、PDF 抽取內容或 assets。
- 若使用者要求 commit 筆記、整理成果、專案文件或輸出成果，必須先提醒有機密外洩風險，且不得執行，除非使用者明確指定可公開的單一檔案與原因。

## 設備專案管理

設備軟體專案採「機種 / 工單」兩層結構。同機種共用資訊放在 `10_Projects/<machine-model>/`，單張工單放在 `10_Projects/<machine-model>/<work-order-id>/`。工單才是 PARA 意義上的 active project。

新增機種時複製 `templates/equipment-model-template/` 到 `10_Projects/<machine-model>/`；新增工單時複製 `templates/equipment-project-template/` 到 `10_Projects/<machine-model>/<work-order-id>/`。更新工單 `project.md`、`schedule.md`、`issues.md`，並同步更新機種 `目錄.md` 與 `10_Projects/目錄.md`。

標準裝機階段：

```text
開工 > 開 BOM > 組裝配線 > 送電 > IO Check > 機台測試 > 交機 move in > 客戶端組裝送電 > 整合測試 > release 產線
```

專案管理相關任務固定流程：

1. 先讀 `10_Projects/目錄.md`。
2. 執行 `toolbox/project_reminder_scan.py`，用 Python 比對日期與提醒。
3. 有提醒、逾期或阻塞時，先讀對應機種 `目錄.md`，再讀工單的 `schedule.md`、`issues.md`。
4. 需背景時再讀工單 `decisions.md`、`meetings.md`、`resources.md` 或機種 `common-resources.md`。
5. AI 負責整理風險、next actions、週報、會議重點或需使用者決策的問題。

## Skill 索引

固定流程與規範已展開為獨立 skill，集中放在 `toolbox/skills/`。遇到對應觸發情境時，AI 應直接遵循該 skill 而不重新推導：

| Skill | 何時用 |
|---|---|
| `safe-commit` | 任何 git commit / push / PR 動作 |
| `project-reminder-scan` | 專案進度、週報、提醒、逾期查詢 |
| `equipment-new-work-order` | 建立新機種或新工單 |
| `stage-gate-check` | 設備裝機 stage gate 判斷 |
| `capture-youtube` / `capture-pdf` / `capture-pptx` / `capture-word` / `capture-excel` / `capture-outlook` | 對應素材的 raw capture |
| `code-distill-note` | CODE 流程整理筆記 |
| `para-classify` | PARA 分類判斷 |
| `toc-sync` | 任何 PARA 資料夾內容變動後同步 `目錄.md` |

詳見 `toolbox/skills/README.md`。本檔（`AGENTS.md`）保留全域工作規範與心法，skill 是具體可執行流程；規則衝突時以本檔為準。

## 工具

文書工具(PDF 抽取、YouTube 字幕、專案提醒)統一在 base 之外的 Python venv `sb-docs` 內執行；此 venv 由 base 環境的 Python 建立，不要污染 base。

新環境一次性建置(只做一次)：

```powershell
& 'C:\Users\jmhuang\AppData\Local\miniconda3\python.exe' -m venv 'C:\Users\jmhuang\.venvs\sb-docs'
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' -m pip install --upgrade pip pymupdf youtube-transcript-api yt-dlp python-pptx python-docx openpyxl pywin32 html2text
```

指定 Python：

```text
C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe
```

如果以後 base Python 換位置，更新上方第一行路徑；如果 venv 換位置，同步更新本檔與 `README.md`。

### YouTube 字幕

優先使用固定工具，不手寫一次性腳本。

```powershell
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/youtube_transcript_to_inbox.py "<youtube-url>"
```

工具會用 `yt-dlp` 抓 metadata、`youtube-transcript-api` 抓公開字幕；語言優先 `zh-TW`、`zh-Hant`、`zh`、`en`；輸出到 `00_Inbox/YYYY-MM-DD - slug-transcript.md`；同 source 更新既有檔；成功後更新 `00_Inbox/目錄.md` 為 `captured / needs-review`。字幕不可得時不建空檔、不更新目錄。逐字稿只屬 Capture，整理時再依 CODE/PARA 處理。

### PDF 抽取

優先使用固定工具，不手寫一次性腳本。

```powershell
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/pdf_extract_to_inbox.py "<pdf-path>"
```

工具用 PyMuPDF 抽 metadata、頁數、文字、內嵌圖片；輸出到 `00_Inbox/YYYY-MM-DD - slug-extract.md`；圖片放 `00_Inbox/assets/<pdf-slug>/`；同 source 更新既有檔；成功後更新 `00_Inbox/目錄.md` 為 `captured / needs-review`。此工具只做 raw extraction，不 OCR、不做 AI 視覺解讀、不產生摘要或行動項。

### PPTX 抽取

優先使用固定工具，不手寫一次性腳本。PPTX 原生格式失真度遠低於 PDF 轉檔(結構、表格、講者備忘稿、原解析度圖片皆可保留)，若同時有 PPTX 和 PDF 一律優先用 PPTX。

```powershell
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/pptx_extract.py "<src.pptx>" "<out_dir>"
```

工具用 `python-pptx` 逐張投影片抽文字、表格、講者備忘稿，處理 group shapes (recursive) 與內嵌圖片；輸出 `<out_dir>/<pptx-stem>_extract.md` + `<out_dir>/assets/<pptx-stem>/slideXX_N.<ext>`。與 PDF/YouTube 工具不同，**out_dir 需手動指定**(通常是 `00_Inbox/` 或對應專案的 `source/`)，工具不自動更新 `00_Inbox/目錄.md`。此工具只做 raw extraction，不做 AI 視覺解讀、不產生摘要或行動項。

### Word 抽取

優先使用固定工具，不手寫一次性腳本(也不要再用「Word COM SaveAs 純文字 + Big5 重編碼」舊 pattern,本工具已涵蓋且輸出乾淨 markdown)。

```powershell
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/word_extract.py "<src.docx|src.doc>" "<out_dir>"
```

自動依副檔名分流:`.docx` 用 `python-docx` 直接解析(跨平台、首選);`.doc` 透過 Word COM (`pywin32`,**需 Windows + Office**) 轉成暫存 `.docx` 再解析。輸出 `<out_dir>/<stem>_extract.md`,包含 Heading 1~6 層級、表格(已處理 horizontal/vertical merged cells 去重,避免合併儲存格內容重複 N 倍 token 浪費)、行內圖片放 `<out_dir>/assets/<stem>/imgN.<ext>`。預設跳過頁首/頁尾避免重複頁碼雜訊。**out_dir 需手動指定**,工具不自動更新 `00_Inbox/目錄.md`。

### Excel 抽取

優先使用固定工具，不手寫一次性腳本。Excel 內容(尤其是廠商回填表、規格 checklist、BOM、排程表)在轉成 PDF 或 CSV 後通常會失去欄位對齊、合併儲存格、隱藏工作表等資訊，請一律優先用本工具。

```powershell
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/xlsx_extract.py "<src.xlsx|src.xlsm|src.xls>" "<out_dir>"
```

自動依副檔名分流:`.xlsx` / `.xlsm` 用 `openpyxl` 直接解析(跨平台、首選,以 `data_only=True` 取得公式快取值);`.xls` 透過 Excel COM (`pywin32`,**需 Windows + Office**) 轉成暫存 `.xlsx` 再解析。輸出 `<out_dir>/<stem>_extract.md`,內含工作表總覽 (名稱 / used range / visible/hidden) 與每張工作表的 Markdown 表格 (第一欄是原 Excel 列號,欄頭是 Excel 欄字母 A/B/...,合併儲存格的非錨點位置會留白以維持欄位對齊);內嵌圖片放 `<out_dir>/assets/<stem>/sheetXX_N.<ext>`。**out_dir 需手動指定**,工具不自動更新 `00_Inbox/目錄.md`。此工具只做 raw extraction,不解圖表 (charts)、不做 AI 視覺解讀、不產生摘要或行動項。

### Outlook 信件抽取

優先使用固定工具，不手寫一次性腳本。連本機已登入的 Outlook（`win32com.client`，需 Windows + Office），可依資料夾 + 過濾條件批次抓，也可用 EntryID / ConversationID 精準抓單封或整串 thread。

```powershell
# 預設抓進 00_Inbox/，同步更新目錄.md
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/outlook_extract_to_inbox.py --since 2026-06-08 --from "boss@company.com" --subject "review"

# 抓進專案 source/（跳過 Inbox 流程）
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/outlook_extract_to_inbox.py --conversation-id <ID> --slug cmp-customer --out-dir 10_Projects/cmp-digital-twin/source

# 列出符合條件但不寫檔
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/outlook_extract_to_inbox.py --since 2026-06-08 --limit 20 --dry-run
```

行為：用 `Outlook.Application` COM 連線；支援 `--folder`（巢狀 `Inbox/Sub/Sub2`）、`--store`、`--since/--until`、`--from`（可重複）、`--subject`（可重複）、`--unread`、`--entry-id`（可重複）、`--conversation-id`、`--limit`、`--html`（HTMLBody 經 `html2text` 轉 markdown）、`--no-attachments`、`--out-dir`、`--dry-run`。輸出單一 Markdown 把多封信合併成 thread，每封含 metadata 表（From/To/Cc/Received/Folder/Importance/Categories/EntryID/ConversationID）+ body + 附件清單；附件 / 嵌入圖存到 `<out_dir>/assets/<slug>/`。預設輸出到 `00_Inbox/YYYY-MM-DD - <slug>-mail.md` 並更新 `00_Inbox/目錄.md` 為 `captured / needs-review`；`--out-dir` 指定其他位置時不動 Inbox 目錄（依 toc-sync 自行更新該資料夾目錄）。此工具只做 raw extraction，不做 AI 摘要 / 行動項；**不修改 Outlook 內容**（不標已讀、不移動、不寄信）。

### 專案提醒

處理專案進度、週報、提醒、逾期項目時，必須先讀 `10_Projects/目錄.md`，再執行：

```powershell
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/project_reminder_scan.py
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/project_reminder_scan.py --date 2026-05-23 --days 14
```

工具遞迴掃描 `10_Projects/**/schedule.md` 與 `issues.md`，依 `Target Date`、`Remind On`、`Status` 找提醒與逾期；`done`、`closed`、`cancelled`、`canceled`、`skipped` 不列入；輸出含機種與工單欄位的 Markdown report。

## 新資料處理

使用者提供新資料時：判斷類型；執行 Capture、Organize、Distill、Express；建立或更新 Markdown；同步更新目錄。資料不足則建 inbox note，列出缺口與問題。

## 品質與行為

- 筆記需讓人 10 秒內看懂重要性、1 分鐘內找到重點，且有來源、摘要、萃取、可能用途。
- 編輯前先檢查同名或相關筆記，優先更新既有筆記；主題明顯不同才新建。
- 不刪除使用者資料，除非使用者明確要求。
- 不只輸出摘要，盡量包含 implications、action items、possible outputs。
- 分類假設要在筆記中簡短註明；需使用者決定時放 Inbox 並列問題。
