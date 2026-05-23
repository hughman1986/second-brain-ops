# 第二大腦 AI 工作規範

本資料夾是一個 Markdown-based second brain。任何 AI agent 在這裡整理資料時，都要依照 Tiago Forte《Building a Second Brain》的核心方法工作：`CODE`、`PARA`、`Progressive Summarization`，並以「未來可利用」為最終目標。

## Core Principles

- 不只是收藏資料，要把資料轉成可以支援行動、決策、創作與專案推進的知識資產。
- 優先保留與使用者目標、責任、興趣、輸出有關的內容。
- 每次整理資料時，都要問：
  - 這份資料未來可能用在哪裡？
  - 它支援哪個 project、area、resource topic，或應該 archive？
  - 有沒有 next action？
  - 能不能轉化成文章、簡報、決策、清單、研究卡片或其他 output？
- 內容使用繁體中文為主，保留必要英文方法名與專有名詞，例如 `CODE`、`PARA`、`Progressive Summarization`。
- 優先產出清楚、可搜尋、可重用的 Markdown，而不是過度複雜的分類。

## Folder Structure

若資料夾尚未存在，agent 可以在需要時建立以下結構：

```text
00_Inbox/
10_Projects/
20_Areas/
30_Resources/
40_Archives/
90_Outputs/
```

### 00_Inbox

暫存尚未整理、歸類不明、或需要使用者確認的資料。

適合：

- 剛貼上的文章、連結、摘錄、想法
- 來源不完整的資料
- 尚不確定要放入 `Projects`、`Areas` 或 `Resources` 的內容

若不確定歸類，先放入 `00_Inbox/`，並在筆記 frontmatter 或 tags 標記 `needs-review`。

### 10_Projects

放有明確成果、期限、完成條件的短中期工作。

判斷標準：

- 有 deadline 或預期完成時間
- 有明確 deliverable
- 完成後可以移到 `40_Archives/`

範例：

- 寫一篇文章
- 準備一次簡報
- 完成某個研究報告
- 規劃一次旅行
- 建立一套自動化流程

### 20_Areas

放需要長期維護、沒有明確結束時間的責任領域。

判斷標準：

- 需要持續注意與維持標準
- 不是一次性完成
- 常與生活、工作、健康、財務、人際、學習有關

範例：

- 健康管理
- 財務管理
- 職涯發展
- 家庭責任
- 個人學習系統

### 30_Resources

放未來可能有用的主題資料、研究素材、興趣與參考內容。

判斷標準：

- 沒有立即專案用途
- 不是必須長期維護的責任
- 但未來可能支援創作、研究、決策或專案

範例：

- AI 工具
- 寫作方法
- 心智模型
- 投資概念
- 書籍摘要
- 產業研究

### 40_Archives

放已完成、暫停、過期、不再活躍，但仍可能需要查找的資料。

適合：

- 完成的 projects
- 不再維護的 areas
- 過期 resources
- 舊版本輸出

Archive 不是刪除，而是降低干擾。

### 90_Outputs

放由筆記轉化出的成果。

範例：

- 文章草稿
- 簡報大綱
- 決策 memo
- 行動清單
- SOP
- 研究報告
- 腳本
- 課程或教學稿

## CODE Workflow

每次整理新資料時，依照 `CODE` 流程處理。

### 1. Capture

捕捉原始資料中值得保留的部分。

要做：

- 保留來源、作者、網址、日期或上下文。
- 摘出與使用者目標可能相關的段落、觀點、數據、問題、靈感。
- 避免完整搬運大量原文，優先摘要與引用短句。
- 如果資料太長，先建立 concise summary，再保留必要 highlights。

Capture 時要回答：

- 這份資料在說什麼？
- 哪些部分值得未來回來看？
- 它可能支援什麼行動、決策或輸出？

### 2. Organize

依照 `PARA` 決定資料位置。

優先順序：

1. 如果資料支援正在進行、有明確成果的事情，放入 `10_Projects/`。
2. 如果資料關於需要長期維護的責任，放入 `20_Areas/`。
3. 如果資料是未來可能有用的主題素材，放入 `30_Resources/`。
4. 如果資料已完成、過期或不再活躍，放入 `40_Archives/`。
5. 如果仍不確定，放入 `00_Inbox/` 並標記 `needs-review`。

