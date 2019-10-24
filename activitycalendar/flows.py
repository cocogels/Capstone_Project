from viewflow import flow, frontend
from viewflow.base import this, Flow 
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from viewflow.lock import select_for_update_lock

from activitycalendar import views
from activitycalendar.models import ActivityCalendarProcess, ActivityCalendar, ActivityCalendarTask

@frontend.register
class ActivityCalendarFlow(Flow):
    """
    Plotting Activity to Calendar 
    """
    process_class = ActivityCalendarProcess
    task_class = ActivityCalendarTask
    #lock_impl = select_for_update_lock
    
    summary_template = """
    Activity {{ process.activity.activity_set.count }}
    """
    
    start = (
        flow.Start(views.CalendarCreateView)
        .Permission('activity.can_create_activity_request')
        .Next(this.for_approval)
    )
    
    
    for_approval = (
        flow.Split()
        .Next(this.approved_request)
        .Next(this.revised_request)
        .Next(this.rejected_request)
    )
    
    
    approved_request = (
        flow.View(
            views.CalendarView,
            task_description="Approval Request"
        )
        .Assign(lambda act: act.process.created_by)
        .Next(this.check_approve)
    )
    
    revised_request = (
        flow.If(
           cond=lambda act: act.process.is_revised_activity(),
        )
        .Then(this.check_activity_request)
        .Else(this.check_approve)
    )

    check_activity_request = (
        flow.View(views.RevisedView, fields=['approved'])
        .Assign(lambda act: act.process.created_by)        
        .Next(this.approved_request)
    )
    
    rejected_request = (
        flow.View(views.CalendarTemplateView)
        .Next(this.end)
    )
    
    check_approve = (
        flow.If(lambda act: act.process.approved)
        .Then(this.plot_to_calendar)
        .Else(this.end)
    )
    
    plot_to_calendar = (
        flow.View(
            views.CalendarTemplateView
        )
        .Next(this.end)
    )
    
    
    end = flow.End()
    
