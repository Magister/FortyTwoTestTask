var new_requests = 0;

function format_date(date) {
    return date.getUTCFullYear()
        + '-' + ('0' + (date.getUTCMonth() + 1)).slice(-2)
        + '-' + ('0' + date.getUTCDate()).slice(-2)
        + ' ' + ('0' + date.getUTCHours()).slice(-2)
        + ':' + ('0' + date.getUTCMinutes()).slice(-2)
        + ':' + ('0' + date.getUTCSeconds()).slice(-2)
}

function update_title() {
    var title = document.title.replace(/\(\d+\)\s*(.*)/, '$1');
    if (new_requests > 0) {
        title = '(' + new_requests + ') ' + title;
    }
    document.title = title;
}

// watch for page activation to update title
$(window).on("blur focus", function(e) {
    new_requests = 0;
    update_title();
});


// polling
$(document).ready(function() {
    setInterval(function() {
        $.ajax({
            url: window.url,
            type: "get",
            data: {from: window.last_update.toISOString()},
            success: function(response) {
                window.last_update = new Date(response.last_update);
                $('#last_update').html(format_date(window.last_update))
                //update table
                if (response.requests.length > 0) {
                    new_requests = new_requests + response.requests.length;
                    update_title();
                    var row_template = $('.request-row').last();
                    var table_body = $('#requests-body');
                    for (var i = response.requests.length - 1; i >= 0; i--) {
                        var new_row = row_template.clone();
                        var req = response.requests[i];
                        new_row.find('.request-date').html(req.date);
                        new_row.find('.request-method').html(req.method);
                        new_row.find('.request-path').html(req.path);
                        $(table_body).prepend(new_row);
                    }
                    // delete old rows
                    table_body.find('tr:gt(' + (window.requests_count - 1) + ')').remove();
                }
            }
        })
    }, 1000);
});
