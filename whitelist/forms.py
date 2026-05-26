from django import forms
import mojang


_api = mojang.API()


class WhitelistForm(forms.Form):
    mc_username = forms.CharField(max_length=16, label='Minecraft Username')
    discord_handle = forms.CharField(max_length=100, label='Discord Handle')
    reason = forms.CharField(widget=forms.Textarea, required=False, label='Reason for Joining')

    def clean_mc_username(self):
        username = self.cleaned_data['mc_username']
        uuid = _api.get_uuid(username)
        if not uuid:
            raise forms.ValidationError('Minecraft username not found.')
        self._mc_uuid = uuid
        return username

    def get_uuid(self):
        return getattr(self, '_mc_uuid', '')
