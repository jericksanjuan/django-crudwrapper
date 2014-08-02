from django.utils.safestring import mark_safe
from django.forms.models import BaseInlineFormSet

from vanilla import CreateView, UpdateView, DeleteView
from braces.views import FormMessagesMixin, SuccessURLRedirectListMixin
from extra_views import ModelFormSetView, CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet

from .forms import CrispyFormViewMixin, FormSetHelperViewMixin
from .mixins import CancelURLMixin, FormSetMessagesMixin

"""
Wrapper views for reusable apps.

Available options:

form_class = set a custom form class, a CrispyModelForm is automatically generated if not defined.
fields = define the fields for the generated form class
succes_list_url = urlname for success redirect

override for messages:
def get_form_valid_message
def get_form_invalid_message
"""

__all__ = (
    'CreateView', 'UpdateView', 'DeleteView',
    'ModelFormSetView', 'CreateWithInlinesView', 'UpdateWithInlinesView',
    'EmptyInlineFormSet',
)

FORM_TEMPLATE = 'crudwrapper/base_form.html'
DELETE_TEMPLATE = 'crudwrapper/base_delete.html'
FORMSET_TEMPLATE = 'crudwrapper/base_formset.html'

DEFAULT_ERROR_MESSAGE = u"Something went wrong. {} was not saved"
CREATE_MESSAGE = u"<small><em>{}</em></small> created successfully"
CREATE_ERROR_MESSAGE = DEFAULT_ERROR_MESSAGE
UPDATE_MESSAGE = u"<small><em>{}</em></small> updated successfully"
UPDATE_ERROR_MESSAGE = DEFAULT_ERROR_MESSAGE
DELETE_MESSAGE = u"<small><em>{}</em></small> deleted successfully"
DELETE_ERROR_MESSAGE = u"Something went wrong. <small><em>{}</em></small> was not deleted"


class CreateView(FormMessagesMixin, SuccessURLRedirectListMixin, CancelURLMixin, CrispyFormViewMixin, CreateView):
    template_name = FORM_TEMPLATE

    def get_form_valid_message(self):
        msg = CREATE_MESSAGE.format(
            self.object)
        return mark_safe(msg)

    def get_form_invalid_message(self):
        msg = CREATE_ERROR_MESSAGE.format(
            self.model._meta.model_name)
        return mark_safe(msg)


class UpdateView(FormMessagesMixin, SuccessURLRedirectListMixin, CancelURLMixin, CrispyFormViewMixin, UpdateView):
    template_name = FORM_TEMPLATE

    def get_form_valid_message(self):
        msg = UPDATE_MESSAGE.format(
            self.object)
        return mark_safe(msg)

    def get_form_invalid_message(self):
        msg = UPDATE_ERROR_MESSAGE.format(
            self.object)
        return mark_safe(msg)


class DeleteView(FormMessagesMixin, SuccessURLRedirectListMixin, CancelURLMixin, DeleteView):
    template_name = DELETE_TEMPLATE

    def get_form_valid_message(self):
        msg = DELETE_MESSAGE.format(
            self.object)
        return mark_safe(msg)

    def get_form_invalid_message(self):
        msg = DELETE_ERROR_MESSAGE.format(
            self.object)
        return mark_safe(msg)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.success_url = self.get_success_url()  # set value before object is deleted.
        response = super(DeleteView, self).post(request, *args, **kwargs)
        self.messages.success(self.get_form_valid_message(),
                              fail_silently=True)
        return response


class ModelFormSetView(FormSetMessagesMixin, CancelURLMixin, FormSetHelperViewMixin, ModelFormSetView):
    template_name = FORMSET_TEMPLATE

    def get_form_valid_message(self):
        msg = UPDATE_MESSAGE.format(self.model.__name__)
        return mark_safe(msg)

    def get_form_invalid_message(self):
        msg = UPDATE_ERROR_MESSAGE.format(
            self.model.__name__)
        return mark_safe(msg)


class CreateWithInlinesView(FormSetMessagesMixin, CancelURLMixin, FormSetHelperViewMixin, CrispyFormViewMixin, CreateWithInlinesView):
    template_name = FORMSET_TEMPLATE

    def get_form_valid_message(self):
        msg = UPDATE_MESSAGE.format(
            self.object)
        return mark_safe(msg)

    def get_form_invalid_message(self):
        msg = UPDATE_ERROR_MESSAGE.format(
            self.model.__name__)
        return mark_safe(msg)


class UpdateWithInlinesView(FormSetMessagesMixin, CancelURLMixin, FormSetHelperViewMixin, CrispyFormViewMixin, UpdateWithInlinesView):
    template_name = FORMSET_TEMPLATE

    def get_form_valid_message(self):
        msg = UPDATE_MESSAGE.format(
            self.object)
        return mark_safe(msg)

    def get_form_invalid_message(self):
        msg = UPDATE_ERROR_MESSAGE.format(
            self.object)
        return mark_safe(msg)


class EmptyBaseInlineFormSet(BaseInlineFormSet):
    def get_queryset(self, *args, **kwargs):
        return self.model._default_manager.get_queryset().none()


class EmptyInlineFormSet(InlineFormSet):
    """
    Exclude existing objects from inline formset.
    """
    formset_class = EmptyBaseInlineFormSet
