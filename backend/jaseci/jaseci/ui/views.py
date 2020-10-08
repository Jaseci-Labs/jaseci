from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms
from . import ui


class UIHome(View, ui.ui):
    def __init__(self):
        ui.ui.__init__(self)
        super().__init__()

    def get(self, request):
        """Handle get requests for Jaseci UI"""
        self.req = request
        if(not request.user.is_authenticated):
            self.check_dummy_user()
            return render(request, 'index.html', {})
        self.master = self.req.user.get_master()

        op = self.check_op()
        if(op):
            return op

        return render(request, 'index.html', self.ctx())

    def post(self, request):
        """Handle post requests for Jaseci UI"""
        return render(request, 'index.html', self.ctx())


class Test(TemplateView):
    template_name = 'test.html'


class CreateUser(CreateView):
    form_class = forms.CreateUserForm
    success_url = reverse_lazy('login')
    template_name = 'create_user.html'
