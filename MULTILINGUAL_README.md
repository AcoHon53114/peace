# peace 三語版本

基於 GitHub main：c27acfb0bbc984d7175ab06aa9fc939c8218db15（peace-optimized）。

## 本次更新（Admin 獨立三語／後台管理三語內容）

Admin 頂部加入繁體／簡體／英文選單及套用按鈕，登入頁也可使用。
Admin 使用独立 peace_admin_language cookie，預設繁體中文，記住一年，不改前台語言。
Django 原生介面使用內建翻譯；消息、心聲、聯絡查詢、預約、付款紀錄、院友資料的後台名称及欄位標籤補上翻譯。
修改中的表單切換語言前會提示；取消保留內容，確認才放棄未儲存修改並切換。

消息新增簡體／英文標題及正文；院友心聲新增簡體／英文姓名及正文。
Admin 按繁體、簡體、英文及共用資料分組，三語欄位始終同時顯示，並在列表顯示翻譯完成狀態。
圖片、YouTube、發布日期、發布狀態及記錄 ID 共用，不建立三筆重複內容。
舊 title/name/description 保留作繁體原文，新翻譯欄位初始為空，不自動翻譯。
缺少翻譯時，該欄位顯示繁體原文，並提示翻譯尚未完成；完成翻譯後提示消失。
前台消息搜尋使用所選語言的標題（翻譯為空則可搜尋顯示中的繁體原文）；Admin 可搜尋所有三語內容。
原有欄位的類型、長度、預設值、選項、關聯不變；其他模型的 migrations 只更新顯示標籤及名稱。
現有背景、按鈕、Hero、導覽、前台語言 JS 及非內容業務邏輯保留。

### 套用與部署順序（本次必須 migrate）

1. 先備份現有專案及資料庫。局部更新 ZIP 以相同路徑覆蓋檔案；完整 ZIP 的 peace-multilingual/ 是完整程式及圖片。
2. 在本機現有虛擬環境、已連接正式 Neon 的設定下，先執行：
   python manage.py check
   python manage.py migrate
3. migrate 成功後才提交 GitHub 並部署 Vercel。新欄位可以與上一版程式共存，因此先 migration、後部署。
   不要重新產生 migrations，不要把 migrate 放進每次 Vercel request；已包含全部 migration 檔案。
4. 不需更改 requirements、環境變數、前台 URL，或在 Vercel 安裝 gettext；三份 .mo 已編譯。
5. 打開 /admin/，選語言後按套用。編輯消息或院友心聲，分別填寫簡體／英文欄位，按儲存。
6. 在前台切換三語，檢查消息列表、詳細頁及院友心聲；文字須由管理員填寫或貼上已審核翻譯。

### 驗證

18 項 Django tests 通過，包含獨立語言 cookie、CSRF、重新導向限制、三語資料、缺少翻譯、搜尋、儲存及 migration 保留舊文字／圖片／日期／網址。
makemigrations --check --dry-run：沒有缺少 migration。
後台6頁×3語言×3主題×4寬度 =216組，登入3語言×5寬度=15組；前台5頁×3語言×5寬度=75組，無水平溢出。
使用較長英文消息／心聲；检查原生 POST 切換、未儲存內容取消／確認；沒有提交任何正式資料。
全部使用獨立本機 SQLite；沒有連接正式 Neon。Chromium viewport 檢查不等同實體 iPhone Safari。
測試停用外部 Google Maps 及 Font Awesome CDN，現有連結及資產保持不變。
下方歷史測試記錄來自此前版本；本次新增三語內容、admin 介面及標籤是既有保留條目的明確例外。

## 已完成

- 繁體中文、簡體中文、英文切換；首次進入預設繁體中文。
- 導覽列語言選單；手機和平板的收合選單亦可切換。
- 語言 cookie 記住選擇一年。切換後保留原網址、查詢參數及頁面錨點。
- 固定頁面文字、登入及註冊、會員頁面、付款選项、成功／錯誤提示、日期顯示、WhatsApp 預填文字。
- 固定內容翻譯及新增 72 條後台／內容管理翻譯，三份 .po 原稿及 .mo 執行檔均已包含，不需要在 Vercel 安裝 gettext。
- 如正在填寫表單，切換只儲存語言偏好，保留當前表單及所選附件；提交表單或前往下一頁後套用新語言。頁面會顯示說明。
- 使用已確認名稱：The Peaceful Home、The Peaceful Home For The Elderly Limited、Ms So、主管／Home Manager、Lucky Mansion。
- responsive 局部樣式處理英文換行、地址、會員表格及新增語言選單。

