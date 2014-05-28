from django.core.exceptions import ImproperlyConfigured
from braces.views import LoginRequiredMixin, UserPassesTestMixin

__all__ = (
    'ModulePermRequiredMixin', 'CancelURLMixin',  'UserRelatedRequiredMixin'
)


class ModulePermRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    module_name = None
    raise_exception = True

    def test_func(self, user):
        if self.module_name is None:
            raise ImproperlyConfigured(
                "'ModulePermRequiredMixin' requires "
                "'module_name' (the app_label).")

        return user.has_module_perms(self.module_name)


class UserRelatedRequiredMixin(UserPassesTestMixin):
    """
    Make sure that the current User has a relation with the object.
    """

    relation_field = None

    def test_func(self, user):
        if self.relation_field is None:
            raise ImproperlyConfigured(
                "'UserRelatedRequiredMixin' requires "
                "'relation_field' (the model field related to request.user).")

        obj_result = self.get_result_relation_field(self.get_object(), self.relation_field)

        return obj_result == self.request.user

    def get_result_relation_field(self, obj, relfield):
        fields = relfield.split('__')
        for field in fields:
            try:
                obj = getattr(obj, field)
                if not obj:
                    raise ImproperlyConfigured("Invalid relation field, returns None")
            except AttributeError:
                raise ImproperlyConfigured("Invalid relation_field '{}'".format(relfield))
        return obj


class CancelURLMixin(object):
    cancel_url = '..'

    def get_cancel_url(self):
        return self.cancel_url

    def get_context_data(self, **kwargs):
        ctx = super(CancelURLMixin, self).get_context_data(**kwargs)
        ctx['cancel_url'] = self.get_cancel_url()
        return ctx
