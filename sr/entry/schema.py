import graphene
from graphene_django import DjangoObjectType

from entry.models import Entry
from sr.decorators import graphql_login_required, graphql_permission_required


class EntryType(DjangoObjectType):
    class Meta:
        model = Entry
        fields = ("id", "title", "content")


class Query(graphene.ObjectType):
    entries = graphene.List(EntryType, q=graphene.String())

    @graphql_login_required
    def resolve_entries(root, info, q=None):
        if q:
            return Entry.objects.all().search(q)
        return Entry.objects.all()


class CreateEntry(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        content = graphene.String()

    entry = graphene.Field(EntryType)
    ok = graphene.Boolean()

    @graphql_login_required
    @graphql_permission_required(['entry.add_entry'])
    def mutate(root, info, title, content):
        entry = Entry.objects.create(title=title, content=content, user=info.context.user)
        return CreateEntry(entry=entry, ok=True)


class UpdateEntry(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        title = graphene.String()
        content = graphene.String()

    ok = graphene.Boolean()

    @graphql_login_required
    @graphql_permission_required(['entry.change_entry'])
    def mutate(root, info, id, title, content):
        try:
            entry = Entry.objects.get(pk=id)
        except Entry.DoesNotExist:
            return UpdateEntry(ok=False)

        entry.title = title
        entry.content = content
        entry.save()
        return UpdateEntry(ok=True)


class Mutation(graphene.ObjectType):
    create_entry = CreateEntry.Field()
    update_entry = UpdateEntry.Field()
