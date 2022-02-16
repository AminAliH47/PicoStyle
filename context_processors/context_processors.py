def site_setting_context_processor(request):
    from main.models import SiteSetting

    return {
        'site_setting': SiteSetting.objects.first(),
    }
