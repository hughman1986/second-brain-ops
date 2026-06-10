# 第二大腦與設備專案管理

這個資料夾是 Markdown-based second brain，也用來管理設備軟體專案。日常使用時看這份 `README.md`；AI agent 的完整工作規範看 `AGENTS.md`。

核心方法：

- `CODE`：Capture、Organize、Distill、Express
- `PARA`：Projects、Areas、Resources、Archives
- `Progressive Summarization`：逐層萃取重點，讓筆記未來可重用

## 這個資料夾用來做什麼

- 保存新資料、想法、會議紀錄、研究素材。
- 把資料整理成可支援行動、決策、專案推進的知識資產。
- 管理多個設備軟體專案的時程、Issue、決策與交付狀態。
- 從筆記產出文章、簡報、決策 memo、SOP、行動清單或研究報告。

## 資料夾結構

```text
00_Inbox/       尚未整理、歸類不明、來源不完整、需確認
10_Projects/    有成果、期限、完成條件的活躍專案
20_Areas/       長期維護的責任領域
30_Resources/   未來可能有用的主題、研究素材、參考內容
40_Archives/    已完成、暫停、過期、不活躍但可查找
90_Outputs/     由筆記轉化出的文章、簡報、memo、SOP、報告等成果
templates/       可複製的專案與筆記模板
toolbox/         YouTube、PDF、PPTX、Word、Excel、Outlook、專案提醒等輔助工具
```

每個主要資料夾都有 `目錄.md`。找資料時先看目錄，再讀完整筆記；新增、更新、移動或封存筆記後，也要同步更新目錄。

## 日常使用流程

1. 新資料先放進 `00_Inbox/`。
2. 請 AI 依 `AGENTS.md` 用 `CODE` 與 `PARA` 整理。
3. AI 會判斷資料屬於 `Projects`、`Areas`、`Resources`、`Archives` 或繼續留在 Inbox。
4. 有可交付成果時，整理到 `90_Outputs/`。
5. 有變動時，同步更新對應資料夾的 `目錄.md`。

常用指令：

```text
請依照 AGENTS.md，用 CODE 和 PARA 整理 00_Inbox 裡的新資料。
```

```text
請先讀各資料夾的目錄.md，再找與這個問題相關的筆記，不要一開始就讀全部全文。
```

## 設備專案快速建立

設備軟體專案採「機種 / 工單」兩層結構。同機種共用資訊放在機種資料夾，實際交付與時程追蹤放在工單資料夾。

```text
10_Projects/
  <machine-model>/
    目錄.md
    model.md
    common-resources.md
    <work-order-id>/
      project.md
      schedule.md
      issues.md
      tasks.md
      decisions.md
      meetings.md
      resources.md
      outputs/
```

新增機種時使用模板：

```text
templates/equipment-model-template/
```

複製到：

```text
10_Projects/<machine-model>/
```

新增工單時使用模板：

```text
templates/equipment-project-template/
```

複製到：

```text
10_Projects/<machine-model>/<work-order-id>/
```

然後更新：

- `project.md`：專案總覽、範圍、owner、release 條件
- `schedule.md`：裝機時程、stage gate、提醒日期
- `issues.md`：Issue list、嚴重度、owner、next action、target date
- `tasks.md`：Next Actions、Waiting、Scheduled、Done
- `decisions.md`：重要決策與原因
- `meetings.md`：會議紀錄與 action items
- `resources.md`：規格、圖面、IO list、程式版本、備份路徑
- 機種 `目錄.md`：同機種工單 dashboard
- `10_Projects/目錄.md`：跨機種/工單 dashboard

常用指令：

```text
請先確認或建立機種資料夾，再用 templates/equipment-project-template 建立新工單，並更新機種目錄與 10_Projects/目錄.md。
```

## 裝機時程與 Issue 追蹤

設備專案標準階段：

