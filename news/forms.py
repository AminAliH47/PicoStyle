from django import forms
from news.models import News

CREATE_FORM = {
    'title': forms.TextInput(
        attrs={'placeholder': 'Title of news'}),
    'category': forms.SelectMultiple(
        attrs={'class': 'js-example-basic-multiple'}
    ),
    'tag': forms.SelectMultiple(
        attrs={'class': 'js-example-basic-multiple'}
    )
}


class NewsSuperuserForm(forms.ModelForm):
    """news field form (superuser)"""

    class Meta:
        model = News
        widgets = CREATE_FORM
        fields = ('title', 'image', 'body', 'category', 'tag', 'author', 'status')


class NewsAuthorForm(forms.ModelForm):
    """news field form (author)"""

    class Meta:
        model = News
        widgets = CREATE_FORM
        fields = ('title', 'image', 'body', 'category', 'tag',)
