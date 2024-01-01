document.addEventListener('DOMContentLoaded', function () {
    var modal = document.getElementById('myModal');
    var span = document.getElementById('closeModalButton');

    modal.style.display = 'block';
    document.body.style.overflow = 'hidden'; // Prevent scrolling on the background

    span.onclick = function () {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restore scrolling on the background
    };
});