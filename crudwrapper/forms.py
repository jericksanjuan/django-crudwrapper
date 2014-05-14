from django.forms import ModelForm, Form
from django.core.exceptions import ImproperlyConfigured

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML


__all__ = (
    'CrispyFormMixin', 'CrispyModelForm', 'CrispyForm', 'CrispyFormViewMixin',
    'CrispyFormSetHelper', 'FormSetHelperViewMixin'
)


class CrispyFormMixin(object):

    """
    Mixin that adds a helper property to the form.

    """
    @property
    def helper(self):
        if not hasattr(self, '_helper'):
            self._helper = FormHelper(form=self)
            self._helper.form_tag = False
            self.set_layout()
        return self._helper

    def set_layout(self):
        """ Update this method if you want a custom layout. """
        pass


class CrispyModelForm(CrispyFormMixin, ModelForm):
    pass


class CrispyForm(CrispyFormMixin, Form):
    pass


class CrispyFormViewMixin(object):
    """
    Auto create a CrispyModelForm for views without form_class defined
    """
    def get_form_class(self):
        """
        Returns the form class to use in this view.
        """
        if self.form_class is not None:
            return self.form_class

        form_class = super(CrispyFormViewMixin, self).get_form_class()
        crispy_form_class = type(form_class)(form_class.__name__,
                                (CrispyFormMixin, form_class), dict(Meta=form_class.Meta))
        return crispy_form_class


class CrispyFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(CrispyFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.form_class = 'form-horizontal'
        self.label_class = 'col-lg-2'
        self.field_class = 'col-lg-8'
        self.render_required_fields = True
        self.error_text_inline = True

        self.set_layout()

    def set_layout(self):
        pass

    def wrap_with_panel(self, fields, heading="", css_class="panel panel-default"):
        layout = Layout(
            Div(css_class=css_class)
        )
        for field in fields:
            layout[0].append(field)

        if heading:
            layout[0].insert(0, HTML('<div class="panel-heading">{}</div>'.format(heading)))

        return layout

    def set_panel_layout(self, fields, **kwargs):
        self.layout = self.wrap_with_panel(fields, **kwargs)


class FormSetHelperViewMixin(object):
    """
    Add crispy form helper to context for

    formset_helper = FormsetHelper class to add to context
    formset_helper_name = the context name to use
    formset_fields = fields to include for panel layout
    formset_panel_layout = toggle use of panel of layout
    formset_panel_heading = text for the panel heading
    formset_panel_css = "the css class for the panel div
    """
    formset_helper = CrispyFormSetHelper
    formset_helper_name = 'helper'
    formset_fields = []
    formset_panel_layout = False
    formset_panel_heading = ''
    formset_panel_css = "panel panel-default"

    def get_formset_helper(self):
        """
        Return a list of formset helpers always.
        """
        if not self.formset_helper:
            raise ImproperlyConfigured("The formset_helper class cannot be None!")
        return self.formset_helper

    def get_formset_helper_name(self):
        """
        Always return a list of formset helper names.
        """
        if not self.formset_helper_name:
            raise ImproperlyConfigured("The formset_helper_name cannot be blank!")
        return self.formset_helper_name

    def get_formset_panel_heading(self):
        """
        Override to set panel heading dynamically.
        """
        return self.formset_panel_heading

    def get_context_data(self, *args, **kwargs):
        context = super(FormSetHelperViewMixin, self).get_context_data(*args, **kwargs)
        helper = self.get_formset_helper()()
        if self.formset_panel_layout:
            helper.set_panel_layout(self.formset_fields, heading=self.get_formset_panel_heading(),
                                    css_class=self.formset_panel_css)
        context[self.get_formset_helper_name()] = helper
        return context
