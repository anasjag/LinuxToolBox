document.addEventListener('DOMContentLoaded', function () {
    var modal = document.getElementById('myModal');
    var btn = document.getElementById('tool_card_btn');
    var span = document.getElementById('closeModalButton');

    btn.onclick = function () {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevent scrolling on the background
    };

    span.onclick = function () {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restore scrolling on the background
    };

    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto'; // Restore scrolling on the background
        }
    };
});