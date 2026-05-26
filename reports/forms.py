from django import forms
import mojang


class IssueReportForm(forms.Form):
    mc_username = forms.CharField(max_length=16, label='Your Minecraft Username')
    short_description = forms.CharField(max_length=200, label='Short Description')
    long_description = forms.CharField(widget=forms.Textarea, label='Full Description')

    def clean_mc_username(self):
        username = self.cleaned_data['mc_username']
        try:
            profile = mojang.MojangAPI.get_profile(username)
            if profile is None:
                raise forms.ValidationError('Minecraft username not found.')
            self._mc_uuid = profile.id
        except Exception:
            raise forms.ValidationError('Could not verify Minecraft username.')
        return username

    def get_uuid(self):
        return getattr(self, '_mc_uuid', '')
