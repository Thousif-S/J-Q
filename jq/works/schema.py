import graphene
from graphql import GraphQLError
from graphene_django import DjangoObjectType
from django.db.models import Q
from users.schema import UserType
from .models import Job, Quest, Vote


class JobType(DjangoObjectType):
    class Meta:
        model = Job


class QuestType(DjangoObjectType):
    class Meta:
        model = Quest


class VoteType(DjangoObjectType):
    class Meta:
        model = Vote


class Query(graphene.ObjectType):
    jobs = graphene.List(
        JobType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    quests = graphene.List(
        QuestType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    votes = graphene.List(VoteType)

    def resolve_jobs(self, info, search=None, first=None, skip=None, **kwargs):
        jqs = Job.objects.all()
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
            jqs = jqs.filter(filter)

        if skip:
            jqs = jqs[skip:]

        if first:
            jqs = jqs[:first]

        return jqs

    def resolve_quests(self, info, search=None, first=None, skip=None, **kwargs):
        qqs = Quest.objects.all()
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
            qqs = qqs.filter(filter)

        if skip:
            qqs = qqs[skip:]

        if first:
            qqs = qqs[:first]

        return qqs

    def resolve_votes(self, info):
        return Vote.objects.all()


class CreateJob(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    category = graphene.String()
    about_us = graphene.String()
    posted_at = graphene.Int()
    updated_at = graphene.Int()
    posted_by = graphene.Field(UserType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        about_us = graphene.String()
        category = graphene.String()

    def mutate(self, info, **kwargs):
        user = info.context.user or None
        job = Job(**kwargs, posted_by=user)
        job.save()

        return CreateJob(
            id=job.id,
            title=job.title,
            description=job.description,
            about_us=job.about_us,
            category=job.category,
            posted_by=job.posted_by
        )


class CreateQuest(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    category = graphene.String()
    expiring_date = graphene.Int()
    posted_at = graphene.Int()
    updated_at = graphene.Int()
    posted_by = graphene.Field(UserType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        expiring_date = graphene.Int()
        category = graphene.String()

    def mutate(self, info, **kwargs):
        user = info.context.user or None
        quest = Quest(**kwargs, posted_by=user)
        quest.save()

        return CreateQuest(
            id=quest.id,
            title=quest.title,
            description=quest.description,
            expiring_date=quest.expiring_date,
            category=quest.category,
            posted_by=quest.posted_by
        )


class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    quest = graphene.Field(QuestType)

    class Arguments:
        quest_id = graphene.Int()
        # job_id = graphene.Int()

    def mutate(self, info, quest_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError(
                "No nO You must be logged into vote sorry sorry in to vote")
        quest = Quest.objects.filter(id=quest_id).first()
        # job = Job.objects.filter(id=job_id).first()
        if not quest:
            raise Exception("Invalid quest")

        Vote.objects.create(
            user=user,
            quest=quest,
        )

        return CreateVote(user=user, quest=quest)


class Mutation(graphene.ObjectType):
    create_job = CreateJob.Field()
    create_quest = CreateQuest.Field()
    create_vote = CreateVote.Field()
