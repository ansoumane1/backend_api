from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 

from onlineapp.api.serializers import OrderSerializer
from onlineapp.models import Order

from django.core.mail import send_mail 
from onlineShop.settings import EMAIL_HOST_USER


class OrderAPIView(APIView):
    def get(self, request):
        try:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {},
                "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        try:
            data = request.data
            serializer = OrderSerializer(data=data)
            if serializer.is_valid():
                # Send email notification
                subject = "Order Confirmation"
                message = f"Dear customer {data['customer_name']} Your order has been placed successfully."
                recipient_list = [EMAIL_HOST_USER]  # Replace with the user's email if available
                email = data['customer_email']
                if email:
                    recipient_list.append(email)
                send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=False)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"error":serializer.errors, "message":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "data": {},
                "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request):
        try:
            order_id = request.data.get('id')
            order = Order.objects.filter(id=order_id)
            if not order.exists():
                return Response({"data":{}, "message":"Order not found with this ID"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = OrderSerializer(order[0], data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"data":serializer.data, "message": "Order update sucessfully"}, status=status.HTTP_200_OK)
            return Response({"error":serializer.errors, "message":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"data":{}, "message":"Order not found with this ID"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request):
        try: 
            data = request.data 
            order_id = data.get('id')
            print("order id: ",order_id)
            order1 = Order.objects.filter(id=order_id)
            print(order1)
            if not order1.exists():
                return Response({"data":{}, "message":"Order not found with this ID"}, status=status.HTTP_400_BAD_REQUEST)
            order1[0].delete()
            return Response({"data":{}, "message":"Order deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"data":{}, "error":str(e),  "message":"somthing went wrong when deleting"}, status=status.HTTP_404_NOT_FOUND)