不要根據資料「主題」直接分類到 Resources，而要先判斷它是否支援目前 project 或 area。

### 3. Distill

用 `Progressive Summarization` 萃取重點，讓未來能快速重用。

每份整理後的筆記建議包含：

- `Summary`：3-7 句說明核心內容。
- `Key Ideas`：最重要的概念、模型、洞察。
- `Highlights`：值得保留的短摘錄或重點句。
- `Bolded / Distilled Points`：用粗體標出真正重要的二次萃取重點。
- `Implications`：這些內容對使用者可能代表什麼。

萃取時避免把所有內容都視為重點。重點應該少而清楚。

### 4. Express

把資料轉成可用輸出，而不是停在筆記。

每份整理後的筆記都要盡量產生：

- `Action Items`：可執行的下一步。
- `Possible Outputs`：可以轉化成的文章、簡報、專案素材、決策 memo、SOP、清單。
- `Questions`：值得後續研究或請使用者確認的問題。
- `Related Notes`：可連到的相關筆記或主題。

如果資料沒有立即行動，也要至少說明未來可能在哪些情境下使用。

## Note Template

新增整理後的 Markdown 筆記時，優先使用以下結構：

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

欄位說明：

- `title`：清楚描述內容，不要只用來源標題。
- `source`：網址、書名、作者、對話、檔案或其他來源。
- `created`：建立日期，格式使用 `YYYY-MM-DD`。
- `updated`：最後更新日期，格式使用 `YYYY-MM-DD`。
- `para`：`project`、`area`、`resource`、`archive` 或 `inbox`。
- `tags`：使用少量有用 tags，避免標籤爆炸。
- `status`：例如 `captured`、`organized`、`distilled`、`expressed`、`needs-review`。

## File Naming

檔名要可讀、可搜尋、穩定。

建議格式：

```text
YYYY-MM-DD - descriptive-title.md
```

範例：

```text
2026-05-17 - building-a-second-brain-code-para.md
2026-05-17 - ai-tools-for-writing-workflow.md
```

檔名原則：

- 使用英文小寫、數字與 hyphen，避免空白造成工具相容性問題。
- 不確定標題時先用暫定標題，但內容中標記 `needs-review`。
- 不要建立過長檔名。

## Linking Guidelines

- 如果同一主題已有相關筆記，應在 `Related Notes` 加入 Markdown 連結。
- 不要為了連結而連結，只連真正可能幫助回顧或輸出的內容。
- 如果使用者未明確要求，不依賴 Obsidian 專屬語法；優先使用標準 Markdown 連結。
- 若未來使用 Obsidian，可接受 `[[wikilinks]]`，但本知識庫預設仍應能用一般 Markdown 閱讀。

## Directory Index Rules

每個主要資料夾都應該有一份 `目錄.md`，作為人類快速瀏覽與 AI 低 token 檢索的索引頁。

必須維護的索引頁：

```text
00_Inbox/目錄.md
10_Projects/目錄.md
20_Areas/目錄.md
30_Resources/目錄.md
40_Archives/目錄.md
90_Outputs/目錄.md
```

### Index Purpose

- `目錄.md` 只保存高密度摘要，不保存完整筆記內容。
- AI 回答問題、搜尋資料或整理新資料時，應先讀相關資料夾的 `目錄.md`，再決定是否讀取完整筆記。
- 避免一開始就掃描大量筆記全文，以降低 token 消耗。
- 人類也應能透過 `目錄.md` 快速知道資料夾裡有哪些內容、狀態與可能用途。

### Index Format

每份 `目錄.md` 應包含：

- 資料夾用途
- 瀏覽重點
- 索引表格：`筆記`、`狀態`、`摘要`、`更新日期`、`可能用途`
- AI 檢索提示

索引表格中的每筆摘要控制在 1-2 句。若需要更多細節，連到完整筆記，不要把全文放進目錄。

### Index Maintenance

當 agent 新增、更新、移動、封存或刪除筆記時，必須同步維護相關 `目錄.md`：

