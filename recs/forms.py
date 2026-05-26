from django import forms
import mojang


_api = mojang.API()


class RecommendationForm(forms.Form):
    mc_username = forms.CharField(max_length=16, label='Your Minecraft Username')
    recommendation = forms.CharField(widget=forms.Textarea, label='Recommendation')

    def clean_mc_username(self):
        username = self.cleaned_data['mc_username']
        uuid = _api.get_uuid(username)
        if not uuid:
            raise forms.ValidationError('Minecraft username not found.')
        self._mc_uuid = uuid
        return username

    def get_uuid(self):
        return getattr(self, '_mc_uuid', '')
