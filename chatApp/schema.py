import graphene
from graphene_django import DjangoObjectType
from chatApp.models import *


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class ProfileType(DjangoObjectType):
  user=graphene.Field(UserType)
  class Meta:
    model = profile
    fields = "__all__"

class Query(graphene.ObjectType):
  profile_data = graphene.List(ProfileType, username=graphene.String())

  def resolve_profile_data(self, info, username):
    if username:
      return profile.objects.filter(user__username=username)
    return profile.objects.all()

schema = graphene.Schema(query=Query)