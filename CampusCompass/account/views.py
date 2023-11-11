from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib import messages
from django.utils import timezone

# models
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from branch.models import Department, Branch
from .models import Student, Mentor
from taggit.managers import TaggableManager
from taggit.models import Tag

# decorators
from django.contrib.auth.decorators import login_required

# authentication
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from account.tokens import account_activation_token
from django.core.mail import send_mail  
from django.contrib.auth.models import User
# from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import View




# Create your views here.

def register(request):
    department= Department.objects.all()
    context={'department':department}
    return render(request, 'account/register.html',context)


def register_submit(request):
    context={}
    if request.method=='POST':
        firstname = request.POST.get('firstname',False)
        lastname = request.POST.get('lastname',False)
        country_code= request.POST.get('countrycode',False)
        whatsappnumber = request.POST.get('phone',False)
        email = request.POST.get('email',False)
        username = request.POST.get('username',False)
        password1 = request.POST.get('password1',False)
        password2 = request.POST.get('password2',False)
        college_email = request.POST.get('collegemail',False)
        SRN = request.POST.get('SRN',False) # student id
        year_of_passing_out = request.POST.get('yearofpassingout',False)
        branch = request.POST.get('branch',False)
        department = request.POST.get('department',False)

        whatsappno =country_code+" "+whatsappnumber

        # trim + from country code if any
        if (country_code[0] == "+"):
            country_code = country_code[1:]
        
        whatsappnumber=country_code+whatsappnumber
        

        whatsapplink="https://api.whatsapp.com/send?phone="+whatsappnumber

        if password1 == password2:
            if User.objects.filter(username= username).exists():
                messages.info (request, "Username taken")
                return redirect('/account/register')
            elif (User.objects.filter(email = email).exists()):
                messages.info (request, "Email already present")
                return redirect('/account/register')
            elif (Student.objects.filter(college_email=college_email).exists()):
                messages.info (request, "Account already present")
                return redirect('/account/register')
            else:
                user = User.objects.create_user(first_name= firstname, last_name= lastname ,username= username, password= password1, email= email)
                user.save()

                student= Student()
                student.user=User.objects.get(username=username)
                student.department= Department.objects.get(department_id= department)
                student.branch= Branch.objects.get(branch_code= branch)

                data=("",whatsappno,whatsapplink,SRN,college_email,year_of_passing_out)                
                student.bio,student.whatsapp_number,student.whatsapp_link,student.student_id,student.college_email,student.year_of_passing_out=data

                student.save()
                auth.login(request, user)

                
                messages.success(request, 'Verify Your Account now!!')
                return redirect ('/account/login')
        else:
            messages.danger (request, "password does not match")
            return redirect('/account/register')
    
    return redirect ('/account/register')

    



def login(request):
    context={}
    return render(request, 'account/login.html',context)


