---
name: code-distill-note
description: 用 CODE 流程把 raw capture 整理為可重用的 distilled 筆記
when_to_use:
  - capture-* 完成後的下一步整理
  - 使用者要求「整理 / 萃取 / 摘要 / distill」某份筆記
  - Inbox 筆記要升級為 organized / distilled / expressed 狀態
inputs:
  - 既有筆記路徑（通常在 00_Inbox/）
outputs:
  - 更新後的筆記，含標準 frontmatter 與 CODE 八個 section
  - 同步更新對應 目錄.md
related:
  - skills/para-classify.md
  - skills/toc-sync.md
  - AGENTS.md「CODE 流程」「筆記格式」
---

# Code Distill Note

## CODE 流程

1. **Capture**：保留來源、作者、網址、日期/上下文；摘要重點、短摘錄、可用數據、問題與靈感（避免大量搬運原文）
2. **Organize**：依 PARA 放到最能促成行動的位置；不確定先進 Inbox（用 [para-classify](para-classify.md)）
3. **Distill**：用 Progressive Summarization，留下 `Summary`、`Key Ideas`、`Highlights`、`Distilled Points`、`Implications`
4. **Express**：產生 `Action Items`、`Possible Outputs`、`Questions`、`Related Notes`；即使無立即行動，也要說明未來用途

## 標準筆記格式

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

- 日期用 `YYYY-MM-DD`
- `para`：`project` / `area` / `resource` / `archive` / `inbox`
- `status`：`captured` / `organized` / `distilled` / `expressed` / `needs-review`
- 檔名：`YYYY-MM-DD - descriptive-title.md`，英文小寫、數字、hyphen，避免過長

## 執行步驟

1. **讀既有筆記**，確認 source、目前 status、已有內容
2. **編輯前先檢查同名或相關筆記**，優先更新既有筆記；主題明顯不同才新建
3. **補 frontmatter**：缺欄位補齊，更新 `updated`、`status`
4. **逐 section 萃取**：
   - Summary：3~5 句話讓人 10 秒看懂重要性
   - Key Ideas：條列核心觀點
   - Highlights：原文短摘錄（quote）
   - Distilled Points：用自己的話總結最關鍵的幾點
   - Implications：對使用者目標、責任、專案的影響
   - Action Items：next actions（誰、何時、做什麼）
   - Possible Outputs：可轉成文章/簡報/SOP/決策 memo 等
   - Related Notes：用標準 Markdown link 連結真正相關的筆記
   - Questions：未解問題、需使用者決策的事
5. **依 PARA 移動**：用 [para-classify](para-classify.md) 判斷，必要時搬到對應資料夾
6. **同步目錄**：用 [toc-sync](toc-sync.md) 更新對應 `目錄.md`

## 完成條件

- 筆記讓人 10 秒內看懂重要性、1 分鐘內找到重點
- 有來源、摘要、萃取、可能用途
- `status` 反映實際整理程度
- 對應 `目錄.md` 已同步

## 注意事項

- 不只輸出摘要，盡量包含 implications、action items、possible outputs
- 不刪除使用者原始資料，除非使用者明確要求
- 分類假設要在筆記中簡短註明；需使用者決定時放 Inbox 並列問題
- 連結只連真正有助回顧或輸出的筆記，不為了連而連
- 預設用標準 Markdown 連結，不依賴 Obsidian 語法
