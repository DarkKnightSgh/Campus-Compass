from django.db import models
from taggit.managers import TaggableManager
from branch.models import Branch
from django.contrib.auth.models import User
from django.db.models import Q

class ResourceQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains=query) |
                Q(user__username__icontains=query) |
                 Q(branch__branch_name__icontains=query) |
                Q(tags__name__icontains=query)
            )
            qs = qs.filter(or_lookup).distinct().only(
                'id', 'user__username', 'title', 'files', 'uploaded_at', 'branch__branch_name', 'tags__name'
            )  # Add more fields as needed
        return qs


class Resource(models.Model):
    # pk
    id = models.AutoField(primary_key=True,auto_created=True)
    user=  models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=255)
    files = models.FileField(upload_to='resource/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    branch = models.ManyToManyField(Branch, related_name='branch')
    tags = TaggableManager()
    objects = ResourceQuerySet.as_manager()

    def __str__(self):
        return self.title
    def get_model_name(self):
        return 'Resource'