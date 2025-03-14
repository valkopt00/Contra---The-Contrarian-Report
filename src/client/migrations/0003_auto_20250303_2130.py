# Generated by Django 5.1.5 on 2025-03-03 21:30

from django.db import migrations


def populate_plan_choice(apps, schema_editor):
    PlanChoice = apps.get_model('client', 'PlanChoice')
    PlanChoice.objects.create(
        plan = 'ST',
        name = 'Standard',
        cost = '2.99',
        is_active = True,
        description1 = 'Get access to standard articles and reports',
        description2 = 'Limited access',
        external_plan_id = 'P-49912523W5800615MM7I2T5Q',
        external_api_url = 'https://www.paypal.com/sdk/js?client-id=AdJehFhXVASN5T7vYUDM_j5jUYgNRQleBtAjZ2jkb2VjJY7QIccnMhg1yFIXtbCGJmUeO2qN01tVLvL4&vault=true&intent=subscription',
        external_style_json = """{
            "shape": "pill",
            "color": "blue",
            "layout": "vertical",
            "label": "subscribe"
        }"""
    )

    PlanChoice.objects.create(
        plan = 'PR',
        name = 'Premium',
        cost = '7.99',
        is_active = True,
        description1 = 'Get access to premium articles and reports',
        description2 = 'Unlimited access',
        external_plan_id = 'P-9RS34182J06111022M7I2ZJA',
        external_api_url = 'https://www.paypal.com/sdk/js?vault=true&intent=subscription',
        external_style_json = """{
            "shape": "pill",
            "color": "gold",
            "layout": "vertical",
            "label": "subscribe"
        }"""
    )


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_planchoice_alter_subscription_cost'),
    ]

    operations = [
        migrations.RunPython(populate_plan_choice),
    ]