## 保留原有內容及功能

圖片、既有業務 JS、付款 choices、requirements.txt 及非內容業務邏輯保持不變。models、migrations、admin.css、brand-theme.css 按本次批准更新。
付款方式／月份只翻譯顯示文字，提交及儲存值仍是原有值。原有記錄無需轉換。
消息及院友心聲已按本次更新支援三語資料；管理後台介面也支援三語。用戶輸入、PDF、圖片內文字、外部網站及內部通知電郵維持原文。
外部資源三個名稱已按確認文案翻譯，繁體／簡體名稱保持原樣。
瀏覽器原生日期選擇器及 required 驗證訊息由瀏覽器自身語言控制。

## 套用到你的現有專案

請按上方「套用與部署順序」執行。保留自己的 .env.local、虛擬環境及資料庫設定；ZIP 不包含秘密、Git 歷史、虛擬環境或測試資料。
只套用本次更新，使用 peace-admin-content-update.zip。全部檔案在專案根目錄按同路徑覆蓋，包含 models、migration、模板、CSS、JS 及翻譯。
確認 migrate 成功後，再將更新清單中的檔案提交 GitHub。不要提交 .env.local。

```sh
python manage.py check
python manage.py migrate
git diff --cached --stat
git commit -m "Add independent admin languages and multilingual news and testimonials"
git push origin main
```

## 已修改／新增檔案

- `MULTILINGUAL_README.md`
- `accounts/views.py`
- `banks/apps.py`
- `banks/migrations/0004_alter_bank_options_alter_bank_comment_and_more.py`
- `banks/models.py`
- `banks/views.py`
- `contacts/apps.py`
- `contacts/migrations/0005_alter_contact_options_alter_contact_comment_and_more.py`
- `contacts/models.py`
- `contacts/views.py`
- `environments/admin.py`
- `environments/apps.py`
- `environments/migrations/0003_alter_voice_options_voice_description_en_and_more.py`
- `environments/models.py`
- `informations/apps.py`
- `informations/migrations/0004_alter_booking_options_alter_booking_comment_and_more.py`
- `informations/models.py`
- `informations/views.py`
- `locale/en/LC_MESSAGES/django.mo`
- `locale/en/LC_MESSAGES/django.po`
- `locale/zh_Hans/LC_MESSAGES/django.mo`
- `locale/zh_Hans/LC_MESSAGES/django.po`
- `locale/zh_Hant/LC_MESSAGES/django.mo`
- `locale/zh_Hant/LC_MESSAGES/django.po`
- `news/admin.py`
- `news/apps.py`
- `news/migrations/0004_alter_new_options_new_description_en_and_more.py`
- `news/models.py`
- `news/views.py`
- `pages/admin_language.py`
- `pages/content_languages.py`
- `pages/templatetags/__init__.py`
- `pages/templatetags/language_ui.py`
- `pages/test_admin_content.py`
- `pages/tests.py`
- `peaceweb/middleware.py`
- `peaceweb/settings.py`
- `peaceweb/static/css/admin.css`
- `peaceweb/static/css/brand-theme.css`
- `peaceweb/static/css/language-ui.css`
- `peaceweb/static/js/admin-language.js`
- `peaceweb/static/js/language-ui.js`
- `peaceweb/urls.py`
- `residents/apps.py`
- `residents/migrations/0008_alter_resident_options_alter_resident_resident_code_and_more.py`
- `residents/models.py`
- `templates/404.html`
- `templates/accounts/dashboard.html`
- `templates/accounts/login.html`
- `templates/accounts/register.html`
- `templates/admin/base_site.html`
- `templates/admin/language_switch.html`
- `templates/admin/login.html`
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

## 歷史驗證記錄（此前版本）

- 此前追加：三語 × 未登入／登入／長帳戶名稱 × 8個寬度，共72組導覽列同列、按鈕相鄰、收合與選單邊界檢查通過。320px只驗證導覽列；原有中文頁尾在320px仍可能溢出，本次未修改。

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
消息及院友心聲的三語內容由 admin 填寫，不需要修改 .po 或重新編譯 .mo。新增其他固定介面文字仍按上面翻譯流程處理。
