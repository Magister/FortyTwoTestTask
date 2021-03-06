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
function setupPolling() {
    setInterval(function() {
        $.ajax({
            url: window.url,
            data: {'idfrom': window.last_id},
            type: "get",
            success: function(response) {
                $('#last_update').html(format_date(new Date(response.last_update)))
                // update table
                if (response.requests.length > 0) {
                    var received_new = 0;
                    var row_template = $('.request-row').last();
                    var table_body = $('#requests-body');
                    var last_id = window.last_id;
                    for (var i = response.requests.length - 1; i >= 0; i--) {
                        var new_row = row_template.clone();
                        var req = response.requests[i];
                        new_row.attr('id', req.id);
                        new_row.attr('data-priority', req.priority);
                        new_row.find('.request-date').html(req.date);
                        new_row.find('.request-method').html(req.method);
                        new_row.find('.request-path').html(req.path);
                        var req_prio = new_row.find('.request-priority');
                        req_prio.find('.view').html(req.priority);
                        req_prio.find('input[name=priority]').val(req.priority);
                        req_prio.find('input[name=id]').val(req.id);
                        // find a place to insert row
                        var inserted = false;
                        $(table_body).find('tr').each(function() {
                            if ($(this).attr('data-priority') <= req.priority) {
                                $(this).before(new_row);
                                inserted = true;
                                return false;
                            }
                        });
                        // no place found, insert at the end
                        if (!inserted) {
                            $(table_body).append(new_row);
                        }
                        // check if request id is greater than last displayed id
                        if (window.last_id < req.id) {
                            new_requests = new_requests + 1;
                            last_id = req.id;
                        }
                    }
                    // update last displayed id
                    window.last_id = last_id;
                    // update window title
                    new_requests = new_requests + received_new;
                    update_title();
                    // delete old rows
                    table_body.find('tr:gt(' + (window.requests_count - 1) + ')').remove();
                }
            }
        })
    }, 1000);
}

// request editing
function setupRequestEditing() {
    var table = $('#requests-body');
    table.find('.request-priority').click(function(e) {
        var $this = $(this);
        var editing = $this.find('.view').hasClass('hide');
        if (editing) {
            return;
        } else {
            e.preventDefault();
            $this.find('.view').addClass('hide');
            $this.find('.edit').removeClass('hide');
        }
    });
}

$(document).ready(function() {
    setupPolling();
    setupRequestEditing()
});
