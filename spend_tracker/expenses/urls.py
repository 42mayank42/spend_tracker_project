
from django.urls import path
from rest_framework import views

from expenses.views import ExpenseListCreateView, ExpenseListView, SummaryView, ExpenseSummaryView


urlpatterns = [
    path("create", ExpenseListCreateView.as_view(), name="expense-list-create"),
    path("summary/", SummaryView.as_view(), name="summary"),
    path("expense-summary/", ExpenseSummaryView.as_view(template_name = 'pages/expense_summary.html'), name="expense-summary"),
    path("expense-list/", ExpenseListView.as_view(template_name = 'pages/list.html'), name="expense-list"),

]