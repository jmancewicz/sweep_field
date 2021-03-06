from flask.ext.wtf import Form
from wtforms import widgets, Field, TextField, IntegerField, validators, FormField, HiddenField

from wtforms.compat import text_type, iteritems
import numpy as np

class SweepForm(Form):
    start = IntegerField('Start', [validators.required()])
    end   = IntegerField('End', [validators.required()])
    incr  = IntegerField('Incr', [validators.required()])
    use_range = HiddenField('Use_Range', [validators.required()])

    def __init__(self, formdata=None, obj=None, prefix='', data=None, meta=None, **kwargs):
        super(SweepForm, self).__init__(formdata, obj, prefix, data, meta, kwargs)

    def range(self):
        start = self.start.data
        end = self.end.data
        incr = self.incr.data
        use_range = self.use_range.data == '1'

        if incr == 0:
            incr = 1

        if not use_range:
            return [start]
        else:
            if np.sign(end - start) != np.sign(incr):
                return [start,end]
            else:
                output = range(start, end, incr)
                output.append(end)
                return output

class RowWidget(object):
    """
    Renders a list of fields as a set of table rows with th/td pairs.

    If `with_table_tag` is True, then an enclosing <table> is placed around the
    rows.

    Hidden fields will not be displayed with a row, instead the field will be
    pushed into a subsequent table row to ensure XHTML validity. Hidden fields
    at the end of the field list will appear outside the table.
    """
    def __init__(self):
        pass

    def __call__(self, field, **kwargs):
        html = []
        kwargs.setdefault('id', field.id)
        with_div = True
        expended = False

        exp_text = 'style=display:none' if expended else ''

        if with_div:
            html.append('<div>')
        html.append('<span %s>' % widgets.html_params(**kwargs))
        hidden = ''
        html.append('<span class="range-span">')
        for subfield in field:
            if subfield.type == 'HiddenField':
                hidden += text_type(subfield)
            else:
                html.append('<div class="range-div">%s%s</div>' % (hidden, text_type(subfield)))
                hidden = ''

        html.append('</span>')
        html.append('<button type="button" class="btn btn-default btn-sm" id="%s-toggle-button"  name="%s-toggle-button" style="font-size: 16px;">' % (field.name, field.name))
        html.append('  <span></span>')
        html.append('</button>')
        html.append('</span>')

        if with_div:
            html.append('</div>')

        if hidden:
            html.append(hidden)

        return widgets.HTMLString(''.join(html))

class RowFormField(FormField):
    """
    Encapsulate a form as a field in another form.

    :param form_class:
        A subclass of Form that will be encapsulated.
    :param separator:
        A string which will be suffixed to this field's name to create the
        prefix to enclosed fields. The default is fine for most uses.
    """
    widget = RowWidget()
    def __init__(self, form_class, label=None, validators=None, separator='-', tooltip='', **kwargs):
        super(RowFormField, self).__init__(form_class, label, validators, separator, **kwargs)
        self.tooltip = tooltip


