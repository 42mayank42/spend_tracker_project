from django.db.models import Sum
from datetime import date, timedelta
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework.permissions import IsAuthenticated
class ExpenseListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]     #uncomment this line to require authentication for this view via JWT
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class SummaryView(APIView):
    # permission_classes = [IsAuthenticated]
    # Uncomment the above line to require JWT authentication

    def get(self, request, *args, **kwargs):

        # Calculate the total amount spent across all expenses
        total_spend = Expense.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0

        # Group expenses by category and calculate total spend for each category
        # Example:
        # [
        #     {"category": "Food", "total": 500},
        #     {"category": "Travel", "total": 1200}
        # ]
        spend_by_category = (
            Expense.objects
            .values('category')
            .annotate(total=Sum('amount'))
        )

        # Get today's date to determine current and previous months
        today = date.today()

        # Calculate total spend for the current month
        current_month = (
            Expense.objects.filter(
                date__year=today.year,
                date__month=today.month
            ).aggregate(total=Sum('amount'))['total']
            or 0
        )

        # Determine the previous month by moving to the last day
        # of the previous month from the first day of the current month
        previous_month_date = (
            today.replace(day=1) - timedelta(days=1)
        )

        # Calculate total spend for the previous month
        previous_month = (
            Expense.objects.filter(
                date__year=previous_month_date.year,
                date__month=previous_month_date.month
            ).aggregate(total=Sum('amount'))['total']
            or 0
        )

        # Calculate month-over-month percentage change in spending
        # Formula:
        # ((Current Month - Previous Month) / Previous Month) * 100
        percentage_change = 0

        # Avoid division by zero if no expenses existed in previous month
        if previous_month > 0:
            percentage_change = round(
                ((current_month - previous_month) / previous_month) * 100,
                2
            )

        # Return summarized expense analytics
        return Response({
            "total_spend": float(total_spend),
            "spend_by_category": list(spend_by_category),
            "month_over_month_change": {
                "current_month": float(current_month),
                "previous_month": float(previous_month),
                "percentage_change": percentage_change,
            }
        }, status=200)

    
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