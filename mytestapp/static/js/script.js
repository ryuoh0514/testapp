document.addEventListener("DOMContentLoaded", function() {
    var form = document.getElementById("new-message");
    var textarea = document.getElementById("message_text");

    textarea.addEventListener("keypress", function(e) {
        if (e.KeyCode == 13) { // Enterが押された
            if (!e.shiftKey && textarea.value.trim().length > 0) {
                e.preventDefault(); // デフォルトのEnterキーの動作を無効化
                form.submit(); // フォームを送信
            }
        }
    });
});
