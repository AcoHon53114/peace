# 第二階段：Admin 儲存成功後通知 Pages 同步

此更新只加入消息／院友心聲 Admin 的通知工具及三語狀態提示。前台模板、CSS、JavaScript、圖片、模型、migration、依賴及第一階段 workflow 保持原樣。

## 更新後的行為

| Admin 操作 | GitHub 同步通知 |
| --- | --- |
| 新增已公開消息／心聲 | 發送 |
| 修改已公開項目的三語文字、圖片或其他內容欄位 | 發送 |
| 草稿改為公開 | 發送 |
| 公開改為不公開 | 發送，讓展示版移除舊內容 |
| 刪除公開項目，包括批量刪除 | 發送 |
| 只新增／修改／刪除未公開草稿 | 不發送 |
| 開啟表單後沒有改動，直接儲存 | 不發送 |
| 修改用戶、密碼、付款、預約或其他模型 | 不發送 |
| Preview／Development／本機操作 | 不發送 |

只在資料庫交易真正提交成功後發送。驗證失敗或交易回滾不通知。同一次列表儲存／批量刪除只註冊一次通知。

GitHub 接受通知時，Admin 顯示「內容已儲存，已提出展示網站同步要求；發布可能需要幾分鐘。」若 GitHub 超時／權限錯誤／憑證未設定，資料仍儲存成功，Admin 顯示警告，保留原有儲存成功訊息。

「立即通知」不等於立即上線：GitHub 仍需排隊、抓取三語公開頁、比對、發布。第一階段每小時檢查和 Run workflow 都繼續保留。GitHub 接受 API 要求亦不代表後續 Pages 發布一定成功，最終結果以 Actions Logs 為準。

## 第 1 步：確認第一階段

開啟 https://github.com/AcoHon53114/peace/actions ，確認 **Publish Peace frontend demo** 可正常執行。

先確認一次發布成功，再次相同內容顯示 `Public content/assets unchanged: publication skipped.`。如果第一階段尚未設定好，先處理第一階段，再啟用第二階段。

`.github/workflows/pages-demo.yml` 要在 `main` 上，並保留 `workflow_dispatch`。這次直接使用原有 workflow，不增加另一個發布流程。

## 第 2 步：套用更新包

先備份目前專案，再把解壓出的 `peace-pages-stage2-update/` 內檔案，按同樣相對路徑放入 `~/Desktop/peace`，覆蓋同名檔案。

包含：

- `peaceweb/pages_sync.py`：新通知工具及 Admin mixin。
- `peaceweb/settings.py`：末尾新增 6 個通知設定；其餘沿用上一個交付版本。
- `news/admin.py`、`environments/admin.py`：接入通知 mixin；原有欄位、搜尋、篩選及列表不變。
- `locale/en/LC_MESSAGES/django.po`、`django.mo`。
- `locale/zh_Hant/LC_MESSAGES/django.po`、`django.mo`。
- `locale/zh_Hans/LC_MESSAGES/django.po`、`django.mo`。
- `pages/test_pages_sync.py`：離線回歸測試。
- `PAGES_STAGE2_GUIDE.md`：本指引。

如果你自行修改過 `settings.py` 或兩份 Admin 檔案，先查看 diff 合併本次新增區域，保留自己的設定。原有 `.env.local`、GitHub Pages 工具及環境變數保持原樣。

這次 **不需要 migrate、不需要 makemigrations、不需要改 requirements.txt**。翻譯 `.mo` 已編譯，不需要在 Vercel 安裝 gettext。

## 第 3 步：建立 GitHub fine-grained Token

這是新增的 **GitHub Token**，與第一階段的 Vercel Token 不同。

1. 登入 GitHub 的 `AcoHon53114` 帳戶。
2. 開啟 https://github.com/settings/personal-access-tokens ，或頭像 → Settings → Developer settings → Personal access tokens → Fine-grained tokens。
3. 按 **Generate new token**。
4. Token name：`peace-admin-pages-sync`。
5. 選擇到期日期，例如先用 30 天；到期前要更新 Vercel 中的值。
6. Resource owner 選擁有 repo 的 `AcoHon53114`。
7. Repository access 選 **Only select repositories**，只選 **peace**。
8. Repository permissions → **Actions** 選 **Read and write**。Metadata 的 Read-only 由 GitHub 自動要求；其他權限保留不授權，不需要 Contents Write。
9. 按 **Generate token**，立即複製完整 Token。

