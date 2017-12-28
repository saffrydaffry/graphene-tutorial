import graphene

from graphene import relay
from graphene_django.types import DjangoObjectType
from cookbook.ingredients.models import (
    Category,
    Ingredient
)


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        #interfaces = (relay.Node, )


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        #interfaces = (relay.Node, )


class Query(graphene.AbstractType):
    #node = relay.Node.Field()
    category = graphene.Field(CategoryType,
                              id=graphene.Int(),
                              name=graphene.String())
    all_categories = graphene.List(CategoryType)
    ingredient = graphene.Field(IngredientType,
                                id=graphene.Int(),
                                name=graphene.String())
    all_ingredients = graphene.List(IngredientType)

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Category.objects.get(pk=id)

        if name is not None:
            return Category.objects.get(name=name)
        
        return None

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Ingredient.objects.get(pk=id)
        
        if name is not None:
            return Ingredient.objects.get(name=name)
        
        return None

    def resolve_all_ingredients(self, info, **kwargs):
        return Ingredient.objects.select_related('category').all()

