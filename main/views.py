from django.core.mail import EmailMultiAlternatives
from django.shortcuts import (
    render,
    redirect,
)
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
# i18n Section
from django.utils.translation import (
    activate,
    get_language,
)

# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_cookie

from main.forms import RetailerForm
from main import models
from main import forms
from config import settings
from products.mixins import SuperuserAccessMixin


# @method_decorator([vary_on_cookie, cache_page(60 * 15)], name='dispatch')
class Index(generic.TemplateView):
    template_name = "main/pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['m_categories'] = models.MainCategories.objects.all()
        context['main_slider'] = models.MainSlider.objects.all()
        context['brands_slider'] = models.BrandsSlider.objects.all()
        return context


def change_lang(request):
    activate(request.GET['lang'])
    return redirect(request.GET['next'])


def page_not_found(request, exception=None):
    response = render(request, "pages/404.html")
    response.status_code = 404
    return response


def server_error(request):
    response = render(request, "pages/500.html")
    response.status_code = 500
    return response


class BecomeRetailer(generic.CreateView):
    """
    Become retailer form
    """
    model = models.Retailers
    form_class = RetailerForm
    template_name = "main/pages/become_retailer.html"
    success_url = reverse_lazy("main:thanks")

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.experience_info = {
            "how_long": form.cleaned_data["how_long"],
            "manage_people": form.cleaned_data["manage_people"],
            "professional_experience": form.cleaned_data["professional_experience"],
            "luxury_experience": form.cleaned_data["luxury_experience"],
            "open_store": form.cleaned_data["open_store"],
            "owner": form.cleaned_data["owner"],
            "previous_member": form.cleaned_data["previous_member"],
            "wish": form.cleaned_data["wish"],
            "equality": form.cleaned_data["equality"],
        }
        subject = "New request for retailer"

        full_name = f'{form.cleaned_data["gender"]} ' \
                    f'{form.cleaned_data["first_name"]} ' \
                    f'{form.cleaned_data["last_name"]} '
        context = {
            "lang": get_language(),
            "full_name": full_name,
            "address": form.cleaned_data["address"],
            "city": form.cleaned_data["city"],
            "country": form.cleaned_data["country"],
            "email": form.cleaned_data["email"],
            "phone": form.cleaned_data["phone"],
            "zip_code": form.cleaned_data["zip_code"],
            "experience": form.cleaned_data["experience"],
            # =========
            "how_long": form.cleaned_data["how_long"],
            "manage_people": form.cleaned_data["manage_people"],
            "professional_experience": form.cleaned_data["professional_experience"],
            "luxury_experience": form.cleaned_data["luxury_experience"],
            "open_store": form.cleaned_data["open_store"],
            "have_store": form.cleaned_data["have_store"],
            "center_town": form.cleaned_data["center_town"],
            "owner": form.cleaned_data["owner"],
            "previous_member": form.cleaned_data["previous_member"],
            "wish": form.cleaned_data["wish"],
            "equality": form.cleaned_data["equality"],
        }

        html_message = render_to_string(template_name="main/email/email_template.html", context=context)

        text_content = 'This is an important message.'
        # Send email as html template

        # if you want to send real email change "settings.DEFAULT_FROM_EMAIL" to "settings.EMAIL_HOST_USER"
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL,
                                     ["retailer@operstyle.com"])
        msg.attach_alternative(html_message, "text/html")
        msg.send()

        return super().form_valid(form)


def thanks(request):
    """ view for become retailer """
    return render(request, "main/pages/thanks.html")


def store_agent(request):
    """ View for store and agent page (world map) """
    if request.method == "POST" and request.is_ajax:
        code = request.POST['data']
        store = models.StoreAgent.objects.filter(active=True, country_code=code)  # search country in db
        from django.http import JsonResponse
        from django.core.serializers import serialize
        store = serialize(queryset=store, format="json")
        return JsonResponse(store, safe=False)  # send country to front
    context = {
        "stores": models.StoreAgent.objects.get_active_store()
    }
    return render(request, "main/pages/store_agent.html", context)


class MainSizeGuide(generic.ListView):
    """
    List of size guide items
    """
    model = models.SizeGuide
    context_object_name = "sizes"
    template_name = "main/pages/size_guide/main.html"


class SizeGuideWomen(generic.TemplateView):
    """
    Women size guide table view
    """
    template_name = "main/pages/size_guide/women.html"


class SizeGuideMen(generic.TemplateView):
    """
    Men size guide table view
    """
    template_name = "main/pages/size_guide/men.html"


class SpecialProjectsList(generic.ListView):
    """
    List of special projects
    """
    model = models.SpecialProjects
    context_object_name = "items"
    template_name = "main/pages/special_projects.html"


class WorkWithUsList(generic.ListView):
    """
    List of work with us
    """
    model = models.WorkWithUs
    context_object_name = "items"
    template_name = "main/pages/work_with_us.html"


class CreateMainSlider(SuperuserAccessMixin, generic.CreateView):
    """
    Create main slider in admin panel
    """
    model = models.MainSlider
    form_class = forms.MainSliderForm
    template_name = "account/items/pages/create-update.html"
    success_url = reverse_lazy('account:m_ms_list')


class UpdateMainSlider(SuperuserAccessMixin, generic.UpdateView):
    """
    Update main slider in admin panel
    """
    model = models.MainSlider
    form_class = forms.MainSliderForm
    template_name = "account/items/pages/create-update.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_ms_list')


