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
    $('#activity-form').on('submit', function(e){
        e.preventDefault()
    
        var activityName= $('#activity_name').val()
        var startDate = $('#start_date').val()
        var endDate = $('#end_date').val()
        var location = $('#location').val()
        var budget = $('#budget').val()
        var standy = $('#standy').val()
        var flyer_shs = $('#flyer_shs').val()
        var flyer_ihs = $('#flyer_ihs').val()
        var tarpaulin = $('#tarpaulin').val()
        var nightclass = $('#nightclass').val()
        var description = $('#description').val()

     
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:8000/activity1/api/request/',
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            data: {
                activity_name: activityName,
                start_date: startDate,
                end_date: endDate,
                location: location,
                budget: budget,
                standy: standy,
                tarpaulin: tarpaulin,
                flyer_shs: flyer_shs,
                flyer_ihs: flyer_ihs,
                flyer_nc: nightclass,
                description: description,

            },

            success: function (json) {
                alert('Success')
                console.log(json)
                console.log('success')
            },
            error: function (xhr, errmsg, err) {
                alert('Fail')
                console.log(xhr.status + ": " + xhr.responseText)
            }



        })
      
    })
})