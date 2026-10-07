# 第一階段：Peace GitHub Pages 自動同步

這個包只更新 Pages 展示版的工具和 workflow。Django 模型、後台、資料庫、CSS、版面和原有 JavaScript 不作改動。三語靜態頁繼續沿用正式網站的響應式樣式和語言按鈕。

## 完成後的日後更新方式

| 你做的事 | 自動處理 |
| --- | --- |
| 修改程式後 push | Vercel 成功部署到 Production 後，Pages workflow 讀取目前正式版本並更新展示版 |
| Admin 更新已公開消息／心聲 | 每小時第 23 分鐘（UTC；香港同樣第 23 分鐘）檢查三語公開頁；有變更才發布 |
| 想立即同步 | GitHub Actions → Publish Peace frontend demo → Run workflow → main |
| 沒有公開內容／圖片／樣式變更 | workflow 執行比對，但跳過 Pages 發布 |

第一階段尚未加入「Admin 儲存後立即觸發」。那是第二階段，這次不修改 Admin 儲存流程。

## 第 1 步：放入專案

解壓後把以下檔案放到 `~/Desktop/peace`，保留子資料夾結構。若已有同名 Pages 工具，覆蓋同名檔案；其他檔案保持原樣。

```text
peace/
  .github/workflows/pages-demo.yml
  tools/export_pages.py
  tools/pages_automation.py
  tools/test_pages_automation.py
  PAGES_GUIDE.md
```

macOS Finder 按 Command + Shift + . 可顯示 `.github`。

開啟專案 `.gitignore`，若沒有以下項目，加入一次：

```gitignore
_site/
_site-preview*/
.pages-state.json
.pages-last/
deployed-source/
```

`.pages-state.json` 和 `.pages-last/` 是本機測試／workflow 的中間資料，不需要提交。Vercel Token 不要寫入任何程式檔案或 `.env` 後提交。

## 第 2 步：取得正確的 Vercel Project ID

1. 開啟 Vercel，選擇正式網址為 `peace-beta-sandy.vercel.app` 的專案。
2. 在 Settings → General 找到 Project ID，例如 `prj_…`，複製完整值。
3. 如果帳戶下有另一個 peace 專案，請不要混用另一個專案的 ID。
4. 如專案屬於 Team，在該 Team 的 Settings → General 取得 Team ID（`team_…`）。個人專案如果 API 要求 Team scope，同樣填寫擁有專案的 Team ID。

## 第 3 步：建立 Vercel Token

1. 前往 https://vercel.com/account/settings/tokens 。
2. 建立 Token，名稱可用 `peace-pages-metadata`。
3. Scope 選擇擁有上述專案的帳戶／Team，選擇合適的到期日期。
4. 複製 Token，下一步放到 GitHub Secret。

工具只呼叫 Vercel 的 GET API，確認正式網域目前指向哪個部署，以及該部署的 Git commit。不會呼叫部署、刪除、更新設定的 API。不過 Vercel Token 本身的權限由你建立時的 Scope 決定，不能把普通 Token 當作必然只有唯讀權限；請只選需要的帳戶／Team，不要公開它。Token 到期後要在 GitHub 更新 Secret。

不需要提供 Neon 密碼、DATABASE_URL、Django SECRET_KEY 或 Admin 登入資料。

## 第 4 步：加入 GitHub Actions Secret 和 Variables

開啟 https://github.com/AcoHon53114/peace → Settings → Secrets and variables → Actions。

在 **Secrets** 分頁按 **New repository secret**：

| Name | Secret |
| --- | --- |
| `VERCEL_TOKEN` | 第 3 步的 Vercel Token |

在 **Variables** 分頁按 **New repository variable**：

| Name | Value |
| --- | --- |
| `PEACE_VERCEL_PROJECT_ID` | 第 2 步取得的 `prj_…` |
| `PEACE_VERCEL_TEAM_ID` | 擁有專案的 `team_…`；API 不要求 Team scope 時可省略 |