class DeleteMainSlider(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete main slider in admin panel
    """
    model = models.MainSlider
    template_name = "account/items/pages/delete.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_bs_list')


class CreateBrandsSlider(SuperuserAccessMixin, generic.CreateView):
    """
    Create brands slider in admin panel
    """
    model = models.BrandsSlider
    form_class = forms.BrandsSliderForm
    template_name = "account/items/pages/create-update.html"
    success_url = reverse_lazy('account:m_bs_list')


class UpdateBrandsSlider(SuperuserAccessMixin, generic.UpdateView):
    """
    Update brands slider in admin panel
    """
    model = models.BrandsSlider
    form_class = forms.BrandsSliderForm
    template_name = "account/items/pages/create-update.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_bs_list')


class DeleteBrandsSlider(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete brand slider in admin panel
    """
    model = models.BrandsSlider
    template_name = "account/items/pages/delete.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_bs_list')


class CreateMainCategories(SuperuserAccessMixin, generic.CreateView):
    """
    Create main categories (category image on index page) in admin panel
    """
    model = models.MainCategories
    form_class = forms.MainCategoriesForm
    template_name = "account/items/pages/create-update.html"
    success_url = reverse_lazy('account:m_mc_list')


class UpdateMainCategories(SuperuserAccessMixin, generic.UpdateView):
    """
    Update main categories (category image on index page) in admin panel
    """
    model = models.MainCategories
    form_class = forms.MainCategoriesForm
    template_name = "account/items/pages/create-update.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_mc_list')


class DeleteMainCategories(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete main categories (category image on index page) in admin panel
    """
    model = models.MainCategories
    template_name = "account/items/pages/delete.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_bs_list')


class CreateSocialMedia(SuperuserAccessMixin, generic.CreateView):
    """
    Create social media in admin panel
    """
    model = models.SocialMedia
    form_class = forms.SocialMediaForm
    template_name = "account/items/pages/create-update.html"
    success_url = reverse_lazy('account:m_sm_list')


class UpdateSocialMedia(SuperuserAccessMixin, generic.UpdateView):
    """
    Update social media in admin panel
    """
    model = models.SocialMedia
    form_class = forms.SocialMediaForm
    template_name = "account/items/pages/create-update.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_sm_list')


class DeleteSocialMedia(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete social media in admin panel
    """
    model = models.SocialMedia
    template_name = "account/items/pages/delete.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_sm_list')


class CreateSpecialProjects(SuperuserAccessMixin, generic.CreateView):
    """
    Create special projects in admin panel
    """
    model = models.SpecialProjects
    form_class = forms.SpecialProjectsForm
    template_name = "account/items/pages/create-update.html"
    success_url = reverse_lazy('account:m_sp_list')


class UpdateSpecialProjects(SuperuserAccessMixin, generic.UpdateView):
    """
    Update special projects in admin panel
    """
    model = models.SpecialProjects
    form_class = forms.SpecialProjectsForm
    template_name = "account/items/pages/create-update.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_sp_list')


class DeleteSpecialProjects(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete special projects in admin panel
    """
    model = models.SpecialProjects
    template_name = "account/items/pages/delete.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_sp_list')


class CreateWorkWithUs(SuperuserAccessMixin, generic.CreateView):
    """
    Create work with us in admin panel
    """
    model = models.WorkWithUs
    form_class = forms.WorkWithUsForm
    template_name = "account/items/pages/create-update.html"
    success_url = reverse_lazy('account:m_wu_list')


class UpdateWorkWithUs(SuperuserAccessMixin, generic.UpdateView):
    """
    Update work with us in admin panel
    """
    model = models.WorkWithUs
    form_class = forms.WorkWithUsForm
    template_name = "account/items/pages/create-update.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_wu_list')


class DeleteWorkWithUs(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete work with us in admin panel
    """
    model = models.WorkWithUs
    template_name = "account/items/pages/delete.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_wu_list')


class CreateStoreAgent(SuperuserAccessMixin, generic.CreateView):
    """
    Create store and agent in admin panel
    """
    model = models.StoreAgent
    form_class = forms.StoreAgentForm
    template_name = "account/items/pages/create-update.html"
    success_url = reverse_lazy('account:m_sa_list')


class UpdateStoreAgent(SuperuserAccessMixin, generic.UpdateView):
    """
    Update store and agent in admin panel
    """
    model = models.StoreAgent
    form_class = forms.StoreAgentForm
    template_name = "account/items/pages/create-update.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_sa_list')


class DeleteStoreAgent(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete store and agent in admin panel
    """
    model = models.StoreAgent
    template_name = "account/items/pages/delete.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_sa_list')


class CreateSizeGuid(SuperuserAccessMixin, generic.CreateView):
    """
    Create size guide in admin panel
    """
    model = models.SizeGuide
    form_class = forms.SizeGuideForm
    template_name = "account/items/pages/create-update.html"
    success_url = reverse_lazy('account:m_sg_list')


class UpdateSizeGuid(SuperuserAccessMixin, generic.UpdateView):
    """
    Update size guide in admin panel
    """
    model = models.SizeGuide
    form_class = forms.SizeGuideForm
    template_name = "account/items/pages/create-update.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_sg_list')


class DeleteSizeGuid(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete size guide in admin panel
    """
    model = models.SizeGuide
    template_name = "account/items/pages/delete.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:m_sg_list')
