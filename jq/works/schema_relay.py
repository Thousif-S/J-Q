import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Job, Quest, Vote


class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['title', 'description']


class JobNode(DjangoObjectType):
    class Meta:
        model = Job
        interfaces = (graphene.relay.Node, )


class QuestFilter(django_filters.FilterSet):
    class Meta:
        model = Quest
        fields = ['title', 'description']


class QuestNode(DjangoObjectType):
    class Meta:
        model = Quest
        interfaces = (graphene.relay.Node, )


class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (graphene.relay.Node, )


class RelayQuery(graphene.ObjectType):
    relay_job = graphene.relay.Node.Field(JobNode)
    relay_jobs = DjangoFilterConnectionField(
        JobNode, filterset_class=JobFilter)

    relay_quest = graphene.relay.Node.Field(QuestNode)
    relay_quests = DjangoFilterConnectionField(
        QuestNode, filterset_class=QuestFilter)


class RelayCreateJob(graphene.relay.ClientIDMutation):
    job = graphene.Field(JobNode)

    class Input:
        title = graphene.String()
        description = graphene.String()
        about_us = graphene.String()
        category = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user or None

        job = Job(
            title=input.get('title'),
            description=input.get('description'),
            about_us=input.get('about_us'),
            category=input.get('category'),
            posted_by=user,
        )
        job.save()

        return RelayCreateJob(job=job)


class RelayCreateQuest(graphene.relay.ClientIDMutation):
    quest = graphene.Field(QuestNode)

    class Input:
        title = graphene.String()
        description = graphene.String()
        expiring_date = graphene.Int()
        category = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user or None

        quest = Quest(
            title=input.get('title'),
            description=input.get('description'),
            expiring_date=input.get('expiring_date'),
            category=input.get('category'),
            posted_by=user,
        )
        quest.save()

        return RelayCreateQuest(quest=quest)


class RelayMutation(graphene.AbstractType):
    relay_create_job = RelayCreateJob.Field()
    relay_create_quest = RelayCreateQuest.Field()
