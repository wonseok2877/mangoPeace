import json

from json.decoder           import JSONDecodeError
from django.db.models.query import Prefetch
from django.http            import JsonResponse
from django.views           import View
from django.db.utils        import DataError
from django.db.models       import Avg, Q, Count
from django.utils           import timezone

from restaurants.models     import Restaurant, Food, SubCategory, Image
from users.utils            import ConfirmUser, LooseConfirmUser
from users.models           import Review


class RestaurantDetailView(View):
    @LooseConfirmUser
    def get(self, request, restaurant_id):
        try:
            restaurant         = Restaurant.objects.select_related("sub_category").prefetch_related("foods").filter(id=restaurant_id).annotate(
                rating_total   = Count("reviews"),
                rating_one     = Count("reviews", filter=Q(reviews__rating=1)),
                rating_two     = Count("reviews", filter=Q(reviews__rating=2)),
                rating_three   = Count("reviews", filter=Q(reviews__rating=3)),
                rating_four    = Count("reviews", filter=Q(reviews__rating=4)),
                rating_five    = Count("reviews", filter=Q(reviews__rating=5)),
                average_rating = Avg("reviews__rating"),
                )[0]
            average_price      = restaurant.foods.aggregate(Avg("price"))["price__avg"]
            is_wished          = request.user.wishlist_restaurants.filter(id=restaurant_id).exists() if request.user else False
            result             = {
            "id"             : restaurant.id,
            "sub_category"   : restaurant.sub_category.name,
            "name"           : restaurant.name,
            "address"        : restaurant.address,
            "phone_number"   : restaurant.phone_number,
            "coordinate"     : restaurant.coordinate,
            "open_time"      : restaurant.open_time,
            "updated_at"     : restaurant.updated_at,
            "is_wished"      : is_wished,
            "reviews_count"   : {
                "total"        : restaurant.rating_total,
                "rating_one"   : restaurant.rating_one,
                "rating_two"   : restaurant.rating_two,
                "rating_three" : restaurant.rating_three,
                "rating_four"  : restaurant.rating_four,
                "rating_five"  : restaurant.rating_five,
                },
            "average_rating" : restaurant.average_rating,
            "average_price"  : average_price,
            }

            return JsonResponse({"message":"SUCCESS", "result":result}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)

        except IndexError:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)   


class RestaurantFoodsView(View):
    def get(self, request, restaurant_id):
        try:
            foods      = Food.objects.prefetch_related("images").filter(restaurant_id=restaurant_id)
            foods_list = [{
                "id"     : food.id, 
                "name"   : food.name, 
                "price"  : food.price, 
                "images" : [image.image_url for image in food.images.all()]
            } for food in foods]

            return JsonResponse({"message":"success", "result":foods_list}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=404)
            

class WishListView(View):
    @ConfirmUser
    def post(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)

            if request.user.wishlist_restaurants.filter(id=restaurant_id).exists():
                return JsonResponse({"message":"WISHLIST_ALREADY_EXISTS"}, status=400)

            request.user.wishlist_restaurants.add(restaurant)
            
            return JsonResponse({"message":"SUCCESS"}, status=201)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=404)   
        
    @ConfirmUser
    def delete(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)

            if not request.user.wishlist_restaurants.filter(id=restaurant_id).exists():
                return JsonResponse({"message":"WISHLIST_NOT_EXISTS"}, status=404)

            request.user.wishlist_restaurants.remove(restaurant)

            return JsonResponse({"message":"SUCCESS"}, status=204)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=404)