Token 本身授權的是該 repo 的 Actions 寫入操作，不是保證只能觸發一個 workflow；本工具只使用它觸發 `pages-demo.yml`，不操作程式碼或其他 workflow。

不要把 Token 寫到任何程式碼、README、workflow、前端或 Git commit；不要貼到聊天室或截圖。Token 只會在建立時顯示一次，遺失可建立新 Token。

## 第 4 步：把 GitHub Token 放入 Vercel Production

1. 開啟 Vercel Dashboard。
2. 選擇正式網域為 **peace-beta-sandy.vercel.app** 的專案。
3. Settings → **Environment Variables**。
4. 加入以下兩項，只勾 **Production**，不要勾 Preview／Development。

| Key | Value | Environment |
| --- | --- | --- |
| `PEACE_PAGES_SYNC_ENABLED` | `true` | Production |
| `PEACE_PAGES_GITHUB_TOKEN` | 第 3 步的完整 GitHub Token | Production |

值不要加引號；Token 不要加 `Bearer ` 前綴。如果畫面提供 Sensitive 選項，Token 可設為 Sensitive。通知工具只在後端讀取此值，不會放入 HTML。

以下三項有預設值，不必新增；只有 repo／workflow／分支改名時才需要修改：

| 可選 Key | 預設 Value |
| --- | --- |
| `PEACE_PAGES_GITHUB_REPOSITORY` | `AcoHon53114/peace` |
| `PEACE_PAGES_GITHUB_WORKFLOW` | `pages-demo.yml` |
| `PEACE_PAGES_GITHUB_REF` | `main` |

在 Environment Variables 頁面確認 **Enable access to System Environment Variables** 已啟用。工具以 Vercel 系統提供的 `VERCEL_ENV=production` 判斷正式環境；不要自行新增或覆蓋 `VERCEL_ENV`。若系統變數未開啟，工具會保持不通知。

不要把 GitHub Token 加到另一個 peace 專案。第二階段這兩項放在 Vercel；第一階段的 `VERCEL_TOKEN` 和 Project ID 仍放在 GitHub Actions，保持原有設定。

環境變數只會套用到後續部署，因此接著要 push 新程式，或在已 push 後再 Redeploy Production 一次。

## 第 5 步：提交程式及部署

在 Terminal：

```bash
cd ~/Desktop/peace
source .venv/bin/activate
python manage.py check

git status --short
git diff --stat
git add peaceweb/pages_sync.py peaceweb/settings.py news/admin.py environments/admin.py pages/test_pages_sync.py locale/en/LC_MESSAGES/django.po locale/en/LC_MESSAGES/django.mo locale/zh_Hant/LC_MESSAGES/django.po locale/zh_Hant/LC_MESSAGES/django.mo locale/zh_Hans/LC_MESSAGES/django.po locale/zh_Hans/LC_MESSAGES/django.mo PAGES_STAGE2_GUIDE.md
git diff --cached --stat
git commit -m "Notify Pages workflow after committed public Admin content changes"
git push origin main
```

確認沒有 `.env.local`、Token、SQLite 或 QA 檔案被 staged。等 Vercel Production 成功。如果第 4 步的變數在這次部署後才加入，請再 Redeploy。

本機設定不包含 Vercel Production 系統值，通知預設關閉。不要在本機設定 `VERCEL_ENV=production` 來測試真實通知。

## 第 6 步：驗證即時通知

1. 登入 https://peace-beta-sandy.vercel.app/admin/ 。
2. 按正常需要修改一則**已公開消息／心聲**，例如更新英文正文；不必新增假消息。
3. 按儲存。
4. 應同時看到 Django 原有儲存成功訊息及新的同步要求提示。此提示支援繁中、簡中、英文。
5. 打開 https://github.com/AcoHon53114/peace/actions 。
6. 確認 **Publish Peace frontend demo** 新增一次執行。GitHub UI 可能把它顯示為手動／workflow_dispatch，因為使用與 Run workflow 相同的觸發方式，不會必然標成 Admin。
7. 等執行成功，開啟 https://acohon53114.github.io/peace/ ，到同一頁查看更新內容及三語版本。
8. 沒有實際改動時再按儲存，不會發送通知；草稿修改也不會發送。
9. 取消公開或刪除時，等待同步後確認展示版列表／頁面已移除該項。

連續儲存數次可能提出多個要求；GitHub 沿用第一階段 concurrency 排隊／合併待執行工作，每次抓取最新公開內容並比較，內容相同便跳過發布。不是每一次 API 通知都保證有獨立完成的發布紀錄。

