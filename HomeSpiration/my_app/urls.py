from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views
from .views import chatbot,user_chatbot


urlpatterns = [
    path('',views.index,name='index'),
    path('professional_home',views.professional_dashboard,name='professional_dashboard'),
    path('login/',views.loginnew,name='login'),
    path('signup/',views.register_normal_user,name='signup'),
    path('user_signup/',views.user_signup,name='user_signup'),
    path('register/professional/',views.register_professional,name='register_professional'),
    path('about',views.about,name='about'),
    path('logout/',views.logoutp,name='logout'),
    path('send_email/', views.send_email, name='send_email'),
    path('save_to_ideabook/', views.save_to_ideabook, name='save_to_ideabook'),
    path('ideabook/', views.ideabook, name='ideabook'),
    path('generate_3d/', views.generate_3d_view, name='generate_3d'),
    path('view_3d_model/', views.view_3d_model, name='view_3d_model'),
    path('meeting/', views.videocall, name='meeting'),
    path('join/', views.join_room, name='join'),
    
    # path('logout/',views.logout,name='logout'),

    path('submit-professional-type-services/', views.submit_professional_type_services, name='submit_professional_type_services'),
    path('submit-professional-website-info/', views.submit_professional_website_info, name='submit_professional_website_info'),
    path('submit-professional-final-details/', views.submit_professional_final_details, name='submit_professional_final_details'),
    path('Design/', views.generate_image_from_txt, name='Design'),
    path('user_design/', views.user_generate_image_from_txt, name='user_design'),
    path('chatbot/', chatbot, name='chatbot'),
    path('user_chatbot/', user_chatbot, name='user_chatbot'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('add_project/', views.add_project, name='add_project'),
    path('show-projects/', views.show_projects, name='show_projects'),
    path('user_project_view/', views.user_project_view, name='user_project_view'),
    path('project-detail/<int:project_id>/', views.project_detail, name='project_detail'),
    path('edit_professional_details/', views.edit_professional_details, name='edit_professional_details'),
    path('project-detail/<int:project_id>/', views.project_detail, name='project_detail'),
    path('add_layout/', views.add_layout500to1000, name='add_layout500to1000'), #url for layout 500 to 1000
    path('add_layout1/', views.add_layout1000to1500, name='add_layout1000to1500'), #url for layout 1000 to 1500
    path('add_layout2/', views.add_layout1500to2000, name='add_layout1500to2000'), #url for layout 1500 to 2000
    path('search_layouts/', views.search_layouts, name='search_layouts'), #url for searching layouts
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


