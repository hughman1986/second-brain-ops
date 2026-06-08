---
name: stage-gate-check
description: 設備裝機 10 階段 gate 檢查，判斷是否可進下一階段
when_to_use:
  - 使用者問「可以進下一階段嗎」「能 release 嗎」
  - 寫週報、stage gate review、出貨前檢查
  - project-reminder-scan 之後的後續判斷
inputs:
  - 工單路徑或 ID
outputs:
  - 目前階段、下一階段、gate pass/blocked、阻塞原因
related:
  - skills/project-reminder-scan.md
  - 10_Projects/<machine-model>/<work-order-id>/schedule.md
  - 10_Projects/<machine-model>/<work-order-id>/issues.md
---

# Stage Gate Check

## 標準 10 階段

```text
1. 開工
2. 開 BOM
3. 組裝配線
4. 送電
5. IO Check
6. 機台測試
7. 交機 move in
8. 客戶端組裝送電
9. 整合測試
10. release 產線
```

## Gate 規則

- 每個階段都有 `Target Date`、`Remind On`、`Owner`、`Status`
- **`critical` 或 `high` issue 未關閉時，不應進下一個 stage gate**
  - 例外：已有明確 workaround，且 workaround 已記錄在 `decisions.md`
- 影響時程的問題必須寫入 `issues.md` 並連回對應 stage

## 執行步驟

1. 讀目標工單的 `schedule.md`，找出目前 stage（最後一個 `Status` 非 `done` 的階段）
2. 讀 `issues.md`，過濾出 status 非 `done/closed/cancelled` 的 `critical` 或 `high` issue
3. 判斷 gate：
   - 無 critical/high open issue → **可進下一階段**
   - 有 open critical/high issue → **blocked**，列出每個 issue 的 owner、next action、target date
   - 有 workaround 已記錄 → **conditionally pass**，註明 workaround 與長期解法
4. 同步更新：
   - 工單 `schedule.md`：階段 Status
   - 機種 `目錄.md`：目前階段、下一步、風險
   - `10_Projects/目錄.md`：跨工單 dashboard

## 完成條件

- 明確輸出 pass / blocked / conditionally pass
- 列出所有阻塞 issue 與 next action
- 相關目錄已同步（透過 [toc-sync](toc-sync.md)）

## 注意事項

- 不擅自將 issue 標為已解決；只判斷狀態
- release 產線階段需特別嚴格，所有 critical/high 必須 closed，不接受 workaround
