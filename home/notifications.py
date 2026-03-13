from django.urls import reverse
from accounts.models import TTUser, JobSeeker, Recruiter
from applications.models import Application
from posting.models import Post, Query
from .models import Notification
from .distance import longlatdistance

#Note when making HTML message, pass formatted VIEW_URL into href of the <a>
def notify(user: TTUser, message: str, link: str, image: str = ""):
    notification = Notification()
    notification.recipient = user
    notification.message = "Notification Failed"
    notification.viewslink = link
    notification.image = image
    notification.save() #To get an id for reverse search
    notification.message = message.replace('VIEW_URL', reverse('home.notification_click', kwargs={'id': notification.id}))
    notification.save()

#Sends one Job Seeker info about multiple job postings
def update_seeker_notifications(user: TTUser):
    if not user.is_seeker: return
    seeker = JobSeeker.objects.get(user=user)
    if not seeker.skills: return
    seekerSkills = seeker.skills.all()
    postingPool = Post.objects.all()
    for post in postingPool:
        if Application.objects.filter(applicant=user, posting=post): continue
        if len(post.skills.all()) == 0: continue
        link = reverse('posting.post', kwargs={'id': post.id})
        try:
            Notification.objects.get(recipient=user, viewslink=link)
            continue
        except:
            if not calculate_fit(seekerSkills, post.skills.all(), 0.1): continue
            notify(user, f'''Based on your profile, we recommend that you apply for the {post.job_title} position at {post.company_name}. <a href="VIEW_URL">Click here</a> to view details.''', link, post.image)
    queryPool = Query.objects.all()
    link = reverse('accounts.profiles', kwargs={'user_link': str(user)})
    for query in queryPool:
        try:
            Notification.objects.get(recipient=query.recruiter.user, viewslink=link)
            continue
        except:
            if not matches_query(seeker, query): continue
            notify(query.recruiter.user, f'''Based on a search query you saved, <a href="VIEW_URL">{user.first_name} {user.last_name}</a> is a viable candidate.''', link, user.pfp)


def update_recruiter_notifications(user: TTUser):
    #Recommend job seekers to hire
    if not user.is_recruiter: return
    recruiter = Recruiter.objects.get(user=user)
    posts = Post.objects.filter(recruiter=recruiter)
    queries = Query.objects.filter(recruiter=recruiter)
    seekerPool = JobSeeker.objects.all()
    for seeker in seekerPool:
        link = reverse('accounts.profiles', kwargs={'user_link': str(seeker)})
        try:
            Notification.objects.get(recipient=user, viewslink=link)
            continue
        except:
            query_notified = False
            for query in queries:
                if not matches_query(seeker, query): continue
                notify(user, f'''Based on a search query you saved, <a href="VIEW_URL">{seeker.user.first_name} {seeker.user.last_name}</a> is a viable candidate.''', link, seeker.user.pfp)
                query_notified = True
                break
            #Make sure somehow that you don't send a notification from the same user multiple times
            if query_notified: continue
            if len(seeker.skills.all()) == 0: continue
            for post in posts:
                if Application.objects.filter(applicant=seeker.user, posting=post): continue
                if not post.skills: continue
                postingSkills = post.skills.all()
                if not calculate_fit(seeker.skills.all(), postingSkills, 0.1): continue
                notify(user, f'''Based on your job posting, <a href="VIEW_URL">{seeker.user.first_name} {seeker.user.last_name}</a> is a good fit for the {post.job_title} position.''', link, seeker.user.pfp)
                break



def update_unsupported_user_notifications(user: TTUser):
    #Remove all existing notifications and tell user to onboard
    existing_notis = Notification.objects.filter(recipient=user)
    for noti in existing_notis:
        noti.delete()
    notify(user, f'''You haven't unlocked all features of Talent Trek. <a href="VIEW_URL">Click here</a> to finish setting up your account.''', reverse('accounts.onboard'))

def update_onboarded_user_notifications(user: TTUser):
    notiToDelete = Notification.objects.get(recipient=user, viewslink=reverse('accounts.onboard'))
    notiToDelete.delete()

#Sends multiple Job Seekers notifications about a single posting
def update_post_notifications(post: Post):
    if not post.skills: return
    postingSkills = post.skills.all()
    link = reverse('posting.post', kwargs={'id': post.id})
    seekerPool = JobSeeker.objects.all()
    for seeker in seekerPool:
        if Application.objects.filter(applicant=seeker.user, posting=post): continue
        if len(seeker.skills.all()) == 0: continue
        try:
            Notification.objects.get(recipient=seeker.user, viewslink=link)
            continue
        except:
        # Won't check to notify if already applied or doesn't have any skills added
            if not calculate_fit(seeker.skills.all(), postingSkills, 0.5): continue
            notify(seeker.user, f'''Based on your profile, we recommend that you apply for the {post.job_title} position at {post.company_name}. <a href="VIEW_URL">Click here</a> to view details.''', link, post.image)
            notify(post.recruiter.user, f'''Based on your job posting, <a href="VIEW_URL">{seeker.user.first_name} {seeker.user.last_name}</a> is a good fit for the {post.job_title} position.''', reverse('accounts.profiles', kwargs={'user_link': str(seeker.user)}), seeker.user.pfp)
    
def calculate_fit(seekerSkills, postingSkills, threshold):
    seekerList = []
    for skill in seekerSkills:
        seekerList.append(skill.name)
    matches = 0
    uniqueSkills = len(seekerList)
    for skill in postingSkills:
        if skill.name in seekerList: matches += 1
        else: uniqueSkills += 1
    return threshold <= (matches / uniqueSkills)

def matches_query(seeker: JobSeeker, query: Query):
    for skill in query.skills.all():
        if skill not in seeker.skills.all(): return False
    if not seeker.user.location: return False
    #print(f"Distance: {longlatdistance(seeker.user, query.recruiter.user)}")
    return longlatdistance(seeker.user, query.recruiter.user) <= query.distance
    