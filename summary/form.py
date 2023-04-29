from django import forms


class SummaryForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'placeholder': '要約したい文章を入力してください。',
                                                        'rows': '10'}),
                           label='テキスト')
