---
name: equipment-new-work-order
description: 建立新機種或新工單的標準化流程，使用既有 template
when_to_use:
  - 使用者要建立新機種、新工單
  - 使用者提到新訂單、新案子、新的設備出貨
inputs:
  - 機種代號 (machine-model)
  - 工單編號 (work-order-id)
  - 客戶、目標交期、Owner 等基本資訊
outputs:
  - 完整的工單資料夾結構與初始化內容
  - 更新後的機種 目錄.md 與 10_Projects/目錄.md
related:
  - templates/equipment-model-template/
  - templates/equipment-project-template/
  - 10_Projects/目錄.md
  - AGENTS.md「設備專案管理」
---

# Equipment New Work Order

## 觸發情境

建立新機種或新工單時。設備軟體專案採「機種 / 工單」兩層結構，工單才是 PARA 意義上的 active project。

## 目錄結構

```text
10_Projects/
  <machine-model>/
    目錄.md
    model.md
    common-resources.md
    <work-order-id>/
      project.md
      schedule.md
      issues.md
      tasks.md
      decisions.md
      meetings.md
      resources.md
      outputs/
```

## 執行步驟

### A. 新機種（首次出現的機種）

1. 確認 `10_Projects/<machine-model>/` 尚未存在
2. 複製 `templates/equipment-model-template/` → `10_Projects/<machine-model>/`
3. 編輯 `model.md`：機種規格、共用資料
4. 編輯 `common-resources.md`：圖面、IO list、共用程式版本
5. 初始化機種 `目錄.md`：工單 dashboard 表頭
6. 進入 B 流程建立第一張工單

### B. 新工單

1. 確認 `10_Projects/<machine-model>/<work-order-id>/` 尚未存在
2. 複製 `templates/equipment-project-template/` → `10_Projects/<machine-model>/<work-order-id>/`
3. 更新檔案：
   - `project.md`：專案總覽、範圍、owner、release 條件
   - `schedule.md`：依標準 10 階段填 `Target Date` / `Remind On` / `Owner` / `Status`
   - `issues.md`：已知 issue（嚴重度、owner、next action、target date）
   - `tasks.md`：Next Actions / Waiting / Scheduled / Done 四區
   - `decisions.md`、`meetings.md`、`resources.md`：先建空骨架
4. 更新機種 `目錄.md`：加入此工單列、目前階段、下一步、風險
5. 更新 `10_Projects/目錄.md`：跨機種 dashboard 加新工單

## 標準 10 階段

```text
開工 > 開 BOM > 組裝配線 > 送電 > IO Check > 機台測試 > 交機 move in > 客戶端組裝送電 > 整合測試 > release 產線
```

每個階段都必須有 `Target Date`、`Remind On`、`Owner`、`Status`。

## 完成條件

- 工單資料夾結構完整，所有必要檔案存在
- `schedule.md` 10 階段都有日期與 owner
- 機種 `目錄.md` 與 `10_Projects/目錄.md` 都已更新

## 注意事項

- 不直接編輯 templates；只複製
- 資訊不足時，在對應檔案標 `TBD`，並列入需使用者補的問題
- 建立完成後，後續進度更新走 [project-reminder-scan](project-reminder-scan.md)