- 新增筆記：在該資料夾 `目錄.md` 加入一列。
- 更新筆記：更新 `狀態`、`摘要`、`更新日期` 或 `可能用途`。
- 移動筆記：從舊資料夾 `目錄.md` 移除或標記已移動，並加入新資料夾 `目錄.md`。
- 封存筆記：在 `40_Archives/目錄.md` 註明封存原因。
- Inbox 筆記：在 `00_Inbox/目錄.md` 標明 `needs-review`、缺少來源或待分類原因。

## Tooling / YouTube Transcript Capture

本知識庫會常用 YouTube 字幕作為 inbox 資料來源。處理 YouTube 連結時，優先使用固定工具，不要手寫一次性腳本。

工具位置：

```text
toolbox/youtube_transcript_to_inbox.py
```

指定 Python 環境：

```text
C:\Users\User\anaconda3\envs\py_3_13_13\python.exe
```

需要套件：

```text
youtube-transcript-api
yt-dlp
```

安裝或更新套件：

```powershell
& 'C:\Users\User\anaconda3\envs\py_3_13_13\python.exe' -m pip install youtube-transcript-api yt-dlp
```

抓取 YouTube 字幕到 `00_Inbox/`：

```powershell
& 'C:\Users\User\anaconda3\envs\py_3_13_13\python.exe' toolbox/youtube_transcript_to_inbox.py "<youtube-url>"
```

工具行為：

- 使用 `yt-dlp` 抓影片 metadata，例如 title、channel、canonical URL。
- 使用 `youtube-transcript-api` 抓公開可取得的字幕。
- 字幕語言優先順序預設為 `zh-TW`、`zh-Hant`、`zh`、`en`。
- 輸出 Markdown 到 `00_Inbox/YYYY-MM-DD - slug-transcript.md`。
- 若 `00_Inbox/` 已有相同 `source:` 的逐字稿，工具會更新既有檔案，避免重複。
- 成功後會同步更新 `00_Inbox/目錄.md`，狀態標記為 `captured / needs-review`。
- 若影片沒有公開字幕、需要登入或字幕抓取失敗，不要建立空檔案，也不要更新目錄。

抓完字幕後，逐字稿仍只是 `Capture` 階段。若使用者要求整理內容，再依 `CODE` 和 `PARA` 另行萃取、分類與輸出。

## Tooling / PDF Extraction

本知識庫會常用 PDF 作為 inbox 資料來源。處理 PDF 時，優先使用固定工具做原始抽取，不要手寫一次性腳本。

工具位置：

```text
toolbox/pdf_extract_to_inbox.py
```

指定 Python 環境：

```text
C:\Users\User\anaconda3\envs\py_3_13_13\python.exe
```

需要套件：

```text
pymupdf
```

安裝或更新套件：

```powershell
& 'C:\Users\User\anaconda3\envs\py_3_13_13\python.exe' -m pip install pymupdf
```

抽取 PDF 到 `00_Inbox/`：

```powershell
& 'C:\Users\User\anaconda3\envs\py_3_13_13\python.exe' toolbox/pdf_extract_to_inbox.py "<pdf-path>"
```

工具行為：

- 使用 `PyMuPDF` 讀取 PDF metadata、頁數、每頁可選取文字與內嵌圖片。
- 輸出 Markdown 到 `00_Inbox/YYYY-MM-DD - slug-extract.md`。
- 抽出的圖片保存到 `00_Inbox/assets/<pdf-slug>/`，並在 Markdown 內記錄頁碼與相對連結。
- 若 `00_Inbox/` 已有相同 `source:` 的 PDF 抽取筆記，工具會更新既有檔案，避免重複。
- 成功後會同步更新 `00_Inbox/目錄.md`，狀態標記為 `captured / needs-review`。
- 這版只做 raw extraction：不做 OCR，不做 AI 視覺解讀，不直接產生摘要或行動項目。

抽完 PDF 後，抽取檔仍只是 `Capture` 階段。若使用者要求整理內容，再依 `CODE` 和 `PARA` 另行萃取、分類與輸出。

## Tooling / Project Reminder Scan

設備軟體專案需要追蹤裝機時程與 issue 到期提醒。處理 `10_Projects/` 內的專案進度、週報、提醒、逾期項目時，必須先讀 `10_Projects/目錄.md`，再使用固定工具掃描，不要只靠 AI 自行瀏覽所有時程，也不要手寫一次性腳本。

