from django.shortcuts import redirect, render
from .models import UrlLead, ImageStorage
from .forms import ImageInputForm, InputLeadForm, CustomSlugInput, ImageInputForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
import pyqrcode
import uuid 
from django.conf import settings
from django.shortcuts import get_object_or_404
# Create your views here.
def qrcode_generator(request,shortened_url_link):
    pyqrcode.create(request.scheme+'://'+get_current_site(request).domain+'/'+shortened_url_link).png('static/url-shortner/30Bits_qrcode.png', scale=5)

def shortner(request):
    context_data = {'user_authenticated_data' : None}
    if request.user.is_authenticated:
        context_data['user_link_count'] = UrlLead.objects.filter(user = request.user).count()
        context_data['created_links'] = UrlLead.objects.filter(user = request.user).order_by('-last_modified')
        context_data['user_authenticated_data'] = request.user
    context_data['sitedomain'] = get_current_site(request).domain
    context_data['protocol_type'] = request.scheme
    if request.method == "POST":
        model = UrlLead.objects.all()
        form = InputLeadForm(data=request.POST)
        if form.is_valid():
            if 'https://'+get_current_site(request).domain in form.cleaned_data.get('input_path') or 'http://'+get_current_site(request).domain in form.cleaned_data.get('input_path') :
                messages.info(request,'{} is already under 30 Bit operation.'.format(form.cleaned_data.get('input_path')))
                return redirect('/')
            input_data = form.cleaned_data.get('input_path')
            if context_data['user_authenticated_data'] and UrlLead.objects.filter(redirect_path = input_data, is_public = False, user = context_data['user_authenticated_data']).exists():
                get_data = UrlLead.objects.get(redirect_path = input_data, is_public = False, user = context_data['user_authenticated_data'])
                return redirect('url-details',slug=get_data.shortened_url)
            elif UrlLead.objects.filter(redirect_path = input_data, is_public = True).exists() == False:
                shortened_url_data = uuid.uuid4().hex[:5] 
                new_data = model.create(redirect_path = input_data, shortened_url = shortened_url_data)
                if request.user.is_authenticated:
                    new_data.user = request.user
                    context_data['created_links'] = UrlLead.objects.filter(user = request.user).order_by('-last_modified')
                    new_data.save()
                    context_data['user_link_count'] = UrlLead.objects.filter(user = request.user).count()
                new_data.save()
            else:
                shortened_url_data = UrlLead.objects.get(redirect_path = input_data,is_public = True ).shortened_url 
                if request.user.is_authenticated:
                    messages.info(request,'This link is already registered, under the given shortened link {}, which you can update to make it distinct.'.format(shortened_url_data))
                    context_data['link_used'] = True
            qrcode_generator(request,shortened_url_data)
            context_data['input_data'] = input_data
            context_data['shortened_url'] = shortened_url_data
            context_data['form'] = InputLeadForm()
            return render(request,'url-shortner/index.html', context_data)

        else:
            messages.info(request,'Something Went Wrong, Try Again!')
            return redirect('/')

    context_data['form'] = InputLeadForm()
    context_data['form2'] = ImageInputForm()
    return render(request,'url-shortner/index.html',context_data)

def redirect_to_shortened(request, slug):
        slug_data = get_object_or_404(UrlLead,shortened_url = slug,is_active = True)
        return redirect(slug_data.redirect_path)

def updateslug(slug_data,input_data,user):
    if UrlLead.objects.filter(shortened_url = input_data).exists() == False:
        if UrlLead.objects.filter(user = user,shortened_url = slug_data.shortened_url).exists():
            get_data =  UrlLead.objects.get(user = user,shortened_url = slug_data.shortened_url)
            get_data.shortened_url = input_data
            get_data.is_public = False
            get_data.save()
            return True
        else:
            UrlLead.objects.create(user= user,redirect_path=slug_data.redirect_path,shortened_url = input_data,is_public = False)
            return True
    else:
        return False          

@login_required()
def url_details(request,slug):
    form = CustomSlugInput(initial={'slug_input': slug})
    slug_data = get_object_or_404(UrlLead,shortened_url = slug)    
    if UrlLead.objects.filter(is_public = True, shortened_url = slug).exists() | UrlLead.objects.filter(user = request.user,shortened_url = slug).exists():
        if request.method == 'POST':
            form = CustomSlugInput(request.POST)
            if form.is_valid():
                input_data = form.cleaned_data.get('slug_input')
                if 'update-button' in request.POST:
                    get_data = updateslug(slug_data,input_data,request.user)
                    if get_data:
                        messages.info(request,'Your Branded link ....../{}  Created Successfully'.format(input_data))
                        return redirect('/')
                    messages.error(request,'..../{} Alreay Exist, Try something unique'.format(input_data))
                
                elif 'delete-button' in request.POST:
                    get_data = UrlLead.objects.get(shortened_url = slug_data.shortened_url, user = request.user)
                    messages.info(request,'Your Branded link ....../{} Deleted Permanently.'.format(slug))
                    get_data.delete()
                    return redirect('/')
                elif 'active_unactive-button' in request.POST:
                    get_data = UrlLead.objects.get(shortened_url = slug_data.shortened_url, user = request.user)
                    if get_data.is_active == True:
                        get_data.is_active = False
                        messages.info(request,'Your Branded link ....../{} Unactivated Now. This link will not work until you activate it.'.format(slug))
                    else:
                        get_data.is_active = True
                        messages.info(request,'Your Branded link ....../{} Activated Successfully.'.format(slug))
                    get_data.save()
                    return redirect('/')
        qrcode_generator(request,slug)      
              
        return render(request, 'url-shortner/index.html',{
            'form' : InputLeadForm(initial={'slug_input': slug}),
            'is_registered' : UrlLead.objects.filter(shortened_url = slug, user = request.user).exists(),
            'slug_data' : slug_data,
            'canvas' : True,
            'user_link_count' : UrlLead.objects.filter(user = request.user).count(),
            'sitedomain' : get_current_site(request).domain,
            'created_links' : UrlLead.objects.filter(user = request.user).order_by('-last_modified'),
            'slug_input' : form,
            'protocol_type': request.scheme,
        })
    messages.info(request,'Something Went Wrong, Unauthorization Access may restricted what you want.')
    return redirect('/')

@login_required()
def image_handler(request):
    if request.method == 'POST':
        form = ImageInputForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data.get('image_data').size < 3206545: #image should be less than 3.058Mb
                obj = ImageStorage.objects.create(user = request.user, image = form.cleaned_data.get('image_data'))
                print()
                obj.save()
                image_url_obj = UrlLead.objects.create(user = request.user, redirect_path = request.scheme+'://'+get_current_site(request).domain+
                settings.MEDIA_URL+obj.image.name, shortened_url = uuid.uuid4().hex[:5], is_public = False)
                image_url_obj.save()
                messages.info(request,'Wonderful, your uploaded image is available at path ....../{}'.format(image_url_obj.shortened_url))
                return redirect('/')
            messages.info(request,'Image Size should be less than 3.058 MB')
    return redirect('/')