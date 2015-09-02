
function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function enable_form(form, enable) {
    form.find(':input').prop('disabled', !enable);
    if (enable) {
        form.find('.add-row').removeClass('hide');
        form.find('.delete-row').removeClass('hide');
    } else {
        form.find('.add-row').addClass('hide');
        form.find('.delete-row').addClass('hide');
    }
}

function submit_form(event) {

    event.preventDefault();

    // clean previous messages
    $('#success').text('').addClass('hide');
    $('#errors').text('').addClass('hide');
    $('.validation-error').remove();
    $('.has-error').removeClass('has-error');
    // show loading message
    $('#loading').removeClass('hide');

    // prepare data
    var form_data = $(this).serializeArray();
    var json_data = {};
    for (var i = 0; i < form_data.length; i++) {
        json_data[form_data[i].name] = form_data[i].value;
    }
    // and send it
    post_form($(this), json_data);
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function post_form(form, json_data) {

    // disable form
    enable_form(form, false);

    // serialize
    var data = JSON.stringify(json_data);

    // do the POST
    $.ajax({
        type: "POST",
        dataType: "json",
        url: this.action,
        data: data,
        contentType: "application/json"
    })
        .success(process_response)
        .fail(function(req, status, error) {
            var msg = status;
            if (error) {
                msg = msg + ': ' + error;
            }
            $('#errors').text(msg).removeClass('hide');
        })
        .always(function() {
            $('#loading').addClass('hide');
            enable_form(form, true);
        });
}

function process_response(data, status) {
    if (!data.ok) {
        // iterate through errors and show them to the user
        var keys = Object.keys(data.errors);
        for (var i = 0; i < keys.length; i++) {
            var el = $('#id_' + keys[i]);
            el.parent().addClass('has-error');
            var errors = data.errors[keys[i]];
            var error_msg = '<ul class="validation-error">';
            for (var j = 0; j < errors.length; j++) {
                error_msg = error_msg + '<li>' +
                        errors[j] + '</li>';
            }
            error_msg = error_msg + '</ul>';
            el.after($(error_msg));
        }
        $('#errors').text('Form has errors').removeClass('hide');
    } else {
        $('#success').text('Saved').removeClass('hide');
    }
}

$(document).ready(function() {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#mainform').on('submit', submit_form);
});
