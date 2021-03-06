from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.shortcuts import reverse, redirect
from django.db.models.signals import pre_save, post_save
from ckeditor.fields  import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

#sending email sections
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import threading
from random import choices
from string import ascii_lowercase, digits

            

course_level = [("Débutant", "Débutant"), ("Intermédiaire","Intermédiaire")]
course_status = [("Publier", "publier"), ("Corbeille","corbeille")]
types = [("Course", "cours"), ("Tutoriels","tutoriels")]

class Level(models.Model):
    level = models.CharField(choices=course_level, max_length=13)
    description = models.TextField(default="ceci est un niveau")

    def __str__(self):
        return self.level

class Course(models.Model):
    title = models.CharField(max_length=225)
    level = models.ForeignKey(to=Level, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=course_status, max_length=13, default="Corbeille")
    type = models.CharField(choices=types, max_length=13, default="Course")
    slug = models.SlugField(blank=True, unique=True)
    body = RichTextUploadingField(verbose_name='content')
    intro = RichTextUploadingField(blank=1, null=1, config_name="extrait")
    img_link = models.URLField(blank=True, null=True)
    notify_users = models.BooleanField(default=False)
    notify_time = models.DateTimeField(blank=True, null=True, auto_now_add=False)
    

    def get_absolute_url(self):
        return reverse('coursedetail', kwargs={"slug":self.slug})

    def alls(self,*args, **kwargs):
        return self.all()

    def __str__(self):
        return self.title

    

class Base_info(models.Model):
    name  = models.CharField(max_length=155)
    email = models.EmailField()
    class Meta:
        abstract = True


class Contact(Base_info):
    message = models.TextField()


class Subscribe(Base_info):
    pass

class Commentaire(models.Model):
    comments = models.TextField(verbose_name="Laisser un commentaire")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    at = models.DateTimeField(auto_now_add=True)
    to = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    id_pk = models.CharField(max_length=8, blank=1, null=True)

    def __str__(self):
        return "commentaire de "+self.author.username

    class Meta:
         ordering =["-at"]

class ReplayToComment(models.Model):
    replay_content = models.TextField(verbose_name="")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    at = models.DateTimeField(auto_now_add=True)
    to = models.ForeignKey(to=Commentaire, on_delete=models.CASCADE, verbose_name="commentaire", related_name="replays")
    id_pk = models.CharField(max_length=8, blank=1, null=True)

    def __str__(self):
        return self.replay_content


class Send_Async_Mail(threading.Thread):
	def __init__(self,email_message, *args, **kwargs):
		super().__init__()
		self.to_send  = email_message


	def run(self):
		self.to_send.content_subtype = "html"
		self.to_send.send()



def slugifyTitle(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(slugifyTitle, Course)



def add_id(sender, instance, *args, **kwargs):
    if not instance.id_pk or len(instance.id_pk) != 8:

        instance.id_pk = "oc"+"".join([value for value in choices(ascii_lowercase+digits, k=6)])
        instance.save()

post_save.connect(add_id, sender=Commentaire)
post_save.connect(add_id, sender=ReplayToComment)

def AfterPostSaving(sender , instance , created , *args, **kwargs):
	if created:
		#get all subuscriber
		reception_list = [sub.email for sub in Subscribe.objects.all()]
		#get all usecrs email
		reception_list += [users.email for users in User.objects.all()]
		#delete all mail duplication
		reception_list = list(set(reception_list))
		#send mail
		context = {
		"currentCourse":instance,
		}

		email = render_to_string("up-posting/emails/notify.html", context)
		subject = f"{instance.title} | Python {instance.type}"

		for mail in reception_list:
			email_message = EmailMessage(subject, email, to=[mail,])
			Send_Async_Mail(email_message).start()
		instance.notify_time = timezone.now()
		instance.notify_users = True



post_save.connect(AfterPostSaving, sender=Course)
