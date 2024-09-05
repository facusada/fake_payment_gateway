from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Payment
import uuid
import random

@api_view(['POST'])
def process_payment(request):
    data = request.data

    try:
        amount = float(data.get('amount', 0))
        if amount <= 0:
            return Response({'error': 'El monto debe ser mayor que cero.'}, status=400)
    except ValueError:
        return Response({'error': 'Monto inválido.'}, status=400)

    transaction_id = str(uuid.uuid4())
    
    random.seed()
    payment_status = random.choice(['approved', 'rejected'])
    
    payment = Payment.objects.create(
        transaction_id=transaction_id,
        amount=amount,
        status=payment_status,
        payment_method=data.get('payment_method', 'credit_card'),
        currency=data.get('currency', 'USD')
    )

    response_data = {
        'transaction_id': payment.transaction_id,
        'status': payment.status,
        'amount': payment.amount,
        'message': 'Payment processed successfully!' if payment.status == 'approved' else 'Payment failed!'
    }
    
    return Response(response_data)

@api_view(['GET'])
def payment_status(request, transaction_id):
    try:
        payment = Payment.objects.get(transaction_id=transaction_id)
        response_data = {
            'transaction_id': payment.transaction_id,
            'status': payment.status,
            'amount': payment.amount,
            'currency': payment.currency,
            'message': f'Payment status is {payment.status}'
        }
        return Response(response_data)
    except Payment.DoesNotExist:
        return Response({'error': 'Transacción no encontrada.'}, status=404)