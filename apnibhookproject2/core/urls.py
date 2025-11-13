# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ============================================================================
    # MAIN PORTFOLIO PAGES
    # ============================================================================
    path('', views.portfolio_home, name='home'),
    path('base/', views.get_portfolio_data, name='portfolio_page'),
    path('about/', views.about_page, name='about'),
    path('services/', views.services_page, name='services'),
    path('service/<uuid:service_id>/', views.service_detail, name='service_detail'),
    path('skills/', views.skills_page, name='skills'),
    path('projects/', views.projects_page, name='projects'),
    path('contact/', views.contact_page, name='contact'),
    
    # Project detail
    path('project/<str:project_id>/', views.project_detail, name='project_detail'),
    
    # ============================================================================
    # AUTHENTICATION
    # ============================================================================
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # ============================================================================
    # MODULAR ADMIN DASHBOARD PAGES
    # ============================================================================
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/portfolio-settings/', views.admin_portfolio_settings, name='admin_portfolio_settings'),
    path('admin/about/', views.admin_about, name='admin_about'),
    path('admin/education/', views.admin_education, name='admin_education'),
    path('admin/work-experience/', views.admin_work_experience, name='admin_work_experience'),
    path('admin/services/', views.admin_services, name='admin_services'),
    path('admin/projects/', views.admin_projects, name='admin_projects'),
    path('admin/skills/', views.admin_skills, name='admin_skills'),
    path('admin/contact/', views.admin_contact, name='admin_contact'),
    path('admin/submissions/', views.admin_submissions, name='admin_submissions'),
    
    # ============================================================================
    # CRUD OPERATIONS - PORTFOLIO SETTINGS
    # ============================================================================
    path('admin/settings/update/', views.update_settings, name='update_settings'),
    
    # ============================================================================
    # CRUD OPERATIONS - ABOUT SECTION
    # ============================================================================
    path('admin/about/update/', views.update_about, name='update_about'),
    
    # ============================================================================
    # CRUD OPERATIONS - EDUCATION
    # ============================================================================
    path('admin/education/add/', views.add_education, name='add_education'),
    path('update-education/<uuid:education_id>/', views.update_education, name='update_education'),
    path('admin/education/delete/<uuid:education_id>/', views.delete_education, name='delete_education'),
    
    # ============================================================================
    # CRUD OPERATIONS - WORK EXPERIENCE
    # ============================================================================
    path('admin/work-experience/add/', views.add_work_experience, name='add_work_experience'),
    path('update-work-experience/<uuid:work_experience_id>/', views.update_work_experience, name='update_work_experience'),
    path('admin/work-experience/delete/<uuid:work_experience_id>/', views.delete_work_experience, name='delete_work_experience'),
    
    # ============================================================================
    # CRUD OPERATIONS - SERVICES
    # ============================================================================
    path('admin/services/add/', views.add_service, name='add_service'),
    path('admin/services/update/<uuid:service_id>/', views.update_service, name='update_service'),
    path('admin/services/delete/<uuid:service_id>/', views.delete_service, name='delete_service'),
    
    # ============================================================================
    # CRUD OPERATIONS - PROJECTS
    # ============================================================================
    path('admin/projects/add/', views.add_project, name='add_project'),
    path('admin/projects/update/<uuid:project_id>/', views.update_project, name='update_project'),
    path('admin/projects/delete/<uuid:project_id>/', views.delete_project, name='delete_project'),
    path('admin/projects/add-image/', views.add_project_image, name='add_project_image'),
    path('admin/projects/delete-image/<uuid:image_id>/', views.delete_project_image, name='delete_project_image'),
    
    # ============================================================================
    # CRUD OPERATIONS - SKILLS
    # ============================================================================
    path('admin/skills/add/', views.add_skill, name='add_skill'),
    path('update-skill/<uuid:skill_id>/', views.update_skill, name='update_skill'),
    path('admin/skills/delete/<uuid:skill_id>/', views.delete_skill, name='delete_skill'),
    
    # ============================================================================
    # CRUD OPERATIONS - CONTACT INFORMATION
    # ============================================================================
    path('admin/contact/update/', views.update_contact, name='update_contact'),
    
    # ============================================================================
    # CONTACT FORM SUBMISSIONS
    # ============================================================================
    path('submit-contact/', views.submit_contact_form, name='submit_contact'),
    path('admin/contact/delete-submission/<uuid:submission_id>/', views.delete_submission, name='delete_submission'),
    
    # ============================================================================
    # API ENDPOINTS
    # ============================================================================
    path('api/portfolio-data/', views.api_portfolio_data, name='api_portfolio_data'),
]