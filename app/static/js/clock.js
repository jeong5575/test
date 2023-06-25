function updateClock() {
    var now = new Date();
    var targetDate = new Date('2023-11-06'); // D-day의 날짜를 설정해주세요
    var timeDiff = targetDate.getTime() - now.getTime();
    var days = Math.floor(timeDiff / (1000 * 60 * 60 * 24)); // D-day까지의 남은 일 수 계산

    var clock = document.getElementById('clock');
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var seconds = now.getSeconds();

    // 오전과 오후 구분
    var period = hours >= 12 ? '오후' : '오전';
    hours = hours % 12;
    hours = hours ? hours : 12; // 0시를 12로 표시

    // 시, 분, 초를 두 자리 숫자로 표시
    hours = addZeroPadding(hours);
    minutes = addZeroPadding(minutes);
    seconds = addZeroPadding(seconds);

    // 시계 텍스트 설정
    var timeText = period + ' ' + hours + '시 ' + minutes + '분 ' + seconds + '초';
    var dDayText = '⏰종강까지 ' + days + '일⏰';
    clock.innerHTML = timeText + '<br>' + dDayText;
}

function addZeroPadding(num) {
    return (num < 10 ? '0' : '') + num;
}

setInterval(updateClock, 1000);