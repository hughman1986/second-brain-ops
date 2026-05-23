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
toolbox/         YouTube、PDF、專案提醒等輔助工具
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

設備軟體專案使用模板：

```text
templates/equipment-project-template/
```

新增專案時，複製到：

```text
10_Projects/<project-slug>/
```

然後更新：

- `project.md`：專案總覽、範圍、owner、release 條件
- `schedule.md`：裝機時程、stage gate、提醒日期
- `issues.md`：Issue list、嚴重度、owner、next action、target date
- `tasks.md`：Next Actions、Waiting、Scheduled、Done
- `decisions.md`：重要決策與原因
- `meetings.md`：會議紀錄與 action items
- `resources.md`：規格、圖面、IO list、程式版本、備份路徑
- `10_Projects/目錄.md`：跨專案 dashboard

常用指令：

```text
請用 templates/equipment-project-template 建立一個新的設備軟體專案，放到 10_Projects，並更新 10_Projects/目錄.md。
```

## 裝機時程與 Issue 追蹤

設備專案標準階段：

```text
開工 > 開 BOM > 組裝配線 > 送電 > IO Check > 機台測試 > 交機 move in > 客戶端組裝送電 > 整合測試 > release 產線
```

追蹤原則：

- 每個 stage 都要有 `Target Date`、`Remind On`、`Owner`、`Status`。
- 影響時程的問題要寫進 `issues.md`，並連回對應 stage。
- `critical` 或 `high` issue 未關閉時，不應進下一個 stage gate，除非已有明確 workaround。
- 每次更新專案狀態後，同步更新 `10_Projects/目錄.md` 的目前階段、下一步、風險/阻塞。

## 提醒掃描流程

處理專案進度、週報、提醒或逾期項目時，固定流程是：

1. 先讀 `10_Projects/目錄.md`。
2. 執行 Python 掃描工具。
3. 若有提醒、逾期或阻塞，再讀對應專案的 `schedule.md`、`issues.md`。
4. 需要背景時，再讀 `decisions.md`、`meetings.md`、`resources.md`。

掃描未來 7 天提醒與逾期項目：

```powershell
& 'C:\Users\User\anaconda3\envs\py_3_13_13\python.exe' toolbox/project_reminder_scan.py
```

指定日期與往後天數：

```powershell
& 'C:\Users\User\anaconda3\envs\py_3_13_13\python.exe' toolbox/project_reminder_scan.py --date 2026-05-23 --days 14
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

## 工具指令

指定 Python：

```text
C:\Users\User\anaconda3\envs\py_3_13_13\python.exe
```

YouTube 字幕擷取：

```powershell
& 'C:\Users\User\anaconda3\envs\py_3_13_13\python.exe' toolbox/youtube_transcript_to_inbox.py "<youtube-url>"
```

PDF 原始抽取：

```powershell
& 'C:\Users\User\anaconda3\envs\py_3_13_13\python.exe' toolbox/pdf_extract_to_inbox.py "<pdf-path>"
```

專案提醒掃描：

```powershell
& 'C:\Users\User\anaconda3\envs\py_3_13_13\python.exe' toolbox/project_reminder_scan.py
```

工具會自動把 YouTube/PDF 結果放入 `00_Inbox/` 並更新 `00_Inbox/目錄.md`；這些結果仍只是 Capture 階段，需要再依 `CODE` / `PARA` 整理。
