# 第二大腦使用說明

這是一個用 Markdown 管理的 Second Brain，用來保存、整理、萃取並利用你找到的資料。這個知識庫採用《Building a Second Brain》的兩個核心方法：

- `CODE`：Capture、Organize、Distill、Express
- `PARA`：Projects、Areas、Resources、Archives

根目錄的 `AGENTS.md` 是給 AI agent 讀的工作規範；這份 `README.md` 是給你日常使用時看的快速說明。

## 資料夾用途

```text
00_Inbox/       暫存未整理、還不知道怎麼歸類的資料
10_Projects/    有明確成果、期限或完成條件的專案資料
20_Areas/       需要長期維護的責任領域
30_Resources/   未來可能有用的主題、興趣、研究素材
40_Archives/    已完成、暫停、過期或不再活躍的資料
90_Outputs/     從筆記轉化出來的文章、簡報、清單、報告等成果
```

## 最簡單的使用方式

1. 先把新資料丟進 `00_Inbox/`。
2. 請 AI 依照 `AGENTS.md` 整理這份資料。
3. AI 會判斷它應該放入 `Projects`、`Areas`、`Resources` 或 `Archives`。
4. AI 會用 `CODE` 流程整理成可重用的 Markdown 筆記。
5. AI 會同步更新對應資料夾的 `目錄.md`。
6. 如果資料能變成文章、簡報、決策 memo、行動清單或 SOP，就放入 `90_Outputs/`。

你可以直接對 AI 說：

```text
請依照 AGENTS.md，用 CODE 和 PARA 整理 00_Inbox 裡的新資料。
```

或：

```text
請把這篇文章整理成第二大腦筆記，判斷 PARA 分類，萃取重點，並提出可能輸出。
```

## 目錄.md 的用途

每個主要資料夾都有一份 `目錄.md`，它是該資料夾的索引頁。

用途：

- 讓你快速知道資料夾裡有哪些內容。
- 讓 AI 先讀短索引，再決定要不要讀完整筆記。
- 避免未來資料變多時，每次都掃描大量筆記，浪費 token。
- 記錄每份筆記的狀態、摘要、更新日期與可能用途。

使用方式：

1. 找資料時，先打開相關資料夾的 `目錄.md`。
2. 如果目錄摘要符合需求，再打開完整筆記。
3. 新增、移動、更新或封存筆記後，請 AI 同步更新 `目錄.md`。

你可以直接對 AI 說：

```text
請先讀各資料夾的目錄.md，再找與這個問題相關的筆記，不要一開始就讀全部全文。
```

## PARA 判斷方式

整理資料時，先問這幾個問題：

```text
這會幫助我完成某個有期限或成果的事情嗎？
-> 放到 10_Projects

這是我需要長期維持或負責的領域嗎？
-> 放到 20_Areas

這是未來可能有用的主題、素材或興趣嗎？
-> 放到 30_Resources

這已經完成、暫停、過期或不再活躍嗎？
-> 放到 40_Archives

我還不確定嗎？
-> 先放到 00_Inbox，標記 needs-review
```

重點是先判斷「用途」，不要只根據「主題」分類。例如一篇 AI 寫作文章，如果正在支援某個文章專案，就放 `10_Projects/`；如果只是未來參考，才放 `30_Resources/`。

## CODE 整理流程

### Capture

捕捉值得保留的內容：

- 來源、作者、網址、日期
- 核心摘要
- 重要觀點、數據、問題、靈感
- 未來可能用途

### Organize

用 `PARA` 決定資料位置。優先放到最能支援行動的位置。

### Distill

用 `Progressive Summarization` 萃取重點：

- 先摘要
- 再列 key ideas
- 再標出真正重要的 distilled points
- 最後寫出 implications

### Express

把資料轉化成可用成果：

- 下一步行動
- 可寫成的文章
- 可做成的簡報
- 可形成的 SOP
- 可支援的決策
- 後續研究問題

## 建議筆記格式

整理後的筆記建議使用：

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

建議檔名：

```text
YYYY-MM-DD - descriptive-title.md
```

範例：

```text
2026-05-17 - building-a-second-brain-code-para.md
```

## 日常維護節奏

建議每週做一次簡單整理：

1. 檢查 `00_Inbox/` 是否有未整理資料。
2. 把能判斷用途的內容移到 PARA 對應資料夾。
3. 將重要筆記補上 `Distilled Points`、`Action Items`、`Possible Outputs`。
4. 把完成或不再活躍的專案移到 `40_Archives/`。
5. 更新所有有變動資料夾的 `目錄.md`。
6. 從重要筆記中挑一個轉成 `90_Outputs/` 裡的成果。

## 給 AI 的常用指令

```text
請整理 00_Inbox 裡尚未整理的資料，依照 AGENTS.md 執行 CODE 和 PARA。
```

```text
請先讀各資料夾的目錄.md，再找相關筆記；只有必要時才讀完整筆記。
```

```text
請檢查這份筆記應該屬於 Project、Area、Resource 還是 Archive，並說明理由。
```

```text
請把這份筆記做 Progressive Summarization，補上 Summary、Key Ideas、Distilled Points、Action Items、Possible Outputs。
```

```text
請從 30_Resources 裡找出可以轉成文章或簡報的素材，產生到 90_Outputs。
```

```text
請幫我整理 10_Projects，把已完成或不活躍的內容移到 40_Archives。
```

```text
請檢查所有目錄.md 是否和資料夾內筆記一致，並更新過期索引。
```