注意：這些設定放在 **GitHub**，不是 Vercel 的 Environment Variables。`VERCEL_TOKEN` 放 Secret，其餘 ID 放 Variables。不要把 Token 貼到聊天室、截圖或 GitHub 程式碼。

## 第 5 步：確認 GitHub Pages 及 Vercel Git 整合

1. GitHub 專案 → Settings → Pages。
2. Build and deployment → Source 選 **GitHub Actions**。
3. Vercel 專案 → Settings → Git，確認已連接 `AcoHon53114/peace`、Production branch 是 `main`。
4. 此 workflow 使用 Vercel 的 `repository_dispatch` 成功／promoted 事件；如果 Git 設定中有相關事件開關，保持開啟。沒有開關時毋須另外建立 webhook。
5. GitHub Actions 如被停用，要先啟用。若 `github-pages` Environment 設有審批要求，每次發布會等待審批；要全自動請按你的專案政策設定。

正式網站保持公開可讀。工具只讀公開網域，不會登入 Admin，也不需要關閉 Preview deployment protection。

## 第 6 步：提交及 push

在 Terminal：

```bash
cd ~/Desktop/peace
source .venv/bin/activate
python -m pip install beautifulsoup4==4.13.4
python tools/test_pages_automation.py

git status --short
git add .github/workflows/pages-demo.yml tools/export_pages.py tools/pages_automation.py tools/test_pages_automation.py PAGES_GUIDE.md .gitignore
git diff --cached --stat
git commit -m "Automate Pages sync after Vercel production and hourly content checks"
git push origin main
```

提交前確認沒有 `.env.local`、Token、資料庫或測試輸出在 staged 檔案內。此工具依賴只由 workflow 安裝，不用修改 Django `requirements.txt`。

## 第 7 步：第一次手動確認

1. 等 Vercel 這次 Production 部署完成。
2. GitHub → Actions → **Publish Peace frontend demo**。
3. 如果成功部署事件已觸發 workflow，打開該次執行看結果；否則按 **Run workflow**，選 `main`。
4. 檢查 `Identify current live Production commit`、`Snapshot public frontend…`、`Deploy changed GitHub Pages site` 成功。
5. 第一次沒有比對記錄，會發布展示版。
6. 打開 https://acohon53114.github.io/peace/ 。檢查繁中、簡中、英文首頁及內頁；在 desktop、tablet、手機檢查選單、語言按鈕、圖片及表單連結。
7. 再按一次 Run workflow，沒有內容變更時 Summary 應顯示 `Public content/assets unchanged: publication skipped.`，Deploy 步驟應 skipped。

Pages 展示版沒有 Django backend。登入及表單會前往 Vercel 正式網站，展示版表單資料不會被直接 POST；需要在正式網站重新填寫。

## 第 8 步：確認兩條自動更新路徑

**程式更新路徑**：日後正常 push 一次實際需要的變更，等 Vercel Production 成功，確認 Actions 自動出現 `repository_dispatch` 執行，並確認展示版反映新內容。不需要為了測試而任意更改現有設計。

**Admin 更新路徑**：日後正常修改一則已公開消息或心聲，確認正式網站已更新。等下一次排程後，確認 Pages 更新。若想即時看到結果，可以 Run workflow，不需要 push 或重新部署 Vercel。

排程是每小時檢查一次，不代表內容更新後正好一小時內一定完成；GitHub 可延遲排程。只有公開頁呈現的內容會同步，未發布內容不會匯出。這個方法每次檢查會讀取完整公開頁和公開媒體，並不是直接查詢資料庫的修改時間。

## 版本配對和失敗保護

