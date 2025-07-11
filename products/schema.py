# products/schema.py
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import ClothingStyle

class ClothingStyleType(DjangoObjectType):
    class Meta:
        model = ClothingStyle
        fields = '__all__'

class Query(graphene.ObjectType):
    all_clothing_styles = graphene.List(ClothingStyleType)
    clothing_style = graphene.Field(ClothingStyleType, id=graphene.ID())
    active_clothing_styles = graphene.List(ClothingStyleType)

    def resolve_all_clothing_styles(self, info):
        return ClothingStyle.objects.all()

    def resolve_clothing_style(self, info, id):
        try:
            return ClothingStyle.objects.get(pk=id)
        except ClothingStyle.DoesNotExist:
            return None

    def resolve_active_clothing_styles(self, info):
        return ClothingStyle.objects.filter(is_active=True)

class CreateClothingStyle(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        cost = graphene.Decimal(required=True)
        image = graphene.String(required=True)

    clothing_style = graphene.Field(ClothingStyleType)

    def mutate(self, info, name, description, cost, image):
        clothing_style = ClothingStyle(
            name=name,
            description=description,
            cost=cost,
            image=image
        )
        clothing_style.save()
        return CreateClothingStyle(clothing_style=clothing_style)

class UpdateClothingStyle(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        cost = graphene.Decimal()
        image = graphene.String()
        is_active = graphene.Boolean()

    clothing_style = graphene.Field(ClothingStyleType)

    def mutate(self, info, id, **kwargs):
        try:
            clothing_style = ClothingStyle.objects.get(pk=id)
            for field, value in kwargs.items():
                if value is not None:
                    setattr(clothing_style, field, value)
            clothing_style.save()
            return UpdateClothingStyle(clothing_style=clothing_style)
        except ClothingStyle.DoesNotExist:
            return None

class DeleteClothingStyle(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            clothing_style = ClothingStyle.objects.get(pk=id)
            clothing_style.delete()
            return DeleteClothingStyle(success=True)
        except ClothingStyle.DoesNotExist:
            return DeleteClothingStyle(success=False)

class Mutation(graphene.ObjectType):
    create_clothing_style = CreateClothingStyle.Field()
    update_clothing_style = UpdateClothingStyle.Field()
    delete_clothing_style = DeleteClothingStyle.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)