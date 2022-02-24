from django.forms import ModelForm
from django.views.generic.edit import UpdateView
from tasks.models import Report
from tasks.views import AuthorizedTaskManager


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["send_time"]

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)

        style = "text-black bg-gray-100 rounded-xl w-full my-1 p-3"
        self.fields["send_time"].widget.attrs.update({"class": style})


class GenericReportUpdateView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = "report_update.html"
    success_url = "/tasks"

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        return self.request.user
