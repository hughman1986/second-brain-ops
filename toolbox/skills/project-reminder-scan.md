---
name: project-reminder-scan
description: 處理專案進度、週報、提醒或逾期項目的固定 5 步驟流程
when_to_use:
  - 使用者問「目前專案狀態」「本週要注意什麼」「哪些 issue 逾期」
  - 要寫週報、daily standup、stage gate 檢查
  - 使用者提到「提醒」「逾期」「risk」「阻塞」相關詞
inputs:
  - 可選：基準日期、向後天數
outputs:
  - 整理後的風險、逾期項目、next actions、需使用者決策的問題
related:
  - toolbox/project_reminder_scan.py
  - 10_Projects/目錄.md
  - AGENTS.md「設備專案管理」
  - skills/stage-gate-check.md
---

# Project Reminder Scan

## 觸發情境

任何與「專案進度 / 提醒 / 週報 / 逾期 / 阻塞」相關的請求。

## 執行步驟

1. **先讀 `10_Projects/目錄.md`**，掌握目前有哪些機種與工單、各自目前階段。
2. **執行提醒掃描**：
   ```powershell
   & "$env:USERPROFILE\.venvs\sb-docs\Scripts\python.exe" toolbox/project_reminder_scan.py
   ```
   若使用者指定日期或天數：
   ```powershell
   & "$env:USERPROFILE\.venvs\sb-docs\Scripts\python.exe" toolbox/project_reminder_scan.py --date 2026-05-23 --days 14
   ```
   工具會遞迴掃描 `10_Projects/**/schedule.md` 與 `issues.md`，依 `Target Date`、`Remind On`、`Status` 找提醒與逾期。`done` / `closed` / `cancelled` / `canceled` / `skipped` 不列入。
3. **針對掃描結果**，對每個有提醒、逾期或阻塞的工單：
   - 先讀對應機種 `目錄.md`
   - 再讀工單的 `schedule.md`、`issues.md`
4. **必要時補充背景**：讀工單 `decisions.md`、`meetings.md`、`resources.md` 或機種 `common-resources.md`。
5. **整理輸出**給使用者：
   - 風險（critical / high issue 未關閉）
   - 逾期項目（owner、target date、目前 status）
   - Next actions（誰負責、何時前做完）
   - 需使用者決策的問題

## 完成條件

- 涵蓋所有掃描出的提醒/逾期項目
- 每項都有 owner、next action、阻塞原因（如有）
- 明確標出需使用者決策的問題

## 注意事項

- 不主動修改 `schedule.md` 或 `issues.md`，除非使用者明確要求
- 不跳過步驟 1（不能直接跳到跑工具）
- 整理時應用 [stage-gate-check](stage-gate-check.md) 判斷是否可進下一階段