## 第 7 步：通知失敗怎樣處理

- **內容已儲存，但通知失敗**：毋須重複按儲存。先確認正式網站內容已更新；可以到 GitHub Run workflow，或等每小時檢查。
- **GitHub HTTP 401／403**：Token 無效／到期、沒有授權 peace repo 或缺少 Actions Write。更新 Vercel Token 值後重新部署。
- **GitHub HTTP 404**：repo／workflow 名稱不對、Token 沒有存取權、workflow 不在預期 repo。
- **GitHub HTTP 422**：branch `main` 不存在或 workflow 不支援 `workflow_dispatch`。
- **沒有提示，也沒有新執行**：先確認真的改了公開內容、Production 變數 `PEACE_PAGES_SYNC_ENABLED=true`、系統環境變數開啟，以及已重新部署。
- **收到同步要求提示，但 Pages 沒更新**：查看 GitHub workflow Logs。提示只表示 GitHub 接受要求，不表示抓取／部署成功。第一階段的 Vercel Token、Project ID、媒體連結等問題仍會令該次執行失敗。
- **想暫時停用**：Vercel Production 把 `PEACE_PAGES_SYNC_ENABLED` 改為 `false`，重新部署。Admin 儲存及第一階段同步保持運作。

HTTP 請求設定 4 秒網絡逾時，不在同一次 Admin 操作中重試。這是網絡操作逾時設定，不是保證整個儲存流程在 4 秒內完成。通知在回應前發送，可能令 Admin 儲存多等一小段時間；前台正常讀取不會呼叫這個 GitHub API。

沒有新增背景 thread、常駐 worker、公開通知 endpoint 或資料庫 outbox。若程序在提交後、通知前意外終止，這次即時通知可能遺漏，保留每小時檢查補同步。沒有宣稱保證 exactly-once。

## 測試及範圍

只在獨立本機 SQLite 和模擬 GitHub 連線驗證；沒有連接正式 Neon、使用你的 Token、改正式 Admin 資料或部署 GitHub／Vercel。

`pages/test_pages_sync.py` 已包含測試。若自行執行 `python manage.py test pages.test_pages_sync`，只在獨立本機測試資料庫設定下執行；不要用正式 Neon DATABASE_URL 跑測試。

本包只有 scoped 更新檔，套用到現有已完成三語的 Django 專案；不是獨立完整 Django repo，不需要刪除或重建你的專案。

## 官方參考

- GitHub workflow dispatch／Actions Write：https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event
- GitHub fine-grained Token：https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
- Django transaction.on_commit：https://docs.djangoproject.com/en/5.2/topics/db/transactions/#performing-actions-after-commit
- Vercel System Environment Variables：https://vercel.com/docs/environment-variables/system-environment-variables

## 本次完成檢查

- 34 項新增 Pages 通知測試及 18 項既有三語／Admin／migration 測試，共 52 項通過。
- 包含真正交易提交後才通知、交易回滾不通知，以及實際 Admin 回應能保留成功／失敗提示。
- 新增／修改／公開／取消公開、草稿、未改動儲存、圖片更新、單筆及批量刪除、列表批量儲存、其他 Admin 模型均驗證。
- GitHub HTTP 拒絕、網絡逾時、缺少 Token、意外例外、禁止跟隨 redirect 和錯誤記錄不洩漏 Token 均驗證。
- Django check 通過；makemigrations --check --dry-run 顯示 No changes detected；三語 .mo 編譯及 Python 語法檢查通過。
- Chromium：兩種內容模型 × 三種 Admin 語言 × 三種主題 × 成功／失敗提示 × 五種寬度，共 180 組，未發現整頁橫向溢出或提示超出畫面；語言控制維持可見。
- 另檢查五個代表前台頁 × 三語 × 五個寬度，共 75 組 responsive，語言選單未超出畫面。
- 寬度為 375、390、768、1024、1440px；第三方 Maps／CDN 請求在本機版面測試攔截。沒有實機 iPhone Safari 測試。
- 逐檔 hash 確認前台模板、CSS、JS、圖片、模型、migration 及依賴不變。本次只有上述 12 個更新／新增檔。
- ZIP 解壓完整性檢查通過，沒有 Token、Git、虛擬環境、資料庫或 QA 暫存檔。
- 未在你的帳戶執行真實 GitHub 通知或正式部署；最後端到端驗證請按第 6 步完成。
