class BootstrapForm(object):
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.bootstrap_exclude_fields:
                continue
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = '请输入' + field.label
            else:
                field.widget.attrs = {'class': 'form-control', 'placeholder': '请输入' + field.label}
