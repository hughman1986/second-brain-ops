---
title: "{{project_name}} - 裝機時程追蹤"
created: 2026-05-23
updated: 2026-05-23
para: project
status: tracking
tags:
  - schedule
  - equipment-installation
  - reminder
---

# {{project_name}} - 裝機時程追蹤

## Reminder Rules

- `target_date` 前 3 天：確認前置條件、owner、風險。
- `target_date` 當天：確認是否完成，未完成要新增或更新 issue。
- `target_date` 後仍非 `done`：標記 `overdue`，並在 `issues.md` 建立阻塞項。
- 每次更新時，同步更新機種資料夾 `目錄.md` 與 `10_Projects/目錄.md` 的「目前階段」、「下一步」、「風險/阻塞」。

## Stage Timeline

| # | Stage | Status | Target Date | Actual Date | Remind On | Owner | Exit Criteria | Risk / Blocker | Related Issues |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 開工 | not-started |  |  |  |  | 專案範圍、窗口、初版時程確認 |  |  |
| 2 | 開 BOM | not-started |  |  |  |  | 軟體相關料號、電控料件、長交期項目確認 |  |  |
| 3 | 組裝配線 | not-started |  |  |  |  | 電控箱、機台配線、label、接線圖版本確認 |  |  |
| 4 | 送電 | not-started |  |  |  |  | 送電檢查完成，無重大電氣異常 |  |  |
| 5 | IO Check | not-started |  |  |  |  | IO 點位、sensor、actuator、interlock 完成確認 |  |  |
| 6 | 機台測試 | not-started |  |  |  |  | sequence、alarm、recipe、cycle test 達標 |  |  |
| 7 | 交機 move in | not-started |  |  |  |  | 出貨/進廠條件、文件、版本、備品確認 |  |  |
| 8 | 客戶端組裝送電 | not-started |  |  |  |  | 客戶端組裝、復機、送電與安全確認完成 |  |  |
| 9 | 整合測試 | not-started |  |  |  |  | 與上下游、host、產線條件整合測試完成 |  |  |
| 10 | release 產線 | not-started |  |  |  |  | 客戶接受 release，未結 issue 有處置方案 |  |  |

## Reminder Queue

| Reminder Date | Item | Stage | Owner | Action Needed | Status |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | open |

## Stage Gate Checklist

### 開工

- [ ] 專案目標與交付範圍確認。
- [ ] 軟體責任邊界確認。
- [ ] 客戶窗口與內部 owner 確認。
- [ ] 初版裝機時程建立。

### 開 BOM

- [ ] 軟體/電控相關料號確認。
- [ ] 長交期料件與替代方案確認。
- [ ] IO list / electrical drawing 版本確認。

### 組裝配線

- [ ] 電控箱與現場配線完成。
- [ ] 線號、端子、圖面版本一致。
- [ ] 初步安全回路確認。

### 送電

- [ ] 送電前檢查完成。
- [ ] 電源、接地、保護元件確認。
- [ ] 異常紀錄已寫入 `issues.md`。

### IO Check

- [ ] Digital input/output 確認。
- [ ] Analog / communication signal 確認。
- [ ] Safety / interlock 確認。
- [ ] IO 異常已追蹤到 owner。

### 機台測試

- [ ] 單動與自動流程測試。
- [ ] Alarm / recovery 流程測試。
- [ ] Recipe / parameter 測試。
- [ ] Cycle time / repeatability 初步確認。

### 交機 move in

- [ ] 出貨版本與現場版本確認。
- [ ] 備份程式、參數、文件完成。
- [ ] 客戶端 move in 條件確認。

### 客戶端組裝送電

- [ ] 現場組裝完成。
- [ ] 客戶端送電檢查完成。
- [ ] 現場差異與 issue 已紀錄。

### 整合測試

- [ ] 上下游設備介面確認。
- [ ] Host / MES / SECS-GEM 或資料介面確認。
- [ ] 產線情境測試完成。

### release 產線

- [ ] 客戶 release 條件確認。
- [ ] Open issue 風險分級完成。
- [ ] 程式、文件、參數、交接資料封版。

## Change Log

| Date | Change | Reason | Owner |
| --- | --- | --- | --- |
|  |  |  |  |
