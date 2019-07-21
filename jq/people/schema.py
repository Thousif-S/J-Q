from graphene_file_upload.scalars import Upload
import graphene
from graphene_django import DjangoObjectType
from .models import Profile
from users.schema import UserType
from django.db.models import Q


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class Query(graphene.ObjectType):
    profiles = graphene.List(ProfileType, search=graphene.String())

    def resolve_profiles(self, info, search=None, **kwargs):
        pqs = Profile.objects.all()
        if search:
            filter = (
                Q(first_name__icontains=search) | Q(last_name__icontains=search) |
                Q(username__icontains=search) | Q(nick_name__icontains=search)
            )
            pqs = pqs.filter(filter)

        return pqs


class CreateProfile(graphene.Mutation):
    id = graphene.Int()
    user = graphene.Field(UserType)
    first_name = graphene.String()
    last_name = graphene.String()
    nick_name = graphene.String()
    gender = graphene.String()
    short_bio = graphene.String()
    portfolio = graphene.String()

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        nick_name = graphene.String()
        gender = graphene.String()
        short_bio = graphene.String()
        portfolio = graphene.String()

    def mutate(self, info, **kwargs):
        user = info.context.user or None
        profile = Profile(**kwargs, user=user)
        profile.save()

        return CreateProfile(
            id=profile.id,
            user=Profile.user,
            first_name=Profile.first_name,
            last_name=Profile.last_name,
            nick_name=Profile.nick_name,
            gender=Profile.gender,
            short_bio=Profile.short_bio,
            portfolio=Profile.portfolio,
        )


class Mutation(graphene.ObjectType):
    create_profile = CreateProfile.Field()
