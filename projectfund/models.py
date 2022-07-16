from django.db import models
from account.models import Account


Choice = [
    ('hospital','hospital'),
    ('Michael','Michael'),
    ('education','education'),
    ('Corona','Corona'),
    ('hayaat karima','hayaat karima'),
]


class Project(models.Model):
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    details = models.TextField(max_length=300)
    category = models.CharField(max_length=20, choices=Choice)
    total_target = models.CharField(max_length=20)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    donations = models.CharField(max_length=20, default=0)
    is_admin = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-start_date",)


class ProjectImage(models.Model):
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project')

    def __str__(self):
        return format(self.project_name.title)


class ProjectTag(models.Model):
    project_name_tag = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20)

    def __str__(self):
        return format(self.project_name_tag.title)
class Comment(models.Model):
    proj = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

RATING_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
class Rate(models.Model):
    ratee = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='rates',null=True)
    rating = models.CharField(max_length=20,choices=RATING_CHOICES)
    active = models.BooleanField(default=False)

