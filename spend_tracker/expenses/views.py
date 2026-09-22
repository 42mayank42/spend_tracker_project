from django.db.models import Sum
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Expense
from .serializers import ExpenseSerializer

class ExpenseListCreateView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

# class SummaryView(APIView):
#     def get(self, request):
#         total = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
#         return Response({'total_spend': total})

from datetime import date, timedelta

from django.db.models import Sum

# class SummaryView(APIView):

#     def get(self, request):

#         # Total Spend
#         total_spend = (
#             Expense.objects.aggregate(total=Sum('amount'))['total']
#             or 0
#         )

#         # Spend by Category
#         category_data = (
#             Expense.objects
#             .values('category')
#             .annotate(total=Sum('amount'))
#             .order_by('category')
#         )

#         spend_by_category = {
#             item['category']: float(item['total'])
#             for item in category_data
#         }

#         # Current Month
#         today = date.today()

#         current_month_total = (
#             Expense.objects.filter(
#                 date__year=today.year,
#                 date__month=today.month
#             )
#             .aggregate(total=Sum('amount'))['total']
#             or 0
#         )

#         # Previous Month
#         previous_month_date = (
#             today.replace(day=1) - timedelta(days=1)
#         )

#         previous_month_total = (
#             Expense.objects.filter(
#                 date__year=previous_month_date.year,
#                 date__month=previous_month_date.month
#             )
#             .aggregate(total=Sum('amount'))['total']
#             or 0
#         )

#         # Month-over-Month Change
#         if previous_month_total > 0:
#             percentage_change = round(
#                 (
#                     (current_month_total - previous_month_total)
#                     / previous_month_total
#                 ) * 100,
#                 2
#             )
#         else:
#             percentage_change = 0

#         return Response({
#             "total_spend": float(total_spend),
#             "spend_by_category": spend_by_category,
#             "month_over_month_change": {
#                 "current_month": float(current_month_total),
#                 "previous_month": float(previous_month_total),
#                 "percentage_change": percentage_change
#             }
#         })

from datetime import date, timedelta
from django.db.models import Sum
from django.views.generic import TemplateView
from .models import Expense

class SummaryView(APIView):

    def get(self, request, *args, **kwargs):

        total_spend = Expense.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0

        spend_by_category = (
            Expense.objects
            .values('category')
            .annotate(total=Sum('amount'))
        )

        today = date.today()

        current_month = (
            Expense.objects.filter(
                date__year=today.year,
                date__month=today.month
            ).aggregate(total=Sum('amount'))['total']
            or 0
        )

        previous_month_date = (
            today.replace(day=1) - timedelta(days=1)
        )

        previous_month = (
            Expense.objects.filter(
                date__year=previous_month_date.year,
                date__month=previous_month_date.month
            ).aggregate(total=Sum('amount'))['total']
            or 0
        )

        percentage_change = 0

        if previous_month > 0:
            percentage_change = round(
                ((current_month - previous_month) / previous_month) * 100,
                2
            )

        return Response({
        "total_spend": float(total_spend),
        "spend_by_category": list(spend_by_category),
        "month_over_month_change": {
            "current_month": float(current_month),
            "previous_month": float(previous_month),
            "percentage_change": percentage_change,
        }},status=200)
        

    
class ExpenseSummaryView(TemplateView):
    template_name = "pages/summary.html"

    def get_context_data(self, **kwargs):

        template_name = 'pages/summary.html' 
        context = super().get_context_data(**kwargs)
        total_spend = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        context['total_spend'] = total_spend
        return context

class ExpenseListView(TemplateView):
    template_name = "pages/list.html"

    def get_context_data(self, **kwargs):

        template_name = 'pages/list.html' 
        context = super().get_context_data(**kwargs)
        expenses = Expense.objects.all()
        context['expenses'] = expenses
        return context