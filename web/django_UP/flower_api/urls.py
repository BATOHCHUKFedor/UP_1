from .views import *
from rest_framework import routers

urlpatterns = [
    
]

router = routers.SimpleRouter()
router.register('category', CategoryViewSet, basename='category_router')
router.register('collection', CollectionViewSet, basename='collection_router')
router.register('supplier', SupplierViewSet, basename='supplier_router')
router.register('flowers', FlowersViewSet, basename='flowers_router')
router.register('order', OrderViewSet, basename='order_router')
router.register('orderitem', OrderItemViewSet, basename='orderitem_router')
router.register('review', ReviewViewSet, basename='review_router')
router.register('promocode', PromoCodeViewSet, basename='promocode_router')
urlpatterns += router.urls