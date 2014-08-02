from django.core.exceptions import ImproperlyConfigured
from braces.views import LoginRequiredMixin, UserPassesTestMixin, FormMessagesMixin

__all__ = (
    'ModulePermRequiredMixin', 'CancelURLMixin',  'UserRelatedRequiredMixin',
    'FormSetMessagesMixin', 'DateRangeQueryMixin'
)


class ModulePermRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Check if user has the required module permissions.
    """

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


class FormSetMessagesMixin(FormMessagesMixin):
    """
    Extend FormMessagesMixin to also work on extra-views Views.
    """

    def forms_valid(self, form, inlines):
        response = super(FormMessagesMixin, self).forms_valid(form, inlines)
        self.messages.success(self.get_form_valid_message(),
                              fail_silently=True)
        return response

    def forms_invalid(self, form, inlines):
        response = super(FormSetMessagesMixin, self).forms_invalid(
            form, inlines)
        self.messages.error(self.get_form_invalid_message(),
                            fail_silently=True)
        return response

    def formset_valid(self, formset):
        response = super(FormSetMessagesMixin, self).formset_valid(formset)
        self.messages.success(self.get_form_valid_message(),
                              fail_silently=True)
        return response

    def formset_invalid(self, formset):
        response = super(FormSetMessagesMixin, self).formset_invalid(formset)
        self.messages.error(self.get_form_invalid_message(),
                            fail_silently=True)
        return response


class DateRangeQueryMixin(object):
    date_field = None
    start_date_q = 'start_date'
    end_date_q = 'end_date'

    def get_date_field(self):
        if self.date_field is None:
            raise ImproperlyConfigured(
                "'DateRangeQueryMixin' requires "
                "'date_field'.")
        return self.date_field

    def get_start_date_q(self):
        if self.start_date_q is None:
            raise ImproperlyConfigured(
                "'DateRangeQueryMixin' requires "
                "'start_date_q'.")
        return self.start_date_q

    def get_end_date_q(self):
        if self.start_date_q is None:
            raise ImproperlyConfigured(
                "'DateRangeQueryMixin' requires "
                "'end_date_q'.")
        return self.end_date_q

    def get_date_range_lookup(self, date_field=None):
        if not date_field:
            date_field = self.get_date_field()
        start_date = self.request.GET.get(self.get_start_date_q(), None)
        end_date = self.request.GET.get(self.get_end_date_q(), None)
        lookup_kwargs = {}
        if start_date:
            lookup_kwargs['{}__gte'.format(date_field)] = start_date
        if end_date:
            lookup_kwargs['{}__lte'.format(date_field)] = end_date
        return lookup_kwargs

    def get_queryset(self):
        qs = super(DateRangeQueryMixin, self).get_queryset()
        lookup_kwargs = self.get_date_range_lookup()
        return qs.filter(**lookup_kwargs)
