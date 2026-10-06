# peace 三語版本

基於 GitHub main：c27acfb0bbc984d7175ab06aa9fc939c8218db15（peace-optimized）。

## 本次修正（desktop 導覽列掉行及語言按鈕走位）

導覽列不再為品牌保留固定百分比空間，桌面連結與帳戶按鈕保持單行，語言按鈕緊接帳戶操作。
按實際可用寬度、語言與帳戶名稱量度，放不下時整組使用 burger，不讓登錄／登出單獨掉行。
手機保持語言按鈕在 burger 左邊；無需改動圖片、其他模板、翻譯、後端或資料庫。
本次只修改 peaceweb/static/css/language-ui.css 和 peaceweb/static/js/language-ui.js，另更新此說明。
如已套用上一版，只需覆蓋以上兩檔，提交 GitHub 讓 Vercel 部署；無需 migration。
本 ZIP 同時包含之前的地球語言選單、三語及外部資源名稱修正。

## 已完成

- 繁體中文、簡體中文、英文切換；首次進入預設繁體中文。
- 導覽列語言選單；手機和平板的收合選單亦可切換。
- 語言 cookie 記住選擇一年。切換後保留原網址、查詢參數及頁面錨點。
- 固定頁面文字、登入及註冊、會員頁面、付款選项、成功／錯誤提示、日期顯示、WhatsApp 預填文字。
- 221 條翻譯，三份 .po 原稿及 .mo 執行檔均已包含，不需要在 Vercel 安裝 gettext。
- 如正在填寫表單，切換只儲存語言偏好，保留當前表單及所選附件；提交表單或前往下一頁後套用新語言。頁面會顯示說明。
- 使用已確認名稱：The Peaceful Home、The Peaceful Home For The Elderly Limited、Ms So、主管／Home Manager、Lucky Mansion。
- responsive 局部樣式處理英文換行、地址、會員表格及新增語言選單。

## 保留原有內容及功能

圖片、既有 CSS/JS 資產、models、migrations、choices、requirements.txt 及業務邏輯保持不變。
付款方式／月份只翻譯顯示文字，提交及儲存值仍是原有值。原有記錄無需轉換。
消息、院友心聲及用戶輸入維持原文；PDF、圖片內文字、外部網站、管理後台及内部通知電郵不作三語化。
外部資源三個名稱已按確認文案翻譯，繁體／簡體名稱保持原樣。
瀏覽器原生日期選擇器及 required 驗證訊息由瀏覽器自身語言控制。

## 套用到你的現有專案

1. 先備份目前專案或確認現有修改已 commit。
2. 解壓縮此 ZIP。其 peace-multilingual/ 是完整程式及原有圖片資料夾。
3. 按下方清單，把已修改及新增檔案複製到你現有 peace 專案的相同路徑。不要刪除現有專案。
4. 保留你自己的 .env.local、虛擬環境及資料庫設定。ZIP 不包含環境秘密、Git 歷史、虛擬環境、資料庫檔案或測試資料。
5. 本次不需要新增 Vercel 環境變數、安裝新執行套件，亦不需要資料庫 migration。
6. 在已啟用原有虛擬環境的終端機執行：python manage.py check。
7. 確認 locale/**/LC_MESSAGES/django.mo 以及新增的兩個靜態檔案有提交 Git。
8. git commit 後 push 到 main，讓原有 Vercel 部署流程重新部署。
9. 部署後在桌面與手機切換三語；確認登入、預約和付款記錄介面。未提交表單保護說明屬預期行為。

建議提交命令（在你的 peace 專案根目錄）：

```sh
git add templates locale pages/templatetags pages/tests.py accounts/views.py banks/views.py contacts/views.py informations/views.py peaceweb/settings.py peaceweb/urls.py peaceweb/middleware.py peaceweb/static/css/language-ui.css peaceweb/static/js/language-ui.js
git diff --cached --stat
git commit -m "Add Traditional Chinese, Simplified Chinese and English language switching"
git push origin main
```

