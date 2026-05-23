---
title: "{{project_name}}"
created: 2026-05-23
updated: 2026-05-23
para: project
status: planning
project_type: equipment-software
machine_model:
work_order_id:
customer:
site:
tool_id:
owner:
deadline:
tags:
  - equipment-project
  - software
---

# {{project_name}}

## Project Snapshot

| Field | Value |
| --- | --- |
| Customer |  |
| Site |  |
| Machine Model |  |
| Work Order ID |  |
| Equipment / Tool ID |  |
| Software Scope | PLC / HMI / motion / vision / SECS-GEM / data collection / recipe / other |
| Current Stage | 開工 |
| Target Release Date |  |
| Project Owner |  |
| Software Owner |  |
| Mechanical / Electrical Owner |  |
| Customer Contact |  |

## Outcome

這個專案完成時，設備軟體與現場整合應達到什麼可交付狀態？

## Success Criteria

- [ ] 設備可依規格完成機台測試。
- [ ] 客戶端完成 move in、組裝送電與整合測試。
- [ ] 主要 issue 已關閉或有客戶接受的 workaround。
- [ ] 產線 release 條件已確認。

## Scope

### In Scope

- 

### Out of Scope

- 

## Software Scope

| Module | Scope | Owner | Status | Notes |
| --- | --- | --- | --- | --- |
| PLC / sequence |  |  | not-started |  |
| HMI |  |  | not-started |  |
| Motion / robot |  |  | not-started |  |
| Vision / inspection |  |  | not-started |  |
| IO / interlock |  |  | not-started |  |
| Recipe / parameter |  |  | not-started |  |
| Data / traceability |  |  | not-started |  |
| Host / SECS-GEM |  |  | not-started |  |

## Current Status

### Summary

目前進度、主要風險、下一個關鍵節點。

### Next Actions

- [ ] 

### Blockers

- 

## Key Links

- [裝機時程](schedule.md)
- [任務清單](tasks.md)
- [Issue List](issues.md)
- [決策紀錄](decisions.md)
- [會議紀錄](meetings.md)
- [專案資源](resources.md)
- [專案輸出](outputs/)
- [機種總覽](../model.md)
- [機種共用資源](../common-resources.md)

## Review Rhythm

- Daily check：檢查 `schedule.md` 中 `remind_on` 到期或逾期項目。
- Weekly review：更新目前 stage、issue aging、下週關鍵任務。
- Stage gate review：每個裝機階段完成前，確認 `Exit Criteria` 與未關閉 issue。

## Notes

- 分類假設：此模板用於單一工單；工單是 PARA 意義上的 project，建議放在 `10_Projects/<machine-model>/<work-order-id>/`。