class RestaurantReviewsView(View):
    @ConfirmUser
    def post(self, request, restaurant_id):
        try:
            data = json.loads(request.body)
            Review.objects.create(
                user          = request.user,
                restaurant_id = restaurant_id,
                content       = data["content"],
                rating        = data["rating"]
            )

            return JsonResponse({"message":"SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        
        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)     

    def get(self, request, restaurant_id):
        offset        = int(request.GET.get("offset", 0))
        limit         = int(request.GET.get("limit", 10))
        rating_min    = request.GET.get("rating-min", 1)
        rating_max    = request.GET.get("rating-max", 5)
        reviews       = Review.objects.prefetch_related("user").filter(restaurant_id=restaurant_id, rating__gte = rating_min, rating__lte = rating_max)\
                                .annotate(review_count=Count("user__reviewed_restaurants")).order_by("-created_at")[offset : offset + limit]
        review_list   = [{
            "id"         : review.id,
            "content"    : review.content,
            "rating"     : review.rating,
            "created_at" : review.created_at,
            "user":{
                "id"            : review.user.id,
                "nickname"      : review.user.nickname,
                "profile_image" : review.user.profile_url,
                "review_count"  : review.user.reviewed_restaurants.count()
                },
            } for review in reviews]

        return JsonResponse({"message":"success", "result":review_list}, status=200)


class RestaurantReviewView(View):
    @ConfirmUser
    def patch(self, request, restaurant_id, review_id):
        try:
            data = json.loads(request.body)

            if not Review.objects.filter(id=review_id, user_id=request.user.id).exists():
                return JsonResponse({"message":"REVIEW_NOT_EXISTS"}, status=404)

            Review.objects.filter(id=review_id, user_id=request.user.id).update(content=data["content"], rating=data["rating"], updated_at=timezone.now())
            
            return JsonResponse({"message":"SUCCESS"}, status=204)
            
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)
    
    @ConfirmUser
    def delete(self, request, restaurant_id, review_id):
        try:
            Review.objects.get(id=review_id, user_id=request.user.id).delete()

            return JsonResponse({"message":"SUCCESS"}, status=204)

        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)

        except Review.DoesNotExist:
            return JsonResponse({"message":"REVIEW_NOT_EXISTS"}, status=404)


class SubCategoriesView(View):
    def get(self, request):
        try:
            subcategories = SubCategory.objects.prefetch_related(
                Prefetch(
                    lookup="restaurant",
                    queryset=Restaurant.objects.prefetch_related(
                        Prefetch(
                            lookup="foods",
                            queryset=Food.objects.prefetch_related(
                                Prefetch(
                                    lookup="images",
                                    queryset=Image.objects.all(),
                                    to_attr="all_images"
                            )),
                            to_attr="all_foods"
                    )), 
                    to_attr="all_restaurants"
            ))

            result = [{
                "id" : subcategory.id,
                "name" : subcategory.name,
                "image" : subcategory.all_restaurants[0].all_foods[0].all_images[0].image_url,
            }for subcategory in subcategories]

            return JsonResponse({
                "message" : "SUCCESS",
                "result"  : result
                }, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)


class RestaurantsView(View):
    def get(self, request):
        sorted_dict     = {
            "rating"       : "-average_rating",
            "review_count" : "-reviews_counts"
        }
        keyword         = request.GET.get('keyword', None)
        offset          = int(request.GET.get('offset', 0))
        limit           = int(request.GET.get('limit', 6))
        sort            = request.GET.get("sort", "rating")
        sub_categories  = request.GET.getlist("subCategory", None)

        try:
            q = Q()

            if keyword:
                q &= Q(name__contains = keyword) | Q(sub_category__name = keyword) | Q(sub_category__category__name = keyword)

            if sub_categories:
                for sub_category in sub_categories:
                    q |= Q(sub_category__name__contains = sub_category)

            restaurants = Restaurant.objects.filter(q).prefetch_related(
                Prefetch(
                    lookup="foods",
                    queryset=Food.objects.prefetch_related(
                        Prefetch(
                            lookup="images",
                            queryset=Image.objects.all(),
                            to_attr="all_images"
                    )),
                    to_attr="all_foods"
            )).annotate(
                average_rating=Avg('reviews__rating'),
                reviews_counts=Count('reviews')
            ).order_by(sorted_dict[sort])[offset:offset+limit]

            return JsonResponse({
                "ok"        : True,
                "message"   : "SUCCESS",
                "result"    : [{
                    "restaurantID"          : restaurant.id,
                    "restaurantName"        : restaurant.name,
                    "restaurantAddress"     : restaurant.address,
                    "restaurantPhoneNum"    : restaurant.phone_number,
                    "restaurantCoordinate"  : restaurant.coordinate,
                    "restaurantOpenTime"    : restaurant.open_time,
                    "foodImageUrl"          : restaurant.all_foods[0].all_images[0].image_url,
                    "averageRating"         : restaurant.average_rating,
                    "reviewCount"           : restaurant.reviews_counts,
                }for restaurant in restaurants]
            }, status=200)
        
        except JSONDecodeError:
            return JsonResponse({"ok" : False, "message" : "JsonDecodeError"}, status=400)