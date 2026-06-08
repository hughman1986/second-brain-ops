---
name: para-classify
description: 判斷筆記應該屬於 Project / Area / Resource / Archive / Inbox
when_to_use:
  - 整理 Inbox 筆記時決定該放哪
  - 使用者問「這份筆記應該放哪」「這算 Project 還是 Resource」
  - code-distill-note 流程的 Organize 步驟
inputs:
  - 筆記內容或主題
outputs:
  - 分類結果與理由，必要時列出需使用者決定的問題
related:
  - skills/code-distill-note.md
  - skills/toc-sync.md
  - AGENTS.md「PARA 結構」
---

# PARA Classify

## PARA 定義

```text
00_Inbox/      尚未整理、歸類不明、來源不完整、需確認
10_Projects/   有成果、期限、完成條件；完成後封存
20_Areas/      長期維護的責任領域，無明確結束時間
30_Resources/  未來可能有用的主題、研究素材、參考內容
40_Archives/   已完成、暫停、過期、不活躍但可查找
90_Outputs/    由筆記轉化出的文章、簡報、memo、SOP、報告等成果
```

## 判斷樹（依序判斷，命中即停）

```text
這會幫助我完成某個有期限或成果的事情嗎？ → 10_Projects
這是需要長期維持或負責的領域嗎？           → 20_Areas
這是未來可能有用的主題、素材或參考嗎？     → 30_Resources
這已完成、暫停、過期或不活躍嗎？           → 40_Archives
還不確定？                                  → 00_Inbox，標 needs-review
```

## 執行步驟

1. 讀筆記內容、frontmatter、相關上下文
2. 套用判斷樹（**依序**判斷，不要跳）
3. 特殊規則：
   - **不要只因主題相似就放 Resources**，先判斷是否支援 active project 或 ongoing area
   - 設備專案：工單才是 PARA 意義上的 active project（不是機種）
   - 由筆記轉出的可交付成果 → `90_Outputs/`
4. 輸出：
   - 建議分類 + 一段理由
   - 若需使用者決定（例如是否還是 active project），放 Inbox 並列出問題
5. 若決定移動，後續用 [code-distill-note](code-distill-note.md) 更新 frontmatter `para` 欄位，並用 [toc-sync](toc-sync.md) 同步目錄

## 完成條件

- 明確分類結果
- 有理由說明
- 不確定時不硬分，回到 Inbox + needs-review

## 注意事項

- 不要為了「乾淨」硬把 Inbox 清空；不確定就留著
- 分類隨時可變更：完成的 Project 進 Archive；長期維護的責任進 Area
