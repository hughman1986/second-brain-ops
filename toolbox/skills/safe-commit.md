---
name: safe-commit
description: git commit 前強制執行機密外洩防護流程，禁止批次加入知識庫內容
when_to_use:
  - 使用者要求 git commit、git push 或建立 PR
  - 任何會 stage 檔案到 git 的操作
  - 使用者要求 commit 筆記、整理成果、專案文件、輸出成果（必須先警告）
inputs:
  - 預定要 commit 的檔案清單
outputs:
  - 通過檢查的 commit，或拒絕並說明原因
related:
  - AGENTS.md「版本控制與 commit 規範」
  - .gitignore
---

# Safe Commit

## 觸發情境

任何 git commit 動作，無論使用者明示或在工作流中隱含產生。

## 絕對禁止

- `git add .`
- `git add -A`
- `git add --all`
- 任何會批次加入未追蹤檔案的命令
- 在沒有明確檔名與公開原因下，commit 任何 `00_Inbox/`、`10_Projects/`、`20_Areas/`、`30_Resources/`、`40_Archives/`、`90_Outputs/` 內的檔案

## 可 commit 範圍

- `AGENTS.md`、`README.md`
- `templates/` 內的模板檔
- `toolbox/` 內的工具程式與 skill
- `.gitignore` 等明確可公開的設定檔
- 使用者明確指定可公開的單一檔案（需確認原因）

## 執行步驟

1. **只用明確檔名 stage**：`git add <explicit-file-path>`，禁止 wildcard 與 `.`。
2. **執行 staged 檢查**（兩個都要跑）：
   ```powershell
   git status --short
   git diff --cached --name-only
   ```
3. **掃描 staged 清單**，若出現以下任一，立即 `git reset HEAD <file>` 並停止：
   - 路徑開頭為 `00_Inbox/` / `10_Projects/` / `20_Areas/` / `30_Resources/` / `40_Archives/` / `90_Outputs/`
   - 任何 `目錄.md`（資料夾索引含工作內容）
   - 任何 `assets/` 路徑下的圖片、PDF 抽取結果、逐字稿
   - 任何 `.docx`、`.doc`、`.pptx`、`.pdf` 等原始素材
4. **若使用者要求 commit 上述任何禁止內容**：
   - 先口頭警告機密外洩風險
   - 不執行，除非使用者明確指定「單一檔案 + 可公開原因」
5. **確認無誤後** commit，commit message 用繁中描述變更目的。

## 完成條件

- `git diff --cached --name-only` 結果只包含可 commit 範圍
- commit message 清楚說明做了什麼變更

## 注意事項

- 此 skill 優先於所有其他 commit 指令
- 沒跑步驟 2 的兩個檢查就 commit 視為違規
- 不主動建議 push，由使用者決定