工具位置：

```text
toolbox/project_reminder_scan.py
```

指定 Python 環境：

```text
C:\Users\User\anaconda3\envs\py_3_13_13\python.exe
```

掃描未來 7 天提醒與逾期項目：

```powershell
& 'C:\Users\User\anaconda3\envs\py_3_13_13\python.exe' toolbox/project_reminder_scan.py
```

指定日期與往後天數：

```powershell
& 'C:\Users\User\anaconda3\envs\py_3_13_13\python.exe' toolbox/project_reminder_scan.py --date 2026-05-23 --days 14
```

工具行為：

- 掃描 `10_Projects/*/schedule.md` 的 `Stage Timeline`，依 `Target Date`、`Remind On`、`Status` 找出提醒與逾期 stage。
- 掃描 `10_Projects/*/issues.md` 的 issue table，依 `Target Date`、`Remind On`、`Status` 找出需要追蹤的 issue。
- `done`、`closed`、`cancelled`、`canceled`、`skipped` 會視為已完成，不列入提醒。
- 輸出 Markdown report，方便貼回專案週報、會議紀錄或 dashboard。

AI agent 開始處理專案管理相關任務時，固定流程如下：

1. 先讀 `10_Projects/目錄.md`，掌握活躍專案、目前階段、下一步與阻塞。
2. 執行 `toolbox/project_reminder_scan.py`，讓 Python 負責日期比對與提醒偵測。
3. 若掃描結果出現提醒、逾期或阻塞，再讀對應專案的 `schedule.md`、`issues.md`。
4. 若需要判斷原因或背景，再讀 `decisions.md`、`meetings.md`、`resources.md`。
5. AI 負責把掃描結果整理成風險、next actions、週報、會議重點或需要使用者決策的問題。

## Handling New Inputs

當使用者提供新資料時，agent 應該：

1. 判斷資料類型：文章、書摘、影片摘要、想法、任務、會議紀錄、研究素材、決策材料等。
2. 執行 `Capture`：摘要來源與保留重點。
3. 執行 `Organize`：選擇 PARA 位置。
4. 執行 `Distill`：萃取最重要內容。
5. 執行 `Express`：提出行動、輸出或後續問題。
6. 建立或更新對應 Markdown 筆記。
7. 更新對應資料夾的 `目錄.md`。

如果資料不足以整理成完整筆記，建立 inbox note，保留缺口與後續問題。

## Classification Rules

使用以下問題判斷 PARA：

```text
這會幫助我完成某個有期限或成果的事情嗎？
-> Yes: Project

這是我需要長期維持標準或負責的領域嗎？
-> Yes: Area

這是未來可能有用的主題、素材或興趣嗎？
-> Yes: Resource

這已經完成、暫停、過期或不再活躍嗎？
-> Yes: Archive

以上都不確定嗎？
-> Inbox + needs-review
```

同一份資料可以在內容中提到多個用途，但檔案應優先放在最能促成行動的位置。

## Quality Bar

整理完成的筆記應該符合：

- 10 秒內能看懂這份資料為什麼重要。
- 1 分鐘內能找到最有用的重點。
- 未來能直接拿來支援一個 project、area、decision 或 output。
- 有來源、有摘要、有萃取、有可能用途。
- 不因過度分類而增加維護成本。

## Agent Behavior

- 在編輯前先檢查是否已有同名或高度相關筆記，避免重複。
- 優先更新既有筆記；只有主題明顯不同時才建立新筆記。
- 不要刪除使用者資料，除非使用者明確要求。
- 不要把所有資料都放進 `Resources`；先判斷是否支援 active project 或 ongoing area。
- 不要只輸出摘要；必須盡量包含 implications、action items 或 possible outputs。
- 若做出分類假設，要在筆記中簡短註明。
- 若需要使用者決定，先放入 `00_Inbox/`，並列出清楚的問題。
- 檢索資料時先讀 `目錄.md`，只有目錄顯示相關時才讀完整筆記。
- 新增、更新、移動或封存筆記後，必須同步更新相關資料夾的 `目錄.md`。
