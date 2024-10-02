

document.addEventListener('DOMContentLoaded', function() {
    var messageContainer = document.getElementById('message-container');
    if (messageContainer) {
        setTimeout(function() {
            messageContainer.style.transition = 'opacity 1s';
            messageContainer.style.opacity = '0';
            setTimeout(function() {
            messageContainer.style.display = 'none';
            }, 1000);
        }, 3000);
        }
    });





document.addEventListener("DOMContentLoaded", function() {
    // 設定今天的日期
    var today = new Date();
    var minDate = new Date(today);
    minDate.setDate(today.getDate() + 1); // 設定最小日期為明天
    var maxDate = new Date(today);
    maxDate.setDate(today.getDate() + 7); // 設定最大日期為今天起的七天

    // 設定日期輸入的最小值和最大值
    var meetingDateInput = document.getElementById("meeting-date");
    meetingDateInput.setAttribute("min", minDate.toISOString().slice(0, 10));
    meetingDateInput.setAttribute("max", maxDate.toISOString().slice(0, 10));

    // 設定可用的時間
    var allowedTimes = [];
    for (var hour = 10; hour <= 17; hour++) {
        allowedTimes.push((hour < 10 ? '0' : '') + hour + ':00');
    }

    meetingDateInput.addEventListener('change', function() {
        var selectedDate = meetingDateInput.value;
        var timeSelect = document.getElementById("meeting-time");
        timeSelect.innerHTML = ""; // 清空先前的選項

        // 添加有效時間選項
        allowedTimes.forEach(function(time) {
            var option = document.createElement("option");
            option.value = time;
            option.textContent = time;
            timeSelect.appendChild(option);
        });
    });
});




document.addEventListener('DOMContentLoaded', function() {
    // 如果有錯誤，滾動到表單位置
    if (document.querySelector('.error')) {
        document.getElementById('bookingForm').scrollIntoView({
            behavior: 'smooth'
        });
    }

    // 保存表單位置
    var form = document.getElementById('bookingForm');
    form.addEventListener('submit', function() {
        localStorage.setItem('formPosition', window.pageYOffset);
    });

    // 如果有保存的位置，滾動到該位置
    var savedPosition = localStorage.getItem('formPosition');
    if (savedPosition !== null) {
        window.scrollTo(0, parseInt(savedPosition));
        localStorage.removeItem('formPosition');
    }
});

