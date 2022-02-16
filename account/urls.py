from django.urls import path
from news import views as n_views
from newsletter import views as nw_views
from products import views as p_views
from pages import views as pp_views
from discount import views as d_views
from messages import views as mm_views
from account import views
from main import views as m_views

app_name = 'account'

urlpatterns = (
    path('', views.Index.as_view(), name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('change-password/<int:pk>', views.change_password, name='change_password'),
    # url for account app
    path('suppliers/create', views.CreateSeller.as_view(), name='s_create'),
    path('suppliers/update/<int:pk>', views.UpdateSeller.as_view(), name='s_update'),
    path('suppliers/delete/<int:pk>', views.DeleteSeller.as_view(), name='s_delete'),
    path('suppliers/<int:pk>', views.SellerPanelDetail.as_view(), name='s_detail'),
    path('suppliers/', views.SellerPanelList.as_view(), name='s_list'),
    # url for newsletter app
    path('newsletter/create', nw_views.CreateMessage.as_view(), name='nw_create'),
    path('newsletter/delete/<int:pk>', nw_views.DeleteMessage.as_view(), name='nw_delete'),
    path('newsletter/', nw_views.MessagesList.as_view(), name='nw_list'),
    path('newsletter/subscribers/delete/<int:pk>', nw_views.DeleteSubscriber.as_view(), name='nws_delete'),
    path('newsletter/subscribers/', nw_views.SubscribersList.as_view(), name='nws_list'),
    # url for news app
    path('news/create', n_views.CreateNews.as_view(), name='n_create'),
    path('news/update/<int:pk>/', n_views.UpdateNews.as_view(), name='n_update'),
    path('news/delete/<int:pk>/', n_views.DeleteNews.as_view(), name='n_delete'),
    path('news/preview/<int:pk>/', views.PreviewNews.as_view(), name='n_preview'),
    path('news/', views.NewsPanelList.as_view(), name='n_list'),
    # url for news category
    path('news/category/create', n_views.CreateNewsCategory.as_view(), name='nc_create'),
    path('news/category/update/<int:pk>/', n_views.UpdateNewsCategory.as_view(), name='nc_update'),
    path('news/category/delete/<int:pk>/', n_views.DeleteNewsCategory.as_view(), name='nc_delete'),
    path('news/category/', views.NewsCategoryList.as_view(), name='nc_list'),
    # url for brands app
    path('brands/preview/<int:pk>/', views.PreviewBrands.as_view(), name='b_preview'),
    path('brands/', views.BrandsPanelList.as_view(), name='b_list'),
    # url for product app
    path('products/create', p_views.CreateProducts.as_view(), name='p_create'),
    path('products/update/<int:pk>/', p_views.UpdateProducts.as_view(), name='p_update'),
    path('products/delete/<int:pk>/', p_views.DeleteProducts.as_view(), name='p_delete'),
    path('products/preview/<int:pk>/', views.PreviewProduct.as_view(), name='p_preview'),
    path('products/', views.ProductPanelList.as_view(), name='p_list'),
    # - url for product category
    path('products/category/create', p_views.CreateCategory.as_view(), name='pc_create'),
    path('products/category/update/<int:pk>/', p_views.UpdateCategory.as_view(), name='pc_update'),
    path('products/category/delete/<int:pk>/', p_views.DeleteCategory.as_view(), name='pc_delete'),
    path('products/category/', views.ProductCategoryList.as_view(), name='pc_list'),
    # - url for product price percent
    path('products/percent/update/<int:pk>/', p_views.UpdateProductPercent.as_view(), name='ppp_update'),
    path('products/percent/', views.ProductPercentList.as_view(), name='ppp_list'),
    # - Product price management
    path('products/manage-price/', views.ManagePriceList.as_view(), name='ppm_list'),
    # -- Product price increase
    path('products/manage-price/increase/create', p_views.CreateIncrease.as_view(), name='pi_create'),
    path('products/manage-price/increase/update/<int:pk>/', p_views.UpdateIncrease.as_view(), name='pi_update'),
    path('products/manage-price/increase/delete/<int:pk>/', p_views.DeleteIncrease.as_view(), name='pi_delete'),
    path('products/manage-price/increase/', views.IncreaseList.as_view(), name='pi_list'),
    # -- Discount app
    path('products/manage-price/discounts/create', d_views.CreateDiscounts.as_view(), name='d_create'),
    path('products/manage-price/discounts/update/<int:pk>/', d_views.UpdateDiscounts.as_view(), name='d_update'),
    path('products/manage-price/discounts/delete/<int:pk>/', d_views.DeleteDiscounts.as_view(), name='d_delete'),
    path('products/manage-price/discounts/', views.DiscountList.as_view(), name='d_list'),
    # -- url for product show/hide status
    path('discount/show-hide/create/', d_views.CreateShow.as_view(), name='ds_create'),
    path('discount/show-hide/update/<int:pk>', d_views.UpdateShow.as_view(), name='ds_update'),
    path('discount/show-hide/delete/<int:pk>', d_views.DeleteShow.as_view(), name='ds_delete'),
    path('discount/show-hide/', views.ShowDiscountList.as_view(), name='ds_list'),
    # -- url for product show/hide status
    path('products/show-hide/create/', p_views.CreateShow.as_view(), name='ps_create'),
    path('products/show-hide/update/<int:pk>', p_views.UpdateShow.as_view(), name='ps_update'),
    path('products/show-hide/delete/<int:pk>', p_views.DeleteShow.as_view(), name='ps_delete'),
    path('products/show-hide/', views.ShowProductsList.as_view(), name='ps_list'),
    # url for Items
    path('items/', views.ItemsList.as_view(), name="i_list"),
    # - Main Slider
    path('items/main-slider/create', m_views.CreateMainSlider.as_view(), name="m_ms_create"),
    path('items/main-slider/update/<int:pk>', m_views.UpdateMainSlider.as_view(), name="m_ms_update"),
    path('items/main-slider/delete/<int:pk>', m_views.DeleteMainSlider.as_view(), name="m_ms_delete"),
    path('items/main-slider/', views.MainSliderList.as_view(), name="m_ms_list"),
    # - Brands Slider
    path('items/brands-slider/create', m_views.CreateBrandsSlider.as_view(), name="m_bs_create"),
    path('items/brands-slider/update/<int:pk>', m_views.UpdateBrandsSlider.as_view(), name="m_bs_update"),
    path('items/brands-slider/delete/<int:pk>', m_views.DeleteBrandsSlider.as_view(), name="m_bs_delete"),
    path('items/brands-slider/', views.BrandsSliderList.as_view(), name="m_bs_list"),
    # - Main Categories
    path('items/main-categories/create', m_views.CreateMainCategories.as_view(), name="m_mc_create"),
    path('items/main-categories/update/<int:pk>', m_views.UpdateMainCategories.as_view(), name="m_mc_update"),
    path('items/main-categories/delete/<int:pk>', m_views.DeleteMainCategories.as_view(), name="m_mc_delete"),
    path('items/main-categories/', views.MainCategoriesList.as_view(), name="m_mc_list"),
    # - Social media
    path('items/social-media/create', m_views.CreateSocialMedia.as_view(), name="m_sm_create"),
    path('items/social-media/update/<int:pk>', m_views.UpdateSocialMedia.as_view(), name="m_sm_update"),
    path('items/social-media/delete/<int:pk>', m_views.DeleteSocialMedia.as_view(), name="m_sm_delete"),
    path('items/social-media/', views.SocialMediaList.as_view(), name="m_sm_list"),
    # - Special projects
    path('items/special-project/create', m_views.CreateSpecialProjects.as_view(), name="m_sp_create"),
    path('items/special-project/update/<int:pk>', m_views.UpdateSpecialProjects.as_view(), name="m_sp_update"),
    path('items/special-project/delete/<int:pk>', m_views.DeleteSpecialProjects.as_view(), name="m_sp_delete"),
    path('items/special-project/', views.SpecialProjectsList.as_view(), name="m_sp_list"),
    # - Work with us
    path('items/work-with-us/create', m_views.CreateWorkWithUs.as_view(), name="m_wu_create"),
    path('items/work-with-us/update/<int:pk>', m_views.UpdateWorkWithUs.as_view(), name="m_wu_update"),
    path('items/work-with-us/delete/<int:pk>', m_views.DeleteWorkWithUs.as_view(), name="m_wu_delete"),
    path('items/work-with-us/', views.WorkWithUsList.as_view(), name="m_wu_list"),
    # - Store and Agent
    path('items/store-agent/create', m_views.CreateStoreAgent.as_view(), name="m_sa_create"),
    path('items/store-agent/update/<int:pk>', m_views.UpdateStoreAgent.as_view(), name="m_sa_update"),
    path('items/store-agent/delete/<int:pk>', m_views.DeleteStoreAgent.as_view(), name="m_sa_delete"),
    path('items/store-agent/', views.StoreAgentList.as_view(), name="m_sa_list"),
    # - Size guide
    path('items/size-guide/create', m_views.CreateSizeGuid.as_view(), name="m_sg_create"),
    path('items/size-guide/update/<int:pk>', m_views.UpdateSizeGuid.as_view(), name="m_sg_update"),
    path('items/size-guide/delete/<int:pk>', m_views.DeleteSizeGuid.as_view(), name="m_sg_delete"),
    path('items/size-guide/', views.SizeGuideList.as_view(), name="m_sg_list"),
    # url for Pages app
    path('pages/create', pp_views.CreatePages.as_view(), name="pp_create"),
    path('pages/update/<int:pk>', pp_views.UpdatePages.as_view(), name="pp_update"),
    path('pages/delete/<int:pk>', pp_views.DeletePages.as_view(), name="pp_delete"),
    path('pages/', views.PagesList.as_view(), name="pp_list"),
    # url for Messages app
    path('messages/create-ajax', mm_views.create_message, name="mm_create_ajax"),
    path('messages/create', mm_views.CreateMassages.as_view(), name="mm_create"),
    path('messages/update/<int:pk>', mm_views.UpdateMassages.as_view(), name="mm_update"),
    path('messages/delete/<int:pk>', mm_views.DeleteMassages.as_view(), name="mm_delete"),
    path('messages/<int:pk>', views.MessagesDetail.as_view(), name="mm_detail"),
    path('messages/', views.MessagesList.as_view(), name="mm_list"),

)
