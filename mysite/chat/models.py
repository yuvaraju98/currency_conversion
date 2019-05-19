from django.db import models

# Create your models here.

class user_info(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100,null=True)
    online = models.BooleanField(default=0, null=True)

    def __unicode__(self):
        return str(self.name)

    class Meta:
        app_label = 'chat'
        db_table = 'user_logs'
        ordering = ['id']


class chat_table(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.CharField(max_length=100)
    message = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return str(self.sender)

    class Meta:
        app_label = 'chat'
        db_table = 'user_chats'
        ordering = ['id']


