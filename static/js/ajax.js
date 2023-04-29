/*
 * This function is from Django official web site:
 *   https://docs.djangoproject.com/en/3.1/ref/csrf/
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    }
});

$('form').submit(function(event) {
    event.preventDefault();
    var form = $(this);
    var formData = new FormData($('form').get(0));
    $.ajax({
        type: 'POST',
        url: form.prop('action'),
        method: form.prop('method'),
        data: formData,
        processData: false,
        contentType: false,
        timeout: 100000,
        dataType: 'text',
    }).done(function(response) {
        console.log('done');
        var parsedResponse = JSON.parse(response);
        if (parsedResponse.status == 0) {
            createSummary(parsedResponse.summary);
        } else {
            console.log('error');
            createAlertMessage(parsedResponse.errorMessage);
        }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log('fail');
        console.log(jqXHR.status);
        console.log(textStatus);
        console.log(errorThrown);
        alert(jqXHR.status + ' Error: ' + errorThrown);
    }).always(function() {
        console.log('always');
    });
});

function createSummary(text) {
    console.log('createSummary start');
    var label = $('#label');
    label.empty();
    label.append('要約結果:');

    var content = $('#summary');
    content.empty();
    content.append(text);
    content.addClass('form-control');
    console.log('createSummary end');
}

function createAlertMessage(message) {
    var messageArea = $('#messageArea');
    messageArea.empty();
    messageArea.append(
        '<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
            '<span>' + message + '</span>' +
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
        '</div>');
}