```text
開工 > 開 BOM > 組裝配線 > 送電 > IO Check > 機台測試 > 交機 move in > 客戶端組裝送電 > 整合測試 > release 產線
```

追蹤原則：

- 每張工單的每個 stage 都要有 `Target Date`、`Remind On`、`Owner`、`Status`。
- 影響時程的問題要寫進 `issues.md`，並連回對應 stage。
- `critical` 或 `high` issue 未關閉時，不應進下一個 stage gate，除非已有明確 workaround。
- 每次更新工單狀態後，同步更新機種 `目錄.md` 與 `10_Projects/目錄.md` 的目前階段、下一步、風險/阻塞。

## 提醒掃描流程

處理專案進度、週報、提醒或逾期項目時，固定流程是：

1. 先讀 `10_Projects/目錄.md`。
2. 執行 Python 掃描工具。
3. 若有提醒、逾期或阻塞，先讀對應機種 `目錄.md`，再讀工單的 `schedule.md`、`issues.md`。
4. 需要背景時，再讀工單 `decisions.md`、`meetings.md`、`resources.md` 或機種 `common-resources.md`。

掃描未來 7 天提醒與逾期項目：

```powershell
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/project_reminder_scan.py
```

指定日期與往後天數：

```powershell
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/project_reminder_scan.py --date 2026-05-23 --days 14
```

常用指令：

```text
請先讀 10_Projects/目錄.md，再執行 project_reminder_scan.py，整理目前需要注意的專案提醒、逾期項目與 next actions。
```

## CODE / PARA 整理規則

PARA 判斷：

```text
這會幫助我完成某個有期限或成果的事情嗎？ -> 10_Projects
這是需要長期維持或負責的領域嗎？ -> 20_Areas
這是未來可能有用的主題、素材或參考嗎？ -> 30_Resources
這已完成、暫停、過期或不活躍嗎？ -> 40_Archives
還不確定嗎？ -> 00_Inbox，標記 needs-review
```

CODE 流程：

- `Capture`：保留來源、作者、網址、日期、摘要、重點與可能用途。
- `Organize`：放到最能支援行動的位置。
- `Distill`：萃取 `Summary`、`Key Ideas`、`Highlights`、`Distilled Points`、`Implications`。
- `Express`：產生 `Action Items`、`Possible Outputs`、`Questions`、`Related Notes`。

## 常用 AI 指令

```text
請檢查這份筆記應該屬於 Project、Area、Resource 還是 Archive，並說明理由。
```

```text
請把這份筆記做 Progressive Summarization，補上 Summary、Key Ideas、Distilled Points、Action Items、Possible Outputs。
```

```text
請整理 10_Projects，檢查目前階段、逾期項目、open issues 和下一步。
```

```text
請檢查所有目錄.md 是否和資料夾內筆記一致，並更新過期索引。
```

```text
請從 30_Resources 找出可以轉成文章、簡報或 SOP 的素材，產生到 90_Outputs。
```

## 編碼規則

所有 Markdown 檔案都用 UTF-8 讀寫，避免繁體中文亂碼。使用 PowerShell 檢查檔案時，優先指定：

```powershell
Get-Content -Encoding UTF8 README.md
Get-Content -Encoding UTF8 AGENTS.md
```

AI agent 編輯或產生筆記、目錄、工具輸出時，也要確保寫入 UTF-8。

## 工具指令

文書工具(PDF / YouTube / PPTX / Word / Excel / Outlook 抽取、專案提醒)統一在 base 之外的 Python venv `sb-docs` 內執行，這個 venv 專門給第二大腦的文書整理任務使用。

### 一次性建置(只在新環境做一次)

用 base 環境的 Python 建立 venv：

```powershell
& 'C:\Users\jmhuang\AppData\Local\miniconda3\python.exe' -m venv 'C:\Users\jmhuang\.venvs\sb-docs'
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' -m pip install --upgrade pip pymupdf youtube-transcript-api yt-dlp python-pptx python-docx openpyxl html2text pywin32
```

