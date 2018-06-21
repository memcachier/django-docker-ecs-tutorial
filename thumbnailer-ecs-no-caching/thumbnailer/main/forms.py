from django import forms


class ThumbnailForm(forms.Form):
    image_url = forms.URLField(label='Image URL')
    thumbnail_size = forms.ChoiceField(
        label='Thumbnail size (largest dim.)',
        choices=[(64, '64'), (128, '128'), (256, '256')])
