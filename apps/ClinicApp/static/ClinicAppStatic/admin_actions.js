/**
 * Dental Clinic - Admin Action Button Handlers
 * Provides delete confirmation and CSRF-aware POST requests for inline delete buttons.
 */

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function adminDelete(deleteUrl) {
    if (confirm('Are you sure you want to delete this item?')) {
        const csrftoken = getCookie('csrftoken');
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = deleteUrl;
        form.style.display = 'none';

        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrftoken;
        form.appendChild(csrfInput);

        document.body.appendChild(form);
        form.submit();
    }
}
