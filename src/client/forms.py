from django.forms import ModelForm

from account.models import CustomUser
from common.django_utils import AsyncModelFormMixin
from typing import Iterable

from django import forms
from django.forms import Form
from django.utils.translation import gettext_lazy as _t
from asgiref.sync import sync_to_async

from common.django_utils import AsyncModelFormMixin
from .models import PlanChoice

class UpdateUserForm(AsyncModelFormMixin, ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'first_name',
            'last_name',
        )

class UpdateSubscriptionForm(Form, AsyncModelFormMixin):
    plan_choices = forms.ChoiceField(
        label=_t("Update Plan Choices"),
    )

    def __init__(
            self,
            *args,
            exclude: Iterable[str] | None = None,
            **kargs
    ):
        super().__init__(*args, **kargs)
        
        plan_choices = PlanChoice.objects.filter(is_active=True)
        
        if exclude:
            plan_choices = plan_choices.exclude(plan_code__in=exclude)

        self.fields["plan_choices"].choices = (
            (plan_choice.plan_code, plan_choice.name) for plan_choice in plan_choices
        )
        
    @classmethod
    async def ainit(cls, *args, **kargs)-> "UpdateSubscriptionForm":
        @sync_to_async
        def call_init() -> UpdateSubscriptionForm:
            return UpdateSubscriptionForm(*args, **kargs)
        
        return await call_init()