- 用 Vercel API 找出正式網域目前指向的 READY Production deployment，再 checkout 該 commit 的公開 CSS／JS／圖片。
- Workflow 工具本身從 default branch 取得；已部署的 commit 不需要已包含這次新增工具。
- 匯出後和發布前重新檢查正式部署。若中途換版本，停止這次發布，保留原有 Pages；下一次事件、排程或手動執行再試。
- Preview 事件不會執行發布工作。其他專案事件即使觸發，也只讀取配置的正式網域，不會使用事件提供的網址。
- 內容 hash 包括三語頁、連結、CSS／JS 及圖片檔案 bytes。只忽略既有消息卡片的「幾小時前」相對時間和匯出報告，不忽略標題、內文或實際發佈日期。
- 相同內容跳過發布。記錄只在 Pages 成功發布後保存；如果 GitHub 清除 cache，下一次會再發布一次，即使內容相同。
- 並行執行會排隊，workflow 不會 push 回 repo，不會造成 Vercel／Pages 互相觸發的循環。
- 公開媒體缺失、語言錯誤、API 權限錯誤或匯出失敗會中止，保留現有 Pages。
- 抓取多頁不是資料庫交易：若 Admin 在抓取期間修改不同項目，可能跨頁看到不同時間的內容；下一次檢查會重新同步。最後一次部署核對與 Pages 上線之間仍有很短的時間差。

## 常見問題

**沒有自動出現部署事件執行**：確認 workflow 已 push 到 default branch（通常 main），Vercel Git repo 連接正確、事件未停用。Hourly schedule 仍可補同步；先用 Run workflow 確認整套流程可成功。

**HTTP 401／403**：檢查 Token 是否到期、Scope 是否正確，以及 `PEACE_VERCEL_TEAM_ID` 是否需要。

**Project mismatch／Alias not found**：確認 Project ID 屬於 `peace-beta-sandy.vercel.app`，不是另一個 peace 專案。

**Cannot identify deployed Git commit**：目前正式部署沒有 Git commit metadata，例如手動 CLI 部署未提供 metadata；請使用原有 GitHub → Vercel 部署方式。工具不會以最新 main 猜測版本。

**Production changed during the export**：抓取時剛好有新部署，不用修改網站；等新部署完成再執行。

**Output already exists**：本機測試換一個尚未存在的 `--output` 資料夾；工具不會自行清除你的檔案。

**本機只測試匯出**：`python tools/export_pages.py --base-path "" --output _site-preview-new`，之後 `python -m http.server 8000 --directory _site-preview-new`。這是單獨預覽，不包含 Vercel 版本核對；請先確認本機 assets 與部署版本一致。

**排程長時間停止**：public repo 60 天沒有 repository activity，GitHub 可自動停用 scheduled workflow；到 Actions 重新啟用。執行時間和 cache 保存都受 GitHub 服務限制。

## 第二階段（這次尚未實作）

第一階段穩定後，才評估讓 Admin 儲存已公開內容時通知 GitHub，縮短等待時間；需要修改後台和加入 GitHub 通知憑證。這次先確認以上兩條路徑和三語 responsive 展示版正常即可。

## 官方參考

- https://vercel.com/docs/git/vercel-for-github
- https://vercel.com/docs/rest-api/aliases/get-an-alias
- https://vercel.com/docs/rest-api/deployments/get-a-deployment-by-id-or-url
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows

## 本次交付前檢查

- 10 項離線回歸測試通過（Production、Preview、專案／repo、Git SHA、rollback 身份、文字／圖片／相對時間 hash）。
- 正式公開網站匯出 21 個三語頁，0 個缺失媒體；靜態內部連結、三語目標、CSRF 移除及正式表單連結檢查通過。
- 實際 compare CLI 首次顯示 changed=true，再次相同內容顯示 changed=false；媒體缺失時中止。
- 375、390、768、1024、1440px，21 頁共 105 組 Chromium 靜態展示版檢查通過：沒有橫向溢出，選單未超出畫面，Escape 能關閉；手機寬度下三語可轉到同一內頁。外部第三方服務在此版面測試被攔截。
- JavaScript 語法及 workflow YAML 結構檢查通過。
- 尚未以你的 Vercel Token 呼叫 metadata API，也未在你的 GitHub 執行或部署此 workflow；需要按上述設定完成首次驗證。這次沒有實機 iPhone Safari 測試。
