"""View module for handling requests about restaurants"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.fields import BooleanField
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from favamealapi.models import Restaurant, FavoriteMeal, FavoriteRestaurant
from rest_framework.decorators import action



class RestaurantSerializer(serializers.ModelSerializer):
    """JSON serializer for restaurants"""

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'favorite')


class FaveSerializer(serializers.ModelSerializer):
    """JSON serializer for favorites"""

    class Meta:
        model = FavoriteRestaurant
        fields = ('restaurant',)
        depth = 1


class RestaurantView(ViewSet):
    """ViewSet for handling restuarant requests"""

    def create(self, request):
        """Handle POST operations for restaurants

        Returns:
            Response -- JSON serialized event instance
        """
        rest = Restaurant()
        rest.name = request.data["name"]
        rest.address = request.data["address"]

        try:
            rest.save()
            serializer = RestaurantSerializer(
                rest, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            user = request.auth.user

            # TODO: Add the correct value to the `favorite` property of the requested restaurant

            serializer = RestaurantSerializer(
                restaurant, context={'request': request})
            data = serializer.data
            if user.id in data["favorite"]:
                data["favorite"]=True
            else:
                data["favorite"]=False
            
            return Response(data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to restaurants resource

        Returns:
            Response -- JSON serialized list of restaurants
        """
        user = request.auth.user
        restaurants = Restaurant.objects.all()


        # TODO: Add the correct value to the `favorite` property of each restaurant

        serializer = RestaurantSerializer(
            restaurants, many=True, context={'request': request})
        
        for restaurant in serializer.data:
            if user.id in restaurant["favorite"]:
                restaurant["favorite"]=True
            else:
                restaurant["favorite"]=False

        return Response(serializer.data)

    # TODO: Write a custom action named `star` that will allow a client to
    # send a POST and a DELETE request to /restaurant/2/star
    @action(methods=['post', 'delete'], detail=True)
    def star(self, request, pk=None):
        user = request.auth.user
        restaurant = Restaurant.objects.get(pk=pk)

        if request.method == "POST":
            try:
                restaurant.favorite.add(user)
                return Response({f"You added {restaurant.name} as a favorite!"}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})
        elif request.method == "DELETE":
                restaurant.favorite.remove(user)
                return Response({f"You removed {restaurant.name} as a favorite."}, status=status.HTTP_204_NO_CONTENT)
