from django.conf import settings

import braintree
from rest_framework import views, response, status, serializers


braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id=settings.BT_MERCHANT_ID,
                                  public_key=settings.BT_PUBLIC_KEY,
                                  private_key=settings.BT_PRIVATE_KEY)


class BrainTreeTokenAPIView(views.APIView):
    def get(self, *args, **kwargs):
        try:
            token = braintree.ClientToken.generate()
        except Exception:
            return response.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response.Response({'token': token}, status=status.HTTP_200_OK)


class PaymentSerializer(serializers.Serializer):
    #opinion = serializers.PrimaryKeyRelatedField(queryset=models.Opinion.objects.all(), write_only=True)
    payment_method_nonce = serializers.CharField(required=True, write_only=True)


class PaymentAPIView(views.APIView):
    def post(self, *args, **kwargs):
        serializer = PaymentSerializer(data=self.request.data)
        serializer.is_valid(True)
        #opinion = serializer.validated_data.get('opinion')
        #if opinion.paid:
        #    return response.Response({'message': 'already paid'}, status=status.HTTP_304_NOT_MODIFIED)
        result = braintree.Transaction.sale({
            "amount": "30.00",
            "payment_method_nonce": serializer.validated_data.get('payment_method_nonce'),
            "options": {
                "submit_for_settlement": True
            }
        })
        print(result)
        if result.is_success:
            return response.Response({'message': 'payment done'}, status=status.HTTP_200_OK)
        return response.Response(status=status.HTTP_400_BAD_REQUEST)
