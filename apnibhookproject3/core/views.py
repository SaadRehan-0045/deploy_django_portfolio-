# views.py
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from supabase import create_client
from django.utils.safestring import mark_safe
import re
import time
from django.contrib.auth.decorators import login_required

# Initialize Supabase client
SUPABASE_URL = "https://rlcqfmoginbchsidwawr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsY3FmbW9naW5iY2hzaWR3YXdyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NzYwODMsImV4cCI6MjA3NjI1MjA4M30.Bputt67mmjY3YgOfO9QMSOJcmUtG5HBLEXKWYqCJYOU"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# NEW FUNCTION: Get portfolio settings
def get_portfolio_settings():
    """Get portfolio settings from Supabase"""
    try:
        print("=== DEBUG: Fetching portfolio settings ===")
        settings_response = supabase.table("portfolio_settings").select("*").limit(1).execute()
        print(f"DEBUG: Settings response: {settings_response}")
        print(f"DEBUG: Settings data: {settings_response.data}")
        
        if settings_response.data:
            settings = settings_response.data[0]
            print(f"DEBUG: Found settings: {settings}")
            
            # Convert profession_text to list if it's a string
            profession_text = settings.get('profession_text', [])
            if isinstance(profession_text, str):
                # If it's a string, try to convert from JSON or split by comma
                try:
                    import json
                    profession_text = json.loads(profession_text)
                except:
                    # If not JSON, split by comma
                    profession_text = [p.strip() for p in profession_text.split(',') if p.strip()]
            
            settings['profession_text'] = profession_text
            print(f"DEBUG: Profession array: {profession_text}")
            return settings
        else:
            print("DEBUG: No settings found in database")
            return {}
            
    except Exception as e:
        print(f"ERROR fetching settings: {e}")
        return {}

