// scripts.js

// 動態創建 <script> 標籤來引入 jQuery
var jqueryScript = document.createElement('script');
jqueryScript.src = "https://code.jquery.com/jquery-3.5.1.slim.min.js";
document.head.appendChild(jqueryScript);

// 動態創建 <script> 標籤來引入 Popper.js
var popperScript = document.createElement('script');
popperScript.src = "https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js";
document.head.appendChild(popperScript);

// 動態創建 <script> 標籤來引入 Bootstrap
var bootstrapScript = document.createElement('script');
bootstrapScript.src = "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js";
document.head.appendChild(bootstrapScript);