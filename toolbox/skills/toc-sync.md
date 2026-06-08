---
name: toc-sync
description: 新增、更新、移動、封存或刪除筆記後，同步更新對應資料夾的 目錄.md
when_to_use:
  - 在 00_Inbox/ / 10_Projects/ / 20_Areas/ / 30_Resources/ / 40_Archives/ / 90_Outputs/ 內新增、更新、移動、封存或刪除筆記
  - capture-* / code-distill-note / para-classify / equipment-* 流程的後置步驟
inputs:
  - 變動的筆記路徑與類型（new / update / move / archive / delete）
outputs:
  - 已同步的對應 目錄.md
related:
  - AGENTS.md「索引規則」
---

# TOC Sync

## 觸發情境

任何對 PARA 資料夾內容的變動。**這是所有寫入動作的後置步驟，不可省略**。

## 目錄.md 規則

每個主要資料夾都必須有 `目錄.md`：

```text
00_Inbox/目錄.md
10_Projects/目錄.md
20_Areas/目錄.md
30_Resources/目錄.md
40_Archives/目錄.md
90_Outputs/目錄.md
```

`目錄.md` **只放高密度摘要**，不放全文。

## 標準格式

```markdown
# <資料夾名> 目錄

## 用途
（這個資料夾收什麼、不收什麼）

## 瀏覽重點
（給 AI 與使用者的速覽提示）

## 索引

| 筆記 | 狀態 | 摘要 | 更新日期 | 可能用途 |
|---|---|---|---|---|
| [檔名](檔名.md) | distilled | 一行摘要 | 2026-06-08 | 文章 / SOP / 決策 |

## AI 檢索提示
（找這類資料時應該優先看哪幾筆、忽略哪幾筆）
```

## 執行步驟

1. 找到變動筆記所屬的 `目錄.md`（可能不只一個，跨資料夾移動要更新來源與目的兩個）
2. 對應變動類型更新：
   - **new**：在索引表加一列
   - **update**：更新該列的「狀態 / 摘要 / 更新日期」
   - **move**：來源目錄移除該列、目的目錄新增該列
   - **archive**：來源目錄移除、`40_Archives/目錄.md` 新增
   - **delete**：移除該列
3. 視需要更新「AI 檢索提示」段
4. 確認檔案為 UTF-8 編碼

## 完成條件

- 對應 `目錄.md` 與實際資料夾內容一致
- 索引表欄位完整（筆記 / 狀態 / 摘要 / 更新日期 / 可能用途）

## 注意事項

- 檢索資料時**先讀目錄，只有相關時才讀完整筆記**
- 不在 `目錄.md` 放全文，只放高密度摘要
- 設備專案有兩層目錄：機種 `目錄.md` 與 `10_Projects/目錄.md`，工單變動要同步兩層
- 部分 capture 工具（PPTX、Word）**不會**自動更新目錄，必須手動跑此 skill
