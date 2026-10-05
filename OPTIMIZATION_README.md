# peace 載入優化版本
來源：GitHub main a19ea86；未推送或部署。

## 使用步驟
1. 備份原有 peace 資料夾。
2. 將本資料夾內容合併到原有 peace，保留原有 .env.local、.venv、.git。
3. python manage.py check
4. python manage.py runserver
5. 檢查手機/平板/桌面導覽、輪播、新聞 Lightbox、關於我們 Counter、登入及預約。
6. git add templates peaceweb/static news/templatetags/youtube_filters.py
7. git commit -m "Optimize images and page asset loading"
8. git push origin main

## 修改範圍
八張照片新增 WebP，原圖保留，解像度及比例保持。首頁刪除重複 JS。統一 jQuery 依賴順序及 defer。Counter 只在關於我們載入；Lightbox 只在新聞詳情載入；保留 Sticky 導覽。移除全站不匹配 section 的 click-scroll 載入。custom.js 保留訊息淡出、Counter、hash 滾動並增加防護。附圖/評語頭像/YouTube 延遲載入。圖片尺寸屬性配合原有 responsive CSS。
CSS、models、views、settings、表單、權限、郵件流程及頁面文字不變。沒有改 media 儲存或產生動態縮圖。

## 驗證
Django check 通過；隔離 SQLite migrations 通過；十個 GET 頁面回應 200。CSS/後端業務檔比對未變，WebP 可以解碼。
瀏覽器下載失敗，未完成手機/平板/桌面實際視覺驗證；請推送前在本機檢查。沒有測試正式 Neon、寄信或上載。
不包含 .env、.git、Python 編譯快取及 .DS_Store。

八張圖片總大小 5.70 MB → 0.91 MB（減少 84.0%）。不是整站速度測量。

修改/新增檔案：
- templates/base.html
- news/templatetags/youtube_filters.py
- peaceweb/static/images/portrait-volunteer-who-organized-donations-charity.webp
- peaceweb/static/images/IMG_1428.webp
- peaceweb/static/js/custom.js
- peaceweb/static/images/slide/different-people-doing-volunteer-work.webp
- peaceweb/static/images/slide/volunteer-selecting-organizing-clothes-donations-charity.webp
- peaceweb/static/images/slide/volunteer-helping-with-donation-box.webp
- peaceweb/static/images/causes/facilities2aa.webp
- peaceweb/static/images/causes/facilities4a.webp
- peaceweb/static/images/causes/facilities3a.webp
- templates/pages/index.html
- templates/pages/about.html
- templates/environments/environment.html
- templates/news/new.html