from rest_framework import mixins, viewsets


class CreateListViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                        mixins.ListModelMixin, viewsets.GenericViewSet):
    pass
