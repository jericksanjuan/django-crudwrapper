from django.core.exceptions import ImproperlyConfigured
from braces.views import LoginRequiredMixin, UserPassesTestMixin


class ModulePermRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    module_name = None
    raise_exception = True

    def test_func(self, user):
        if self.module_name is None:
            raise ImproperlyConfigured(
                "'ModulePermRequiredMixin' requires "
                "'module_name' (the app_label).")

        return user.has_module_perms(self.module_name)


class CancelURLMixin(object):
    cancel_url = '..'

    def get_cancel_url(self):
        return self.cancel_url

    def get_context_data(self, **kwargs):
        ctx = super(CancelURLMixin, self).get_context_data(**kwargs)
        ctx['cancel_url'] = self.get_cancel_url()
        return ctx
