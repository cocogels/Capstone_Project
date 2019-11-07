



$(document).ready( function(){


    $('#start_date').kronos({
        periodTo: '#end_date',
        format: 'mm/dd/yyyy',
        button:{
            month: true,
            trigger: true,
            today:true,
        },
        text:{
            month: ['January', 'February', 'March', 
            'April', 'May', 'June', 'July', 'August', 
            'September', 'October', 'November', 'December'],
            btnToday: 'Today',
            btnTrigger: 'Pick A Date',
            btnPrevMonth: 'Prev Month',
            btnNextMonth: 'Next Month',
        },

        
    })


    $('#end_date').kronos({
        periodFrom: '#start_date',
        periodTo: '#end_date',
        format: 'mm/dd/yyyy',
        button:{
            month: true,
            trigger: true,
            today:true,
        },
        text:{
            month: ['January', 'February', 'March', 
            'April', 'May', 'June', 'July', 'August', 
            'September', 'October', 'November', 'December'],
            btnToday: 'Today',
            btnTrigger: 'Pick A Date',
            btnPrevMonth: 'Prev Month',
            btnNextMonth: 'Next Month',
        },
    })
})