## 已修改／新增檔案

- `MULTILINGUAL_README.md`
- `accounts/views.py`
- `banks/views.py`
- `contacts/views.py`
- `informations/views.py`
- `locale/en/LC_MESSAGES/django.mo`
- `locale/en/LC_MESSAGES/django.po`
- `locale/zh_Hans/LC_MESSAGES/django.mo`
- `locale/zh_Hans/LC_MESSAGES/django.po`
- `locale/zh_Hant/LC_MESSAGES/django.mo`
- `locale/zh_Hant/LC_MESSAGES/django.po`
- `pages/templatetags/__init__.py`
- `pages/templatetags/language_ui.py`
- `pages/tests.py`
- `peaceweb/middleware.py`
- `peaceweb/settings.py`
- `peaceweb/static/css/language-ui.css`
- `peaceweb/static/js/language-ui.js`
- `peaceweb/urls.py`
- `templates/404.html`
- `templates/accounts/dashboard.html`
- `templates/accounts/login.html`
- `templates/accounts/register.html`
- `templates/base.html`
- `templates/contacts/contact.html`
- `templates/environments/environment.html`
- `templates/informations/guideline.html`
- `templates/informations/information.html`
- `templates/news/new.html`
- `templates/news/news.html`
- `templates/pages/about.html`
- `templates/pages/index.html`
- `templates/partials/_alert.html`
- `templates/partials/_footer.html`
- `templates/partials/_navbar.html`
- `templates/partials/_topbar.html`

## 驗證

- 本次追加：三語 × 未登入／登入／長帳戶名稱 × 8個寬度，共72組導覽列同列、按鈕相鄰、收合與選單邊界檢查通過。320px只驗證導覽列；原有中文頁尾在320px仍可能溢出，本次未修改。

- Django check：無問題；所有 templates 可編譯。
- 8 項 Django feature tests 全部通過（包括實際繁簡字形和 Django locale 目錄名稱）（含三語頁面、cookie、CSRF、跳轉、付款選項舊資料及表單錯誤提示）。
- 11 個頁面 × 3 語言皆回應 200，另檢查登入後 dashboard 與預約驗證。
- Chromium headless：6 個代表頁面 × 3 語言 × 5 個寬度（375、390、768、1024、1440px），90 組無整頁橫向溢出，並逐頁驗證實際繁體、簡體、英文導覽文字。
- 登入後 dashboard 及付款記錄 modal：3 語言 × 5 個寬度，15 組通過。
- 手機 hamburger、語言切換、原 query/hash、未提交文字及已選附件保留通過。
- 已檢視手機、平板、桌面截圖，並局部修正地址及導覽列溢出。
- 翻譯檔 msgfmt --check、JavaScript 語法、git diff --check 通過。
- 353 個原有圖片、靜態資產、models、migrations、choices及依賴檔逐檔比對保持原樣；4個 view 去除 gettext 包裝後 AST 與原版一致。

### 驗證範圍

使用獨立 SQLite 測試資料庫，沒有接觸你的 Neon 或正式資料。瀏覽器測試使用桌面 Chromium 的 viewport 模擬，不等同實體 iPhone Safari／Android 裝置。
測試時停用外部 Google Maps 及 Font Awesome CDN 請求；這些現有連結和資產未修改。
發現原有預約頁 main.js 使用不存在的 bookingForm id 而產生 Console 錯誤；該檔案與原版本位元組相同，依「其他保持不變」保留。語言切換及預約日期／時間選項測試不受此既有錯誤影響。
本次未測試正式環境的 SMTP 發信或附件儲存，相關業務程式並未變更。

## 翻譯維護

新增或編輯固定文字時，更新 locale 下對應 .po，重新產生 .mo 後一起提交。日後可在有 GNU gettext 的開發電腦執行 python manage.py compilemessages。
如日後把消息正文及院友心聲加入三語內容，需要另設資料欄位及後台編輯方式。
