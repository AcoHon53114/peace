# peace：同一個 repo 的 GitHub Pages 前台展示版

正式 Django 網站仍部署在 Vercel。這個工具只讀取 Vercel 的公開前台 GET 頁面，產生 HTML；CSS、JS、圖片沿用 repo 的公開 static 資產。GitHub Pages 不運行 Django，也不連接 Neon。

這是「已部署網站的公開快照」，不是在 Actions 中啟動 Django。必須先等 Vercel 完成部署，再手動匯出，確保 repo 的 CSS/JS 與 Vercel 頁面屬於同一版。

## 1. 加入檔案

在 Mac 解壓 peace-pages-setup.zip，把以下兩檔放到 ~/Desktop/peace 的相同路徑：

- tools/export_pages.py
- .github/workflows/pages-demo.yml

PAGES_GUIDE.md 可一併複製到專案根目錄，供日後查閱。不要覆蓋 Django settings、models、requirements.txt 或 Vercel 設定。
若 Finder 看不到 .github，按 Command + Shift + . 顯示隱藏檔案／資料夾。

## 2. 排除產生的網站檔案

在現有 .gitignore 最底加入（不要清空原有內容）：

```gitignore
_site/
_site-preview*/
```

展示版 HTML 由 Actions 產生及上傳，不需要 commit。不要提交 .env.local。

## 3. 本機安裝匯出工具需要的套件

```bash
cd ~/Desktop/peace
source .venv/bin/activate
python -m pip install beautifulsoup4==4.13.4
```

只供匯出工具使用，不需修改 Django 的 requirements.txt；Actions 會自行安裝這個套件。

## 4. 本機產生及預覽（建議）

確認正式網址能正常開啟，而且三語切換已完成部署。然後執行：

```bash
python tools/export_pages.py --source https://peace-beta-sandy.vercel.app --base-path "" --output _site-preview
python -m http.server 8000 --directory _site-preview
```

在瀏覽器開啟 http://localhost:8000/。首頁會轉到繁體展示版。

检查三語、圖片、各頁連結、手機版導覽。表單上方會標明展示版；按提交會打開 Vercel 正式頁面，需要在正式網站重新填寫。登入、註冊、會員及 admin 連結直接指向 Vercel。

停止預覽伺服器：終端機按 Control + C。

再次匯出時，如果 _site-preview 已存在，工具不會刪除它。可改用 --output _site-preview-2，並將 --directory 改成相同名稱。

## 5. 提交 GitHub

```bash
git add tools/export_pages.py .github/workflows/pages-demo.yml .gitignore
git diff --cached --stat
git commit -m "Add GitHub Pages frontend demo exporter"
git push origin main
```

若也複製了 PAGES_GUIDE.md，在 commit 前另執行 git add PAGES_GUIDE.md。

這一步可能同時觸發原有 Vercel 部署，先等待它完成。新增工具不會自動執行資料庫 migration。

## 6. 啟用 GitHub Pages

打開 https://github.com/AcoHon53114/peace ：

1. Settings。
2. 左邊 Pages。
3. Build and deployment → Source，選 GitHub Actions。
4. 不需要選 gh-pages branch，不需要新增 DATABASE_URL 或 DJANGO_SECRET_KEY。

## 7. 手動發布展示版

1. Repo 頂部 Actions。
2. 左邊 Publish Peace frontend demo。
3. Run workflow。
4. Branch 選 main。
5. 按 Run workflow。
6. 等 build 及 deploy 都變綠色。

沒有 Run workflow：確認 pages-demo.yml 已在 main 的 .github/workflows/，以及 Actions 已允許使用。

## 8. 開啟展示網站

一般專案網址為 https://acohon53114.github.io/peace/；以成功 workflow 的部署連結為準。

- https://acohon53114.github.io/peace/zh-hant/
- https://acohon53114.github.io/peace/zh-hans/
- https://acohon53114.github.io/peace/en/

Workflow 會從 GitHub Pages metadata 取得 base path，因此不用把正式網站的 STATIC_URL 改成 /peace/。

## 9. 日後如何更新

修改同一個 Django repo → commit/push → 等 Vercel 部署成功 → 手動 Run workflow。

只在 admin 更新消息或院友心聲：正式 Vercel 會即時讀取資料庫；等公開頁面顯示新內容後，直接再 Run workflow 即可，不需要再 commit。

第一版刻意沒有 push 自動發布：GitHub Actions 若比 Vercel 早完成，可能抓到上一版 HTML。不要單純加入 push trigger 而忽略 Vercel 的完成時間。

## 範圍

匯出首頁、關於我們、院舍環境、入院須知、入住指引、公開消息及聯絡頁，繁／簡／英各一份。公開消息列表中的詳情及分頁也會跟隨匯出（每語言最多 100 個頁面，超限會停止）。

不匯出登入、註冊、admin、會員頁、付款紀錄、查詢內容或資料庫檔案。移除 HTML 內的 CSRF hidden inputs。沒有任何正式表單 POST 或登入。

缺少公開圖片／文件時，export-report.json 會記錄，該圖片仍連到原網址；外部 Google Maps、YouTube、Font Awesome 等沿用原服務，需要網絡。

## 常見錯誤

- deploy-pages: Not Found：先確認 Settings → Pages → Source 已選 GitHub Actions，再重新執行。
- 找不到 workflow：檔案路徑要是 .github/workflows/pages-demo.yml，且已 push 到 main。
- Wrong language / Expected current Peace language control is missing：Vercel 尚未部署所需三語版本，或前台語言 markup 已改變；不要發布不完整結果。
- 圖片失效：先確認相同 Vercel 頁面的圖片可正常開啟，再看產生的 export-report.json。
- 找不到 public static assets：必須在含 manage.py 及 peaceweb/ 的 repo 根目錄執行。
- Output already exists：使用新的 --output 名稱，或自行移除先前產生的網站資料夾。

本工具沒有替你啟用 GitHub Pages、push 或發布任何網站。GitHub 官方說明：https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
