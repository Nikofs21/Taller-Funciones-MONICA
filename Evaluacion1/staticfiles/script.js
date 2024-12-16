// Semaforo.html


document.addEventListener("DOMContentLoaded", function() {
    const datePicker = document.getElementById("datePicker");
    const today = new Date().toISOString().split("T")[0];
    datePicker.max = today;

    const urlParams = new URLSearchParams(window.location.search);
    const selectedDate = urlParams.get("fecha");
    if (selectedDate) {
        datePicker.value = selectedDate;
    }
});

function updateDate() {
    const datePicker = document.getElementById("datePicker");
    const selectedDate = datePicker.value;
    const comunaId = "{{ comuna.id_comuna }}";

    if (comunaId) {
        window.location.href = `${window.location.pathname}?comuna_id=${comunaId}&fecha=${selectedDate}`;
    } else {
        console.error("ID de comuna no disponible");
    }
}
function goBack() 
{
//window.history.back(); // Vuelve a la página anterior
window.location.href = 'http://127.0.0.1:8000/monica/';
}