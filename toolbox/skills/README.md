# Skills 索引

本資料夾收錄從 `AGENTS.md` 抽取出的可重用 skill。每個 skill 對應一個固定流程或規範，AI agent 在遇到對應觸發情境時應直接遵循該 skill。

## 格式

所有 skill 檔案使用 Markdown + YAML frontmatter，UTF-8 編碼：

```yaml
---
name: skill-name
description: 一行描述
when_to_use:
  - 觸發情境 1
inputs:
  - 輸入 1
outputs:
  - 輸出 1
related:
  - 相關 skill 或檔案
---
```

## Skill 清單

| Priority | Skill | 用途 |
|---|---|---|
| P0 | [safe-commit](safe-commit.md) | git commit 前的機密外洩防護流程 |
| P1 | [project-reminder-scan](project-reminder-scan.md) | 專案提醒、週報、逾期掃描 |
| P1 | [equipment-new-work-order](equipment-new-work-order.md) | 建立新機種或新工單 |
| P2 | [capture-youtube](capture-youtube.md) | 抓 YouTube 字幕到 Inbox |
| P2 | [capture-pdf](capture-pdf.md) | PDF 原始抽取到 Inbox |
| P2 | [capture-pptx](capture-pptx.md) | PPTX 投影片抽取 |
| P2 | [capture-word](capture-word.md) | Word 文件抽取 |
| P3 | [code-distill-note](code-distill-note.md) | CODE 流程整理筆記 |
| P3 | [para-classify](para-classify.md) | PARA 分類判斷 |
| P3 | [toc-sync](toc-sync.md) | 同步更新資料夾 `目錄.md` |
| P3 | [stage-gate-check](stage-gate-check.md) | 設備裝機 10 階段 gate 檢查 |

## 與 AGENTS.md 的關係

- `AGENTS.md` 保留全域工作規範與心法
- 本資料夾 skill 是具體可執行流程的展開
- 規則衝突時以 `AGENTS.md` 為準
