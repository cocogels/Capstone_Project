// Check if Webpage already loaded then excute the code below
$(document).ready( function(){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';')
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    })
    $(document).on('submit', '#activity-form', function(event){
        event.preventDefault()

        $.ajax({
            url: '/activity/api/request/',
            dataType:'json',
            type: 'POST',
            data:{
                start_date: $('#start_date').val(),
                end_date: $('#end_date').val(),
                activity_name: $('#activity_name').val(),
                location: $('#location').val(),
                description: $('#description').val(),
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            }
            
        })
    })
})