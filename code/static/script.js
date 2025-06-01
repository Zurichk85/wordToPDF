// Funcionalidad para el conversor Word a PDF

// Verifica si LibreOffice está disponible
function checkLibreOfficeStatus() {
    fetch('/check-libreoffice')
        .then(response => response.json())
        .then(data => {
            if (!data.available) {
                showLibreOfficeWarning(data.message);
            }
        })
        .catch(error => {
            console.error('Error verificando LibreOffice:', error);
        });
}

function showLibreOfficeWarning(message) {
    const warningDiv = document.createElement('div');
    warningDiv.className = 'error-container';
    warningDiv.innerHTML = `
        <p><i class="fa-solid fa-triangle-exclamation"></i> <strong>Atención:</strong> ${message}</p>
        <p>La conversión podría no funcionar correctamente. Considera las siguientes opciones:</p>
        <ul style="list-style-type: none; padding-left: 20px; margin-top: 10px;">
            <li><i class="fa-solid fa-docker" style="margin-right: 8px;"></i> Usar la versión Docker para una experiencia sin problemas</li>
            <li><i class="fa-solid fa-download" style="margin-right: 8px;"></i> <a href="https://www.libreoffice.org/download/download/" target="_blank">Descargar e instalar LibreOffice</a></li>
        </ul>
    `;
    
    // Insertar antes del área de carga
    const uploadArea = document.getElementById('drop-area');
    uploadArea.parentNode.insertBefore(warningDiv, uploadArea);
}

// Muestra consejos útiles
function showTips() {
    const tipsDiv = document.createElement('div');
    tipsDiv.className = 'tips-container';
    tipsDiv.innerHTML = `
        <div class="tips-title"><i class="fa-solid fa-lightbulb"></i> Consejos para una mejor conversión</div>
        <ul class="tips-list">
            <li>Asegúrate de que tus documentos Word estén en formato .docx</li>
            <li>Para preservar fuentes, utiliza tipos de letra comunes</li>
            <li>Las imágenes se mantienen en alta calidad</li>
            <li>Los documentos con macros pueden dar problemas en la conversión</li>
        </ul>
    `;
    
    // Insertar después del área de carga
    const uploadArea = document.getElementById('drop-area');
    const nextElement = uploadArea.nextElementSibling;
    uploadArea.parentNode.insertBefore(tipsDiv, nextElement);
}

// Maneja la carga de ejemplos
function loadExample(exampleFile) {
    fetch(`/examples/${exampleFile}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('No se pudo cargar el ejemplo');
            }
            return response.blob();
        })
        .then(blob => {
            const file = new File([blob], exampleFile, { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
            addFile(file);
        })
        .catch(error => {
            console.error('Error cargando ejemplo:', error);
            alert('No se pudo cargar el archivo de ejemplo');
        });
}

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Verificar LibreOffice cuando esté disponible
    if (document.readyState === 'complete') {
        setTimeout(checkLibreOfficeStatus, 2000);
        setTimeout(showTips, 500);
    } else {
        window.addEventListener('load', function() {
            setTimeout(checkLibreOfficeStatus, 2000);
            setTimeout(showTips, 500);
        });
    }
});

// Detecta si estamos en un dispositivo móvil
function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// Ajusta la interfaz para dispositivos móviles
function adjustForMobile() {
    if (isMobile()) {
        document.querySelector('.upload-text').textContent = 'Toca para seleccionar archivos Word';
    }
}

// Llamar al ajuste para móviles cuando se cargue la página
window.addEventListener('load', adjustForMobile);