# Authentication check decorator
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('logged_in'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

# ============================================================================
# PUBLIC PORTFOLIO VIEWS
# ============================================================================

def portfolio_home(request):
    """Main portfolio website view - Fully Dynamic"""
    try:
        # USE THE NEW FUNCTION: Get portfolio settings
        settings = get_portfolio_settings()
        
        # Get about section
        about_response = supabase.table("about_section").select("*").limit(1).execute()
        about = about_response.data[0] if about_response.data else {}
        
        # Get services
        services_response = supabase.table("services").select("*").execute()
        services = services_response.data if services_response.data else []
        
        # Get projects
        projects_response = supabase.table("projects").select("*").execute()
        projects = projects_response.data if projects_response.data else []
        
        # Get skills
        skills_response = supabase.table("skills").select("*").execute()
        skills = skills_response.data if skills_response.data else []
        
        # Get education
        education_response = supabase.table("education").select("*").order("year_start", desc=True).execute()
        education = education_response.data if education_response.data else []
        
        # Get work experience
        work_experience_response = supabase.table("work_experience").select("*").order("year_start", desc=True).execute()
        work_experience = work_experience_response.data if work_experience_response.data else []
        
        # Get contact info
        contact_response = supabase.table("contact_info").select("*").limit(1).execute()
        contact_info = contact_response.data[0] if contact_response.data else {
            'phone': '', 'email': '', 'address': '',
            'linkedin_url': '', 'facebook_url': '', 'instagram_url': '', 'skype_url': '',
            'whatsapp_url': '', 'twitter_url': '', 'freelancer_url': '', 'fiverr_url': '', 'upwork_url': ''
        }
        
        context = {
            'settings': settings,
            'about': about,
            'services': services,
            'projects': projects,
            'skills': skills,
            'education': education,
            'work_experience': work_experience,
            'contact_info': contact_info,  # This now includes new fields
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/home.html', context)
        
    except Exception as e:
        print(f"Error: {e}")
        # Return empty data if there's an error
        context = {
            'settings': get_portfolio_settings(),
            'about': {},
            'services': [],
            'projects': [],
            'skills': [],
            'education': [],
            'work_experience': [],
            'contact_info': {
                'phone': '', 'email': '', 'address': '',
                'linkedin_url': '', 'facebook_url': '', 'instagram_url': '', 'skype_url': '',
                'whatsapp_url': '', 'twitter_url': '', 'freelancer_url': '', 'fiverr_url': '', 'upwork_url': ''
            },
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/home.html', context)


# Add this function to your views.py - place it with the other portfolio views
def get_portfolio_data(request):
    """Get portfolio data for base template"""
    try:
        # Fetch portfolio settings from Supabase
        response = supabase.table("portfolio_settings").select("*").execute()
        
        if response.data:
            # Get the first record (assuming you have only one row)
            portfolio_data = response.data[0]
            
            # Map the data to variables - USE 'settings' as variable name
            settings = {
                'user_name': portfolio_data.get('user_name', 'Harry'),
                'profession': portfolio_data.get('profession', 'Video Editor'),
                'resume_url': portfolio_data.get('resume_url', ''),
                'github_url': portfolio_data.get('github_url', ''),
                'greeting_text': portfolio_data.get('greeting_text', ''),
                'user_display_r': portfolio_data.get('user_display_r', ''),
                'profession_teo': portfolio_data.get('profession_teo', ''),
                'description_teo': portfolio_data.get('description_teo', ''),
                'welcome_text': portfolio_data.get('welcome_text', ''),
                'cta_text': portfolio_data.get('cta_text', ''),
                'profile_image': portfolio_data.get('profile_image', ''),
            }
            return render(request, 'portfolio/base.html', {'settings': settings})
        else:
            # Return default data if no settings found
            settings = {
                'user_name': 'Harry',
                'profession': 'Video Editor',
                'resume_url': '',
                'github_url': '',
                'greeting_text': '',
                'user_display_r': '',
                'profession_teo': '',
                'description_teo': '',
                'welcome_text': '',
                'cta_text': '',
                'profile_image': '',
            }
            return render(request, 'portfolio/base.html', {'settings': settings})
            
    except Exception as e:
        print(f"Error in get_portfolio_data: {e}")
        # Return default data on error
        settings = {
            'user_name': 'Harry',
            'profession': 'Video Editor',
            'resume_url': '',
            'github_url': '',
            'greeting_text': '',
            'user_display_r': '',
            'profession_teo': '',
            'description_teo': '',
            'welcome_text': '',
            'cta_text': '',
            'profile_image': '',
        }
        return render(request, 'portfolio/base.html', {'settings': settings})




# ============================================================================
# ADDITIONAL FUNCTIONALITY
# ============================================================================

# Admin function to add project images
@login_required
def add_project_image(request):
    """Add image to project"""
    if request.method == 'POST':
        try:
            project_id = request.POST.get('project_id')
            image_url = request.POST.get('image_url')
            image_order = request.POST.get('image_order', 0)
            
            response = supabase.table("project_images").insert({
                "project_id": project_id,
                "image_url": image_url,
                "image_order": image_order
            }).execute()
            
            messages.success(request, 'Project image added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding project image: {str(e)}')
    
    return redirect('admin_projects')

# Admin function to delete project image
@login_required
def delete_project_image(request, image_id):
    """Delete project image"""
    try:
        response = supabase.table("project_images").delete().eq("id", image_id).execute()
        messages.success(request, 'Project image deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting project image: {str(e)}')
    
    return redirect('admin_projects')

# Project detail view
def project_detail(request, project_id):
    """Display detailed project view"""
    try:
        # Get project details
        project_response = supabase.table("projects").select("*").eq("id", project_id).execute()
        
        if not project_response.data:
            messages.error(request, 'Project not found!')
            return redirect('portfolio_home')
        
        project = project_response.data[0]
        
        # Get project images
        images_response = supabase.table("project_images").select("*").eq("project_id", project_id).order("image_order").execute()
        project_images = images_response.data if images_response.data else []
        
        context = {
            'project': project,
            'project_images': project_images,
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/project_detail.html', context)
        
    except Exception as e:
        print(f"Error loading project: {e}")
        messages.error(request, 'Error loading project details!')
        return redirect('portfolio_home')

# API Endpoints
def api_portfolio_data(request):
    """API endpoint to get all portfolio data"""
    try:
        settings_response = supabase.table("portfolio_settings").select("*").execute()
        about_response = supabase.table("about_section").select("*").execute()
        services_response = supabase.table("services").select("*").execute()
        projects_response = supabase.table("projects").select("*").execute()
        
        data = {
            'settings': settings_response.data[0] if settings_response.data else {},
            'about': about_response.data[0] if about_response.data else {},
            'services': services_response.data,
            'projects': projects_response.data
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)






def about_page(request):
    """About page view"""
    try:
        # Get about section
        about_response = supabase.table("about_section").select("*").limit(1).execute()
        about = about_response.data[0] if about_response.data else {}
        
        # Get education
        education_response = supabase.table("education").select("*").order("year_start", desc=True).execute()
        education = education_response.data if education_response.data else []
        
        # Get work experience
        work_experience_response = supabase.table("work_experience").select("*").order("year_start", desc=True).execute()
        work_experience = work_experience_response.data if work_experience_response.data else []
        
        # USE THE NEW FUNCTION: Get settings
        settings = get_portfolio_settings()
        
        context = {
            'about': about,
            'education': education,
            'work_experience': work_experience,
            'settings': settings,
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/about.html', context)
        
    except Exception as e:
        print(f"Error loading about page: {e}")
        context = {
            'about': {},
            'education': [],
            'work_experience': [],
            'settings': get_portfolio_settings(),
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/about.html', context)

def services_page(request):
    """Services page view"""
    try:
        services_response = supabase.table("services").select("*").execute()
        services = services_response.data if services_response.data else []
        
        # ADD SETTINGS TO CONTEXT
        settings = get_portfolio_settings()
        
        context = {
            'services': services,
            'settings': settings,
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/services.html', context)
        
    except Exception as e:
        print(f"Error loading services page: {e}")
        context = {
            'services': [],
            'settings': get_portfolio_settings(),
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/services.html', context)

def service_detail(request, service_id):
    """Service detail page view"""
    try:
        service_response = supabase.table("services").select("*").eq("id", service_id).execute()
        service = service_response.data[0] if service_response.data else None
        
        if not service:
            return redirect('services')
        
        # ADD SETTINGS TO CONTEXT
        settings = get_portfolio_settings()
        
        context = {
            'service': service,
            'settings': settings,
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/service_detail.html', context)
        
    except Exception as e:
        print(f"Error loading service detail: {e}")
        return redirect('services')

def skills_page(request):
    """Skills page view"""
    try:
        skills_response = supabase.table("skills").select("*").execute()
        skills = skills_response.data if skills_response.data else []
        
        # USE THE NEW FUNCTION: Get settings
        settings = get_portfolio_settings()
        
        context = {
            'skills': skills,
            'settings': settings,
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/skills.html', context)
        
    except Exception as e:
        print(f"Error loading skills page: {e}")
        context = {
            'skills': [],
            'settings': get_portfolio_settings(),
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/skills.html', context)

def projects_page(request):
    """Projects page view"""
    try:
        projects_response = supabase.table("projects").select("*").execute()
        projects = projects_response.data if projects_response.data else []
        
        # USE THE NEW FUNCTION: Get settings
        settings = get_portfolio_settings()
        
        context = {
            'projects': projects,
            'settings': settings,
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/projects.html', context)
        
    except Exception as e:
        print(f"Error loading projects page: {e}")
        context = {
            'projects': [],
            'settings': get_portfolio_settings(),
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/projects.html', context)

def contact_page(request):
    """Contact page view"""
    try:
        contact_response = supabase.table("contact_info").select("*").limit(1).execute()
        contact_info = contact_response.data[0] if contact_response.data else {
            'phone': '', 'email': '', 'address': '',
            'linkedin_url': '', 'facebook_url': '', 'instagram_url': '', 'skype_url': '',
            # ADD DEFAULT VALUES FOR NEW FIELDS
            'whatsapp_url': '', 'twitter_url': '', 'freelancer_url': '', 'fiverr_url': '', 'upwork_url': ''
        }
        
        # USE THE NEW FUNCTION: Get settings
        settings = get_portfolio_settings()
        
        context = {
            'contact_info': contact_info,
            'settings': settings,
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/contact.html', context)
        
    except Exception as e:
        print(f"Error loading contact page: {e}")
        context = {
            'contact_info': {
                'phone': '', 'email': '', 'address': '',
                'linkedin_url': '', 'facebook_url': '', 'instagram_url': '', 'skype_url': '',
                'whatsapp_url': '', 'twitter_url': '', 'freelancer_url': '', 'fiverr_url': '', 'upwork_url': ''
            },
            'settings': get_portfolio_settings(),
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/contact.html', context)
# ============================================================================
# AUTHENTICATION VIEWS
# ============================================================================

def login_view(request):
    """Login page"""
    # If user is already logged in, redirect to dashboard
    if request.session.get('logged_in'):
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"Login attempt: username={username}, password={password}")
        
        try:
            # Check admin credentials in your custom admin_users table
            response = supabase.table("admin_users").select("*").eq("username", username).execute()
            
            print(f"Database response: {response}")
            
            if response.data:
                admin_user = response.data[0]
                print(f"Found user: {admin_user}")
                
                # Simple password comparison
                if admin_user['password'] == password:
                    # Set session variables
                    request.session['logged_in'] = True
                    request.session['username'] = username
                    request.session.set_expiry(3600)  # 1 hour session
                    
                    messages.success(request, 'Login successful!')
                    print("Login successful, redirecting to dashboard...")
                    return redirect('admin_dashboard')
                else:
                    print(f"Password mismatch: {admin_user['password']} != {password}")
                    messages.error(request, 'Invalid credentials!')
            else:
                print("No user found")
                messages.error(request, 'Invalid credentials!')
                
        except Exception as e:
            print(f"Login error: {e}")
            messages.error(request, f'Login error: {str(e)}')
    
    return render(request, 'portfolio/login.html')

def logout_view(request):
    """Logout user"""
    request.session.flush()
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

# ============================================================================
# MODULAR ADMIN VIEWS
# ============================================================================

@login_required
def admin_dashboard(request):
    """Admin dashboard overview"""
    return render(request, 'admin/dashboard.html')

@login_required
def admin_portfolio_settings(request):
    """Portfolio settings management"""
    settings = get_portfolio_settings()
    return render(request, 'admin/portfolio_settings.html', {'settings': settings})

@login_required
def admin_about(request):
    """About section management"""
    about_response = supabase.table("about_section").select("*").limit(1).execute()
    about = about_response.data[0] if about_response.data else {}
    return render(request, 'admin/about_management.html', {'about': about})

@login_required
def admin_education(request):
    """Education management"""
    education_response = supabase.table("education").select("*").order("year_start", desc=True).execute()
    education = education_response.data if education_response.data else []
    return render(request, 'admin/education_management.html', {'education': education})

@login_required
def admin_work_experience(request):
    """Work experience management"""
    work_experience_response = supabase.table("work_experience").select("*").order("year_start", desc=True).execute()
    work_experience = work_experience_response.data if work_experience_response.data else []
    return render(request, 'admin/work_experience_management.html', {'work_experience': work_experience})

@login_required
def admin_services(request):
    """Services management"""
    services_response = supabase.table("services").select("*").execute()
    services = services_response.data if services_response.data else []
    return render(request, 'admin/services_management.html', {'services': services})

@login_required
def admin_projects(request):
    """Projects management"""
    projects_response = supabase.table("projects").select("*").execute()
    projects = projects_response.data if projects_response.data else []
    return render(request, 'admin/projects_management.html', {'projects': projects})

@login_required
def admin_skills(request):
    """Skills management"""
    skills_response = supabase.table("skills").select("*").execute()
    skills = skills_response.data if skills_response.data else []
    return render(request, 'admin/skills_management.html', {'skills': skills})

@login_required
def admin_contact(request):
    """Contact information management"""
    contact_response = supabase.table("contact_info").select("*").limit(1).execute()
    contact_info = contact_response.data[0] if contact_response.data else {
        'phone': '', 'email': '', 'address': '', 
        'linkedin_url': '', 'facebook_url': '', 'instagram_url': '', 'skype_url': '',
        # ADD DEFAULT VALUES FOR NEW FIELDS
        'whatsapp_url': '', 'twitter_url': '', 'freelancer_url': '', 'fiverr_url': '', 'upwork_url': ''
    }
    return render(request, 'admin/contact_management.html', {'contact_info': contact_info})

@login_required
def admin_submissions(request):
    """Contact submissions management"""
    try:
        contact_submissions_response = supabase.table("contact_submissions").select("*").order("created_at", desc=True).execute()
        contact_submissions = contact_submissions_response.data if contact_submissions_response.data else []
        
        # Ensure each submission has proper datetime handling
        for submission in contact_submissions:
            if 'created_at' in submission:
                # Convert to datetime object if it's a string
                if isinstance(submission['created_at'], str):
                    try:
                        from django.utils.dateparse import parse_datetime
                        parsed_date = parse_datetime(submission['created_at'])
                        if parsed_date:
                            submission['created_at'] = parsed_date
                    except:
                        # If parsing fails, keep the original string
                        pass
        
        return render(request, 'admin/submissions_management.html', {
            'contact_submissions': contact_submissions
        })
        
    except Exception as e:
        print(f"Error fetching submissions: {e}")
        return render(request, 'admin/submissions_management.html', {
            'contact_submissions': []
        })

# ============================================================================
# CRUD OPERATIONS
# ============================================================================

# Portfolio Settings CRUD
@login_required
def update_settings(request):
    """Update portfolio settings - Fully Dynamic with Image Upload"""
    if request.method == 'POST':
        try:
            # Check if settings exist
            existing_response = supabase.table("portfolio_settings").select("*").execute()
            
            # Get current settings to preserve existing data
            current_settings = existing_response.data[0] if existing_response.data else {}
            
            # Initialize Supabase client
            supabase_url = "https://rlcqfmoginbchsidwawr.supabase.co"
            supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsY3FmbW9naW5iY2hzaWR3YXdyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NzYwODMsImV4cCI6MjA3NjI1MjA4M30.Bputt67mmjY3YgOfO9QMSOJcmUtG5HBLEXKWYqCJYOU"
            client = create_client(supabase_url, supabase_key)
            
            # Function to convert line breaks only (without strip)
            def convert_line_breaks(text):
                if text is None:
                    return ''
                # Convert <br> tags and \n to newlines only
                text = text.replace('<br>', '\n')
                text = text.replace('\\n', '\n')
                return text
            
            # Handle profile image upload
            profile_image_url = ""
            profile_img_file = request.FILES.get('profile_img_file')
            
            if profile_img_file:
                try:
                    # Generate unique file name
                    file_extension = profile_img_file.name.split('.')[-1]
                    file_name = f"profile_{request.user.id}_{int(time.time())}.{file_extension}"
                    file_path = f"profile_images/{file_name}"
                    
                    # Read file data
                    file_data = profile_img_file.read()
                    
                    # Upload to Supabase storage
                    response = client.storage.from_('images').upload(
                        path=file_path,
                        file=file_data
                    )
                    
                    # Check if upload was successful
                    if response:
                        # Get public URL
                        public_url_response = client.storage.from_('images').get_public_url(file_path)
                        
                        # Handle different response types
                        if isinstance(public_url_response, str):
                            profile_image_url = public_url_response
                        elif hasattr(public_url_response, 'public_url'):
                            profile_image_url = public_url_response.public_url
                        elif isinstance(public_url_response, dict) and 'publicUrl' in public_url_response:
                            profile_image_url = public_url_response['publicUrl']
                        else:
                            # Construct URL manually as fallback
                            profile_image_url = f"{supabase_url}/storage/v1/object/public/images/{file_path}"
                        
                        print(f"Profile image uploaded successfully! URL: {profile_image_url}")
                    else:
                        print("Profile image upload response was empty")
                        messages.error(request, 'Profile image upload failed: Empty response from storage')
                        return redirect('admin_portfolio_settings')
                        
                except Exception as upload_error:
                    print(f"Profile image upload error: {upload_error}")
                    messages.error(request, f'Error uploading profile image: {str(upload_error)}')
                    return redirect('admin_portfolio_settings')
            
            # Prepare update data
            update_data = {
                "user_name": convert_line_breaks(request.POST.get('user_name', '')),
                "greeting_text2": convert_line_breaks(request.POST.get('greeting_text2', '')),
                "resume_url": convert_line_breaks(request.POST.get('resume_url', '')),
                "github_url": convert_line_breaks(request.POST.get('github_url', '')),
                "greeting_text": convert_line_breaks(request.POST.get('greeting_text', '')),
                "user_display_name": convert_line_breaks(request.POST.get('user_display_name', '')),
                "profession_text": convert_line_breaks(request.POST.get('profession_text', '')),
                "description_text": convert_line_breaks(request.POST.get('description_text', '')),
                "profile_image_url": convert_line_breaks(request.POST.get('profile_image_url', ''))
            }
            
            # Use uploaded image URL if available, otherwise keep existing URL field
            if profile_image_url:
                update_data["profile_image_url"] = profile_image_url
            
            # Debug: Show what's being processed
            print("=== DEBUG: CLEANED FORM DATA ===")
            for key, value in update_data.items():
                original = request.POST.get(key, '')
                print(f"{key}: '{original}' → '{value}'")
            
            # Remove only TRULY empty values
            final_update_data = {}
            for key, value in update_data.items():
                if value:  # This will be False for empty strings
                    final_update_data[key] = value
            
            print(f"DEBUG: Final update data: {final_update_data}")
            
            if existing_response.data:
                # Update existing - only update fields that have new non-empty values
                if final_update_data:
                    response = supabase.table("portfolio_settings").update(final_update_data).eq("id", existing_response.data[0]['id']).execute()
                    messages.success(request, 'Settings updated successfully!')
                else:
                    messages.info(request, 'No changes to update.')
            else:
                # Create new - only if there's at least some data
                if final_update_data:
                    response = supabase.table("portfolio_settings").insert(final_update_data).execute()
                    messages.success(request, 'Settings created successfully!')
                else:
                    messages.warning(request, 'No data provided to create settings.')
            
        except Exception as e:
            messages.error(request, f'Error updating settings: {str(e)}')
    
    return redirect('admin_portfolio_settings')

# About Section CRUD
@login_required
def update_about(request):
    """Update about section - Personal Story and Image Upload"""
    if request.method == 'POST':
        try:
            personal_story = request.POST.get('personal_story', '')
            about_img_file = request.FILES.get('about_img_file')
            
            # Clean the text
            personal_story = personal_story.replace('<br>', '\n').replace('\\n', '\n').strip()
            
            # Initialize Supabase client
            supabase_url = "https://rlcqfmoginbchsidwawr.supabase.co"
            supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsY3FmbW9naW5iY2hzaWR3YXdyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NzYwODMsImV4cCI6MjA3NjI1MjA4M30.Bputt67mmjY3YgOfO9QMSOJcmUtG5HBLEXKWYqCJYOU"
            client = create_client(supabase_url, supabase_key)
            
            about_img_url = ""
            
            # Handle image upload if file was provided
            if about_img_file:
                try:
                    # Generate unique file name
                    file_extension = about_img_file.name.split('.')[-1]
                    file_name = f"about_{request.user.id}_{int(time.time())}.{file_extension}"
                    file_path = f"about_images/{file_name}"
                    
                    # Read file data
                    file_data = about_img_file.read()
                    
                    # Upload to Supabase storage
                    response = client.storage.from_('images').upload(
                        path=file_path,
                        file=file_data
                    )
                    
                    # Check if upload was successful
                    if response:
                        print(f"Upload response: {response}")
                        
                        # Get public URL - FIXED METHOD
                        # The get_public_url method returns a string directly, not an object
                        public_url = client.storage.from_('images').get_public_url(file_path)
                        
                        # Check if it's already a string or has public_url attribute
                        if isinstance(public_url, str):
                            about_img_url = public_url
                        elif hasattr(public_url, 'public_url'):
                            about_img_url = public_url.public_url
                        else:
                            # Construct the URL manually if needed
                            about_img_url = f"{supabase_url}/storage/v1/object/public/images/{file_path}"
                        
                        print(f"Image uploaded successfully! URL: {about_img_url}")
                    else:
                        print("Upload response was empty")
                        messages.error(request, 'Image upload failed: Empty response from storage')
                        return redirect('admin_about')
                        
                except Exception as upload_error:
                    print(f"Supabase upload error: {upload_error}")
                    
                    # Check if it's an RLS policy error
                    if "row-level security policy" in str(upload_error).lower():
                        messages.error(request, 'Storage permissions error. Please check your Supabase storage policies.')
                    else:
                        messages.error(request, f'Error uploading image: {str(upload_error)}')
                    
                    return redirect('admin_about')
            
            # Prepare update data
            update_data = {
                "personal_story": personal_story,
            }
            
            # Only add image URL if we have one
            if about_img_url:
                update_data["about_img_url"] = about_img_url
            
            # Check if about exists and update database
            existing_response = supabase.table("about_section").select("*").execute()
            
            if existing_response.data:
                # Update existing
                response = supabase.table("about_section").update(update_data).eq("id", existing_response.data[0]['id']).execute()
            else:
                # Create new
                response = supabase.table("about_section").insert(update_data).execute()
            
            messages.success(request, 'About section updated successfully!')
            
        except Exception as e:
            messages.error(request, f'Error updating about section: {str(e)}')
    
    return redirect('admin_about')

# Education CRUD Operations
@login_required
def add_education(request):
    """Add new education"""
    if request.method == 'POST':
        try:
            # Function to convert line breaks only
            def convert_line_breaks(text):
                if text is None:
                    return ''
                text = text.replace('<br>', '\n')
                text = text.replace('\\n', '\n')
                return text
            
            response = supabase.table("education").insert({
                "degree": convert_line_breaks(request.POST.get('degree')),
                "institution": convert_line_breaks(request.POST.get('institution')),
                "year_start": request.POST.get('year_start'),
                "year_end": request.POST.get('year_end'),
                "description": convert_line_breaks(request.POST.get('description'))
            }).execute()
            
            messages.success(request, 'Education added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding education: {str(e)}')
    
    return redirect('admin_education')

@login_required
def update_education(request, education_id):
    """Update education"""
    if request.method == 'POST':
        try:
            # Function to convert line breaks only
            def convert_line_breaks(text):
                if text is None:
                    return ''
                text = text.replace('<br>', '\n')
                text = text.replace('\\n', '\n')
                return text
            
            update_data = {
                "degree": convert_line_breaks(request.POST.get('degree')),
                "institution": convert_line_breaks(request.POST.get('institution')),
                "year_start": request.POST.get('year_start'),
                "year_end": request.POST.get('year_end') or None,
                "description": convert_line_breaks(request.POST.get('description')) or None
            }
            
            # Remove None values
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            response = supabase.table("education").update(update_data).eq("id", education_id).execute()
            messages.success(request, 'Education updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating education: {str(e)}')
    
    return redirect('admin_education')

@login_required
def delete_education(request, education_id):
    """Delete education"""
    try:
        response = supabase.table("education").delete().eq("id", education_id).execute()
        messages.success(request, 'Education deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting education: {str(e)}')
    
    return redirect('admin_education')

# Work Experience CRUD Operations
@login_required
def add_work_experience(request):
    """Add new work experience"""
    if request.method == 'POST':
        try:
            # Function to convert line breaks only
            def convert_line_breaks(text):
                if text is None:
                    return ''
                text = text.replace('<br>', '\n')
                text = text.replace('\\n', '\n')
                return text
            
            response = supabase.table("work_experience").insert({
                "job_title": convert_line_breaks(request.POST.get('job_title')),
                "company": convert_line_breaks(request.POST.get('company')),
                "year_start": request.POST.get('year_start'),
                "year_end": request.POST.get('year_end'),
                "description": convert_line_breaks(request.POST.get('description'))
            }).execute()
            
            messages.success(request, 'Work experience added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding work experience: {str(e)}')
    
    return redirect('admin_work_experience')

@login_required
def update_work_experience(request, work_experience_id):
    """Update work experience"""
    if request.method == 'POST':
        try:
            # Function to convert line breaks only
            def convert_line_breaks(text):
                if text is None:
                    return ''
                text = text.replace('<br>', '\n')
                text = text.replace('\\n', '\n')
                return text
            
            update_data = {
                "job_title": convert_line_breaks(request.POST.get('job_title')),
                "company": convert_line_breaks(request.POST.get('company')),
                "year_start": request.POST.get('year_start'),
                "year_end": request.POST.get('year_end') or None,
                "description": convert_line_breaks(request.POST.get('description')) or None
            }
            
            # Remove None values
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            response = supabase.table("work_experience").update(update_data).eq("id", work_experience_id).execute()
            messages.success(request, 'Work experience updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating work experience: {str(e)}')
    
    return redirect('admin_work_experience')

@login_required
def delete_work_experience(request, work_experience_id):
    """Delete work experience"""
    try:
        response = supabase.table("work_experience").delete().eq("id", work_experience_id).execute()
        messages.success(request, 'Work experience deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting work experience: {str(e)}')
    
    return redirect('admin_work_experience')

# Services CRUD Operations
@login_required
def add_service(request):
    """Add new service"""
    if request.method == 'POST':
        try:
            # Function to convert line breaks only
            def convert_line_breaks(text):
                if text is None:
                    return ''
                text = text.replace('<br>', '\n')
                text = text.replace('\\n', '\n')
                return text
            
            title = convert_line_breaks(request.POST.get('title', ''))
            description = convert_line_breaks(request.POST.get('description', ''))
            icon_class = convert_line_breaks(request.POST.get('icon_class', ''))
            
            # Validate lengths
            if len(title) > 100:
                messages.error(request, 'Title must be less than 100 characters')
                return redirect('admin_services')
            
            if len(icon_class) > 100:
                messages.error(request, 'Icon class must be less than 100 characters')
                return redirect('admin_services')
            
            if len(description) > 500:
                messages.error(request, 'Description must be less than 500 characters')
                return redirect('admin_services')
            
            # Insert into Supabase
            response = supabase.table("services").insert({
                "title": title,
                "description": description,
                "icon_class": icon_class
            }).execute()
            
            messages.success(request, 'Service added successfully!')
            
        except Exception as e:
            print(f"Error adding service: {e}")
            messages.error(request, f'Error adding service: {str(e)}')
    
    return redirect('admin_services')

@login_required
def update_service(request, service_id):
    """Update existing service"""
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            icon_class = request.POST.get('icon_class', '').strip()
            
            # Validate lengths
            if len(title) > 100:
                messages.error(request, 'Title must be less than 100 characters')
                return redirect('admin_services')
            
            if len(icon_class) > 100:
                messages.error(request, 'Icon class must be less than 100 characters')
                return redirect('admin_services')
            
            if len(description) > 500:
                messages.error(request, 'Description must be less than 500 characters')
                return redirect('admin_services')
            
            # Update in Supabase
            response = supabase.table("services").update({
                "title": title,
                "description": description,
                "icon_class": icon_class
            }).eq("id", service_id).execute()
            
            messages.success(request, 'Service updated successfully!')
            
        except Exception as e:
            print(f"Error updating service: {e}")
            messages.error(request, f'Error updating service: {str(e)}')
    
    return redirect('admin_services')

@login_required
def delete_service(request, service_id):
    """Delete service"""
    try:
        response = supabase.table("services").delete().eq("id", service_id).execute()
        messages.success(request, 'Service deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting service: {str(e)}')
    
    return redirect('admin_services')

# Projects CRUD Operations
@login_required
def add_project(request):
    """Add new project with image upload"""
    if request.method == 'POST':
        try:
            # Initialize Supabase client
            supabase_url = "https://rlcqfmoginbchsidwawr.supabase.co"
            supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsY3FmbW9naW5iY2hzaWR3YXdyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NzYwODMsImV4cCI6MjA3NjI1MjA4M30.Bputt67mmjY3YgOfO9QMSOJcmUtG5HBLEXKWYqCJYOU"
            client = create_client(supabase_url, supabase_key)
            
            # Function to convert line breaks only
            def convert_line_breaks(text):
                if text is None:
                    return ''
                text = text.replace('<br>', '\n')
                text = text.replace('\\n', '\n')
                return text
            
            # Handle project image upload
            project_image_url = ""
            project_img_file = request.FILES.get('project_img_file')
            
            if project_img_file:
                try:
                    # Generate unique file name
                    file_extension = project_img_file.name.split('.')[-1]
                    file_name = f"project_{request.user.id}_{int(time.time())}.{file_extension}"
                    file_path = f"project_images/{file_name}"
                    
                    # Read file data
                    file_data = project_img_file.read()
                    
                    # Upload to Supabase storage
                    response = client.storage.from_('images').upload(
                        path=file_path,
                        file=file_data
                    )
                    
                    # Check if upload was successful
                    if response:
                        # Get public URL
                        public_url_response = client.storage.from_('images').get_public_url(file_path)
                        
                        # Handle different response types
                        if isinstance(public_url_response, str):
                            project_image_url = public_url_response
                        elif hasattr(public_url_response, 'public_url'):
                            project_image_url = public_url_response.public_url
                        elif isinstance(public_url_response, dict) and 'publicUrl' in public_url_response:
                            project_image_url = public_url_response['publicUrl']
                        else:
                            # Construct URL manually as fallback
                            project_image_url = f"{supabase_url}/storage/v1/object/public/images/{file_path}"
                        
                        print(f"Project image uploaded successfully! URL: {project_image_url}")
                    else:
                        print("Project image upload response was empty")
                        messages.error(request, 'Project image upload failed: Empty response from storage')
                        return redirect('admin_projects')
                        
                except Exception as upload_error:
                    print(f"Project image upload error: {upload_error}")
                    messages.error(request, f'Error uploading project image: {str(upload_error)}')
                    return redirect('admin_projects')
            
            # Process technologies
            technologies = request.POST.get('technologies', '')
            if technologies:
                technologies = [tech.strip() for tech in technologies.split(',')]
            
            project_data = {
                "title": convert_line_breaks(request.POST.get('title')),
                "full_description": convert_line_breaks(request.POST.get('full_description')),
                "technologies": technologies,
                "project_url": convert_line_breaks(request.POST.get('project_url')) or None,
                "github_url": convert_line_breaks(request.POST.get('github_url')) or None,
                "video_url": convert_line_breaks(request.POST.get('video_url')) or None
            }
            
            # Use uploaded image URL if available, otherwise use URL field
            if project_image_url:
                project_data["image_url"] = project_image_url
            else:
                project_data["image_url"] = convert_line_breaks(request.POST.get('image_url'))
            
            # Remove None values
            project_data = {k: v for k, v in project_data.items() if v is not None}
            
            response = supabase.table("projects").insert(project_data).execute()
            messages.success(request, 'Project added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding project: {str(e)}')
    
    return redirect('admin_projects')

@login_required
def update_project(request, project_id):
    """Update project with image upload"""
    if request.method == 'POST':
        try:
            # Initialize Supabase client
            supabase_url = "https://rlcqfmoginbchsidwawr.supabase.co"
            supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJsY3FmbW9naW5iY2hzaWR3YXdyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2NzYwODMsImV4cCI6MjA3NjI1MjA4M30.Bputt67mmjY3YgOfO9QMSOJcmUtG5HBLEXKWYqCJYOU"
            client = create_client(supabase_url, supabase_key)
            
            # Function to convert line breaks only
            def convert_line_breaks(text):
                if text is None:
                    return ''
                text = text.replace('<br>', '\n')
                text = text.replace('\\n', '\n')
                return text
            
            # Handle project image upload
            project_image_url = ""
            project_img_file = request.FILES.get('project_img_file')
            
            if project_img_file:
                try:
                    # Generate unique file name
                    file_extension = project_img_file.name.split('.')[-1]
                    file_name = f"project_{request.user.id}_{int(time.time())}.{file_extension}"
                    file_path = f"project_images/{file_name}"
                    
                    # Read file data
                    file_data = project_img_file.read()
                    
                    # Upload to Supabase storage
                    response = client.storage.from_('images').upload(
                        path=file_path,
                        file=file_data
                    )
                    
                    # Check if upload was successful
                    if response:
                        # Get public URL
                        public_url_response = client.storage.from_('images').get_public_url(file_path)
                        
                        # Handle different response types
                        if isinstance(public_url_response, str):
                            project_image_url = public_url_response
                        elif hasattr(public_url_response, 'public_url'):
                            project_image_url = public_url_response.public_url
                        elif isinstance(public_url_response, dict) and 'publicUrl' in public_url_response:
                            project_image_url = public_url_response['publicUrl']
                        else:
                            # Construct URL manually as fallback
                            project_image_url = f"{supabase_url}/storage/v1/object/public/images/{file_path}"
                        
                        print(f"Project image uploaded successfully! URL: {project_image_url}")
                    else:
                        print("Project image upload response was empty")
                        messages.error(request, 'Project image upload failed: Empty response from storage')
                        return redirect('admin_projects')
                        
                except Exception as upload_error:
                    print(f"Project image upload error: {upload_error}")
                    messages.error(request, f'Error uploading project image: {str(upload_error)}')
                    return redirect('admin_projects')
            
            # Process technologies
            technologies_text = request.POST.get('technologies', '')
            technologies = [tech.strip() for tech in technologies_text.split(',') if tech.strip()]
            
            update_data = {
                "title": convert_line_breaks(request.POST.get('title')),
                "full_description": convert_line_breaks(request.POST.get('full_description')),
                "technologies": technologies,
            }
            
            # Use uploaded image URL if available, otherwise use URL field
            if project_image_url:
                update_data["image_url"] = project_image_url
            else:
                update_data["image_url"] = convert_line_breaks(request.POST.get('image_url'))
            
            # Handle optional links - set to None if empty
            optional_fields = ['project_url', 'github_url', 'video_url']
            for field in optional_fields:
                value = convert_line_breaks(request.POST.get(field, ''))
                update_data[field] = value if value else None
            
            response = supabase.table("projects").update(update_data).eq("id", project_id).execute()
            messages.success(request, 'Project updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating project: {str(e)}')
    
    return redirect('admin_projects')

@login_required
def delete_project(request, project_id):
    """Delete project"""
    try:
        response = supabase.table("projects").delete().eq("id", project_id).execute()
        messages.success(request, 'Project deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting project: {str(e)}')
    
    return redirect('admin_projects')

# Skills CRUD Operations
@login_required
def add_skill(request):
    """Add new skill"""
    if request.method == 'POST':
        try:
            # Function to convert line breaks only
            def convert_line_breaks(text):
                if text is None:
                    return ''
                text = text.replace('<br>', '\n')
                text = text.replace('\\n', '\n')
                return text
            
            response = supabase.table("skills").insert({
                "title": convert_line_breaks(request.POST.get('title')),
                "percentage": request.POST.get('percentage'),
                "skill_type": convert_line_breaks(request.POST.get('skill_type')),
                "icon_class": convert_line_breaks(request.POST.get('icon_class'))
            }).execute()
            
            messages.success(request, 'Skill added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding skill: {str(e)}')
    
    return redirect('admin_skills')

@login_required
def update_skill(request, skill_id):
    """Update skill"""
    if request.method == 'POST':
        try:
            # Function to convert line breaks only
            def convert_line_breaks(text):
                if text is None:
                    return ''
                text = text.replace('<br>', '\n')
                text = text.replace('\\n', '\n')
                return text
            
            update_data = {
                "title": convert_line_breaks(request.POST.get('title')),
                "percentage": request.POST.get('percentage'),
                "skill_type": convert_line_breaks(request.POST.get('skill_type')),
                "icon_class": convert_line_breaks(request.POST.get('icon_class'))
            }
            
            # Remove None values
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            response = supabase.table("skills").update(update_data).eq("id", skill_id).execute()
            messages.success(request, 'Skill updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating skill: {str(e)}')
    
    return redirect('admin_skills')

@login_required
def delete_skill(request, skill_id):
    """Delete skill"""
    try:
        response = supabase.table("skills").delete().eq("id", skill_id).execute()
        messages.success(request, 'Skill deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting skill: {str(e)}')
    
    return redirect('admin_skills')

# Contact Information CRUD
@login_required
def update_contact(request):
    """Update contact information with social media"""
    if request.method == 'POST':
        try:
            # Check if contact info exists
            existing_response = supabase.table("contact_info").select("*").execute()
            
            update_data = {
                "phone": request.POST.get('phone'),
                "email": request.POST.get('email'),
                "address": request.POST.get('address'),
                "linkedin_url": request.POST.get('linkedin_url'),
                "facebook_url": request.POST.get('facebook_url'),
                "instagram_url": request.POST.get('instagram_url'),
                "skype_url": request.POST.get('skype_url'),
                # ADD NEW FIELDS HERE
                "whatsapp_url": request.POST.get('whatsapp_url'),
                "twitter_url": request.POST.get('twitter_url'),
                "freelancer_url": request.POST.get('freelancer_url'),
                "fiverr_url": request.POST.get('fiverr_url'),
                "upwork_url": request.POST.get('upwork_url')
            }
            
            # Remove None values to avoid overwriting with null
            update_data = {k: v for k, v in update_data.items() if v is not None}
            
            print("Updating contact with data:", update_data)  # Debug print
            
            if existing_response.data:
                # Update existing
                response = supabase.table("contact_info").update(update_data).eq("id", existing_response.data[0]['id']).execute()
            else:
                # Create new
                response = supabase.table("contact_info").insert(update_data).execute()
            
            print("Supabase response:", response)  # Debug print
            
            messages.success(request, 'Contact information updated successfully!')
        except Exception as e:
            print("Error updating contact:", str(e))  # Debug print
            messages.error(request, f'Error updating contact information: {str(e)}')
    
    return redirect('admin_contact')

# Contact form submission handler
def submit_contact_form(request):
    """Handle contact form submissions"""
    if request.method == 'POST':
        try:
            print("Form data received:")
            print("Name:", request.POST.get('name'))
            print("Email:", request.POST.get('email'))
            print("Message:", request.POST.get('message'))
            
            response = supabase.table("contact_submissions").insert({
                "name": request.POST.get('name'),
                "email": request.POST.get('email'),
                "message": request.POST.get('message')
            }).execute()
            
            print("Supabase response:", response)
            
            return JsonResponse({'success': True, 'message': 'Thank you for your message! I will get back to you soon.'})
        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({'success': False, 'message': f'Error submitting form: {str(e)}'}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

# Delete contact submission
@login_required
def delete_submission(request, submission_id):
    """Delete contact submission"""
    try:
        response = supabase.table("contact_submissions").delete().eq("id", submission_id).execute()
        messages.success(request, 'Submission deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting submission: {str(e)}')
    
    return redirect('admin_submissions')

# ============================================================================
# ADDITIONAL FUNCTIONALITY
# ============================================================================

# Project detail view
def project_detail(request, project_id):
    """Display detailed project view"""
    try:
        # Get project details
        project_response = supabase.table("projects").select("*").eq("id", project_id).execute()
        
        if not project_response.data:
            messages.error(request, 'Project not found!')
            return redirect('portfolio_home')
        
        project = project_response.data[0]
        
        # Get project images
        images_response = supabase.table("project_images").select("*").eq("project_id", project_id).order("image_order").execute()
        project_images = images_response.data if images_response.data else []
        
        context = {
            'project': project,
            'project_images': project_images,
            'logged_in': request.session.get('logged_in', False)
        }
        return render(request, 'portfolio/project_detail.html', context)
        
    except Exception as e:
        print(f"Error loading project: {e}")
        messages.error(request, 'Error loading project details!')
        return redirect('portfolio_home')

# API Endpoints
def api_portfolio_data(request):
    """API endpoint to get all portfolio data"""
    try:
        settings_response = supabase.table("portfolio_settings").select("*").execute()
        about_response = supabase.table("about_section").select("*").execute()
        services_response = supabase.table("services").select("*").execute()
        projects_response = supabase.table("projects").select("*").execute()
        
        data = {
            'settings': settings_response.data[0] if settings_response.data else {},
            'about': about_response.data[0] if about_response.data else {},
            'services': services_response.data,
            'projects': projects_response.data
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)