from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship


"""
    Aqui temos a criação automática de Perfil com base no USER do Django.
    No 'post_save', criamos o perfil com base na instancia do usuário que se encontra no USER
"""
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


"""
    Criação do relacionamento entre os usuários com a amizade.
    Um perfil envia o pedido de amizade para outro. Quando o status muda para 'accepted',
    os perfis começam um relacionamento de amizade entre si.
        print('sender: ', sender_)
        print('receiver: ', receiver_)
            Acima, temos o exemplo sender: Diego, receiver: testeuser2
"""
@receiver(post_save, sender=Relationship)
def post_save_add_to_friend(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver

    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()

# Deletar ambos os relacionamentos entre os usuários
@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_friend(sender, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver

    sender_.friends.remove(receiver_.user)
    receiver_.friends.remove(sender_.user)

    sender_.save()
    receiver_.save()