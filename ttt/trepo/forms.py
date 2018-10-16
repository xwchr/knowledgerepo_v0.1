from datetime import datetime
from django import forms
#from itertools import chain
from django.contrib.admin.widgets import FilteredSelectMultiple

from dal import autocomplete

from .models import Pub

class PubForm(forms.ModelForm):

    class Meta:
        model = Pub
        fields = '__all__'

    # add form widget to edit 'relatedpubs' reverse relation 'is_related_to'

    is_related_to = forms.ModelMultipleChoiceField(
        queryset=Pub.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
          verbose_name='Publications',
          is_stacked=False
      )
    )

    def __init__(self, *args, **kwargs):
        super(PubForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['is_related_to'].initial = self.instance.is_related_to.all()

            # exclude currently edited item from queryset
            self.fields['is_related_to'].queryset = Pub.objects.exclude(pk=self.instance.pk)
            self.fields['relatedpubs'].queryset = Pub.objects.exclude(pk=self.instance.pk)

    def save(self, commit=True):
        pub = super(PubForm, self).save(commit=False)

        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            pub.is_related_to.set(self.cleaned_data['is_related_to'])

        self.save_m2m = save_m2m
        pub.save()
        self.save_m2m()

        return pub

    # parse date_as_string and check if valid

    def clean_date_as_string(self):

        DEFAULT = '1970/01/01'

        v = self.cleaned_data['date_as_string']

        if v == '':
            return DEFAULT

        err = False
        s = v.split('/')
        try:                            # validate year
            year = int(s[0])
            if year<0 or year>2050:
                err = True
        except ValueError:
            err = True
            year = None
        try:                            # validate month (optional)
            month = int(s[1])
            if month<0 or month>12:
              err = True
        except IndexError:
            month = 1
        except ValueError:
            err = True
        try:                            # validate day (optional)
            day = int(s[2])
            if day<0 or day>31:
              err = True
        except IndexError:
            day = 1
        except ValueError:
            err = True

        vdate = v

        try:
            vdate = '%d/%02d/%02d' % (year, month, day)
            date = datetime.strptime(vdate,'%Y/%m/%d')
        except:
            err = True

        # pass full date string (e.g. 2016/12/01) to save method

        self.cleaned_data['date_as_string_full'] = vdate

        if err:
            raise forms.ValidationError(u"Error in date format")

        return v