如果以後 base Python 換位置，請更新上方第一行路徑；如果 venv 換到別的位置，請同步更新本檔與 `AGENTS.md`。

### 指定 Python

```text
C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe
```

### YouTube 字幕擷取

```powershell
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/youtube_transcript_to_inbox.py "<youtube-url>"
```

### PDF 原始抽取

```powershell
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/pdf_extract_to_inbox.py "<pdf-path>"
```

### PPTX 投影片抽取

```powershell
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/pptx_extract.py "<src.pptx>" "<out_dir>"
```

逐張投影片抽出文字、表格、講者備忘稿，圖片放到 `<out_dir>/assets/<pptx-stem>/`，並輸出 `<pptx-stem>_extract.md`。比 PDF 轉檔失真度低很多，PPTX 可直接抽原始結構與原解析度圖片。與 PDF/YouTube 不同，**out_dir 需手動指定**(通常是 `00_Inbox/` 或對應專案的 `source/`)。

### Word 文件抽取

```powershell
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/word_extract.py "<src.docx|src.doc>" "<out_dir>"
```

支援 `.docx` (用 `python-docx`,跨平台,首選) 與 `.doc` (用 Word COM 先轉 `.docx`,**需 Windows + Office**)。輸出 markdown 含標題層級、表格 (合併儲存格已自動去重避免 token 浪費)、內嵌圖片到 `<out_dir>/assets/<stem>/`。**out_dir 需手動指定**。

### Excel 表單抽取

```powershell
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/xlsx_extract.py "<src.xlsx|src.xlsm|src.xls>" "<out_dir>"
```

支援 `.xlsx` / `.xlsm` (用 `openpyxl`,跨平台,首選,以 `data_only=True` 取公式快取值) 與 `.xls` (用 Excel COM 先轉 `.xlsx`,**需 Windows + Office**)。輸出 markdown 含工作表總覽 + 每張工作表的對齊表格 (第一欄是 Excel 原列號,欄頭是 Excel 欄字母,合併儲存格非錨點留白以維持欄位對齊),內嵌圖片放 `<out_dir>/assets/<stem>/`。**out_dir 需手動指定**。Excel 內容 (廠商回填表、規格 checklist、BOM、排程表) 一律優先用本工具而不要先轉 PDF/CSV,以免失去欄位對齊、合併儲存格與隱藏工作表資訊。

### Outlook 信件抽取

```powershell
# 依資料夾 + filter 搜尋
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/outlook_extract_to_inbox.py --folder "收件匣\01_行政單位\PM" --subject "交期異動" --since 2026-05-01

# 依 EntryID 抽單封
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/outlook_extract_to_inbox.py --entry-id "<EntryID>"

# 依 ConversationID 抽整串對話
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/outlook_extract_to_inbox.py --conversation-id "<ConvID>"
```

用本機 Outlook COM (`pywin32`) + `html2text` 抽信件 metadata、body、附件,**需 Windows + 已登入的 Outlook**。多封信合併成單檔 markdown,附件存到 `assets/<slug>/`。預設輸出到 `00_Inbox/`,可用 `--out-dir` 指定 (整理到專案時通常指向 `10_Projects/<...>/source/`)。常用旗標：`--dry-run` 只列符合的信不抽取、`--html` 保留 HTML body 而非轉 markdown、`--no-attachments` 跳過附件。

### 專案提醒掃描

```powershell
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/project_reminder_scan.py
& 'C:\Users\jmhuang\.venvs\sb-docs\Scripts\python.exe' toolbox/project_reminder_scan.py --date 2026-05-23 --days 14
```

工具會自動把 YouTube/PDF 結果放入 `00_Inbox/` 並更新 `00_Inbox/目錄.md`；這些結果仍只是 Capture 階段，需要再依 `CODE` / `PARA` 整理。
