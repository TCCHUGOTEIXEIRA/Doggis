from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):

    CLIENTE = 1
    ATENDENTE = 2
    VETERINARIO = 3
    ADMIN = 4

    ROLE_CHOICES = (
        (CLIENTE, 'Cliente'),
        (ATENDENTE, 'Atendente'),
        (VETERINARIO, 'Veterinário'),
        (ADMIN, 'Administrador'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)
    picture = models.ImageField(upload_to='images/', default='default.jpg')

    def __str__(self):
        return (self.user.first_name + ' ' + self.user.last_name)

    def name(self):
        if len(self.user.first_name + ' ' + self.user.last_name) > 1:
            return (self.user.first_name + ' ' + self.user.last_name)
        else:
            return self.user.username

    def getRole(self):
        roles = ['Cliente', 'Atendente', 'Veterinário', 'Administrador']
        user_role = roles[self.role-1]
        return user_role

    def isClient(self):
        if self.role is 1:
            return True
        else:
            return False

    def isStaff(self):
        if self.role is 2:
            return True
        else:
            return False

    def isVet(self):
        if self.role is 3:
            return True
        else:
            return False

    def isAdmin(self):
        if self.role is 4:
            return True
        else:
            return False

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