def login_submit(request):
    context={}
    if request.method == 'POST':        
        username = request.POST.get('username',False)
        password = request.POST.get('password',False)
        
        user = auth.authenticate(username=username, password= password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in successfully')
            return redirect('/account/profile')
        else:
            messages.error(request, 'invalid username or password')

            return redirect ('/account/login')
    else:
        pass

def logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out")
    return redirect('/')



def confirm_email(request):
    user=request.user
    current_site = get_current_site(request)
    subject = 'Activate Your Campus Compass Account'
    print(user)
    message = render_to_string('account/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
    user.email_user(subject, message)

    messages.success(request, ('Your email confirmation is pending! Verify now'))
    return redirect('/')


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            # uid = force_text(urlsafe_base64_decode(uidb64))
            uid=str(urlsafe_base64_decode(uidb64), 'utf-8')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.student.email_confirmed = True
            student=Student.objects.get(user=user)
            student.email_confirmed=True
            student.save()
            user.save()
            auth.login(request, user)
            messages.success(request, ('Your email has been confirmed.'))
            return redirect('/')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('/')



def profile(request):
    username= request.user
    if(username.__str__() != 'AnonymousUser'):
        user= User.objects.get(username=username)
        student = Student.objects.get(user=user)
        SRN= student.student_id
        # mentor = Mentor.objects.get(student_id=SRN)
        # check if mentor
        mentor=None
        if(student.is_mentor):
            mentor=Mentor.objects.get(username=username)
        
        context ={
            'user':user,
            'student':student,
            'mentor':mentor,
        }

        return render(request, 'account/profile.html',context)
    else:
        messages.error(request,"Please sign in first")
        return redirect('/account/login')

def edit_profile(request):
    username= request.user
    if(username.__str__() != 'AnonymousUser'):
        department=Department.objects.all()
        user= User.objects.get(username=username)
        student= Student.objects.get(user=user)
        branch=Branch.objects.filter(department=student.department)

        # print(branch)
        # print(student.branch.branch_code)
        context ={'department':department,'user':user,'student':student,'branch':branch}
        return render(request, 'account/editprofile.html',context)
    else:
        messages.error(request,"Please sign in first")
        return redirect('/account/login')

def edit_profile_submit(request):
    if request.method == 'POST':        
        username = request.user.__str__()
        first_name = request.POST.get('firstname',False)
        last_name = request.POST.get('lastname',False)
        bio=request.POST.get('bio',False)
        show_number= request.POST.get('show_number',False)
        country_code= request.POST.get('countrycode',False)
        whatsappnumber = request.POST.get('phone',False)
        email = request.POST.get('email',False)

        branch = request.POST.get('branch',False)
        department = request.POST.get('department',False)

        whatsappno =country_code+" "+whatsappnumber

        # trim + from country code if any
        if (country_code[0] == "+"):
            country_code = country_code[1:]
        
        whatsappnumber=country_code+whatsappnumber
        
        # generate whatsapp link
        whatsapplink="https://api.whatsapp.com/send?phone="+whatsappnumber

        if(show_number):
            show_number=True
        else:
            show_number=False

        # find user and update
        user = User.objects.get(username=username)
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.save()

        # find student and update
        student= Student.objects.get(user=user)
        student.department= Department.objects.get(department_id= department)
        student.bio=bio
        student.show_number= show_number
        student.branch= Branch.objects.get(branch_code= branch)
        student.whatsapp_number= whatsappno
        student.whatsapp_link=whatsapplink
        student.save()  

        messages.success(request,"Profile Updated")
        return redirect('/account/profile')     
        
    else:
        pass




def can_apply_again(mentor):
    six_months_ago = timezone.now() - timezone.timedelta(days=180)  # 6 months = 180 days
    if mentor.last_application_date < six_months_ago:
        # get mentor
        mentor = Mentor.objects.filter(user=mentor).first()
        mentor.last_application_date = None
        mentor.save()


def mentor_registration(request):
    username=request.user.__str__()
    if(username=="AnonymousUser"):
        messages.error(request,"Please sign in first")
        return redirect("/account/login" )
    if request.method == "POST":

        print(request.FILES)
        
        if  'fileupload' in request.FILES:
            resume = request.FILES['fileupload']
            domains_input = request.POST.get("domains")
            domain_list = domains_input.split(",")  # Assuming domains are comma-
            
            user=User.objects.get(username=username)
            student = Student.objects.get(user=user)
            if (Mentor.objects.filter(username=username).exists()):
                mentor=Mentor.objects.get(username=username)
            else:
                mentor = Mentor()
            
            mentor.student=student
            mentor.username=username
            mentor.approved=0
            mentor.resume = resume
            mentor.description = request.POST.get("description")
            mentor.last_application_date= timezone.now()
            mentor.save()
            # mentor.domain.add(*domain_list)

            for domain_name in domain_list:
                # strip domain of spaces and make it in lower case only
                domain_name = domain_name.strip().lower()
                domain, created = Tag.objects.get_or_create(name=domain_name)
                mentor.domain.add(domain)

            messages.success(request,"Role for mentor successfully applied!, We will get back to you in 1 week")
            return redirect('/account/profile')  # Redirect to a success page or any desired location
        
        else:
            messages.error(request,"Add your resume first!")
            return redirect('/account/mentor_registration')
        
    context={}
    if Mentor.objects.filter(username=username).exists():
        mentor=Mentor.objects.get(username=username)
        can_apply_again(mentor)
        context['mentor']=mentor
    return render(request, 'account/mentor_registration.html',context)  # Render the form again if it's a GET request


def show_mentor(request):
    # get all mentors of branch
    username= request.user.__str__()
    # get Student
    user=User.objects.get(username=username)
    student=Student.objects.get(user=user)
    # Branch
    branch=Branch.objects.get(branch_code=student.branch.branch_code)
    mentors=Mentor.objects.filter(student__branch__branch_code=branch.branch_code,approved=True)    
    print(mentors[0].student.user.username)
    context={'mentors':mentors}
    return render(request, 'account/show_mentor.html',context)

def show_mentors_by_domain(request,domain):
    # get all mentors of branch
    username= request.user.__str__()
    # get Student
    user=User.objects.get(username=username)
    student=Student.objects.get(user=user)
    # Branch
    mentors=Mentor.objects.filter(approved=True,domain__slug=domain)    
    print(mentors[0].student.user.username)
    context={'mentors':mentors}
    return render(request, 'account/show_mentor.html',context)

@club_head_required
def approve_membership(request):
    if request.method == 'POST':
        srn = request.POST.get('srn',False)
        social_media_manager = request.POST.get('social_media_manager',False)
        username = request.user.__str__()
        club = which_club_head(username)
        club_head = User.objects.get(username=username)
        print(club)
        club = Club.objects.get(club_name=club)
        if (Student.objects.filter(student_id=srn).exists()):
            s = Student.objects.get(student_id=srn)
            print(s.user)
            if(ClubMember.objects.filter(user=s.user,club=club).exists()):
                c=ClubMember.objects.get(user=s.user,club=club)
            else:
                c=ClubMember()
            c.user= s.user
            c.club=club
            if(social_media_manager):
                c.social_media_manager=True
            c.save()
            return redirect('/account/profile')
        else:
            messages.error("Student not present in our system")
            return redirect('/account/approve_membership')

        
    context = {}
    return render(request, 'account/approve_membership.html', context)
