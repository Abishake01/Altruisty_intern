from django.db import models

# Create your models here.

class user_detail(models.Model):
    profile_photo = models.BinaryField(null=True, blank=True)
    user_id = models.CharField(max_length=20,null=True,blank=True)
    name = models.CharField(max_length=90,null=True,blank=True)
    bio = models.CharField(max_length=150,null=True,blank=True)

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'User_profile'

class post_details(models.Model):
    post_id = models.CharField(max_length=60,null=True,blank=True)
    posted_by = models.CharField(max_length=20,null=True,blank=True)
    media = models.BinaryField( null=True, blank=True)
    caption = models.CharField(max_length=450,null=True,blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.post_id

    class Meta:
        db_table = 'Post_details'


class follower(models.Model):
    from_id = models.CharField(max_length=20,null=True,blank=True)
    to_id = models.CharField(max_length=20,null=True,blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.from_id

    class Meta:
        db_table = 'followers_details'


class create_community(models.Model):
    community_id = models.CharField(max_length=10, null=True, blank=True)
    community_name = models.CharField(max_length=30)
    community_image = models.BinaryField(null=True, blank=True)
    creator_id = models.CharField(max_length=15,null=True, blank=True)
    creator_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.community_name

    class Meta:
        db_table = 'Create_community'

class user_community(models.Model):
    user_id = models.CharField(max_length=20, null=True, blank=True)
    community_id = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, null=True, blank=True , default='follower')
    
    

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'User_community'

class chat_communitydata(models.Model):
    message_id = models.CharField(max_length=20, null=True, blank=True)
    user_id = models.CharField(max_length=20, null=True, blank=True)
    community_id = models.CharField(max_length=20, null=True, blank=True)
    content_type = models.CharField(max_length=20)
    messagecontent = models.CharField(max_length=40)
    sent_date = models.DateTimeField(auto_now_add=True)


    
    

    def __str__(self):
        return self.message_id

    class Meta:
        db_table = 'chat_communitydata'

class community_chat_data(models.Model):
    message_id = models.CharField(max_length=90, null=True, blank=True)
    user_id = models.CharField(max_length=20, null=True, blank=True)
    community_id = models.CharField(max_length=20, null=True, blank=True)
    content_type = models.CharField(max_length=20)
    messagecontent = models.CharField(max_length=40)
    media_content = models.BinaryField(null=True, blank=True)
    media_caption = models.CharField(max_length=250,null=True, blank=True)
    sent_date = models.DateTimeField(auto_now_add=True)
    editted = models.CharField(max_length=15,null=True, blank=True)


    
    

    def __str__(self):
        return self.message_id

    class Meta:
        db_table = 'chat_community_data'