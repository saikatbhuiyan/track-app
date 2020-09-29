import graphene
from graphene_django import DjangoObjectType
from .models import Track


class TrackType(DjangoObjectType):
    class Meta:
        model = Track


# """Get All Tracks"""
class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType)

    def resolve_tracks(self, info):
        return Track.objects.all()



# """Create Track"""
class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    # def mutate(self, info, **kwargs):
    #     description = kwargs.get('description')
    #     title = kwargs.get('title')
    #     url = kwargs.get('url')
    #     track = Track(title=title, description=description, url=url)
    #     track.save()
    #     return CreateTrack(track=track)

    def mutate(self, info, title, description, url):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("User not logged in.")

        track = Track(title=title,
                      description=description,
                      url=url, posted_by=user)
        track.save()
        return CreateTrack(track=track)


# """Update Track"""
class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, track_id, title, description, url):
        user = info.context.user
        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise Exception("Don't have permission to update this track.")

        if user.is_anonymous:
            raise Exception("User not logged in.")

        track.title = title
        track.description = description
        track.url = url

        track.save()

        return UpdateTrack(track=track)


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
