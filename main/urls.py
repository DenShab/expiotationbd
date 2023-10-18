from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='home'),
    path('card/<int:idcard>/', views.card, name='card'),
    path('addPerson/', views.addPerson, name='addPerson'),
    path('aboba/', views.aboba, name='aboba'),
    path('monitoring/', views.monitoring, name='monitoring'),
    path('registerOfViolations/', views.registerOfViolations, name='registerOfViolations'),
    path('addRegisterOfViolations/', views.addRegisterOfViolations, name='addRegisterOfViolations'),
    path('cardRegisterOfViolations/<int:idcard>/', views.cardRegisterOfViolations, name='cardRegisterOfViolations'),
    path('accountingForInjuries/', views.injuryAccounting, name='accountingForInjuries'),
    path('addAccountingForInjuries/', views.addInjuryAccounting, name='addAccountingForInjuries'),
    path('cardAccountingForInjuries/<int:idcard>/', views.cardInjuryAccounting, name='cardAccountingForInjuries'),
    path('documentation/', views.documentation, name='documentation'),
    path('testing/', views.testing, name='testing'),
    path('addTesting/', views.addTesting, name='addTesting'),
    path('expenses/', views.expenses, name='expenses'),
    path('addExpenses/', views.addExpenses, name='addExpenses'),
    path('orders/', views.orders, name='orders'),
    path('addOrders/', views.addOrders, name='addOrders'),
    path('equipmentAccounting/', views.equipmentAccounting, name='equipmentAccounting'),
    path('addEquipmentAccounting/', views.addEquipmentAccounting, name='addEquipmentAccounting'),
    path('email_autocomplete/', views.email_autocomplete, name='email_autocomplete'),
    path('expenses_autocomplete/', views.expenses_autocomplete, name='expenses_autocomplete'),
    path('controller/', views.ajax_view, name='controller'),
    path('controllerTesting/', views.ajax_view_testing, name='controllerTesting'),
    path('controllerTechnicalExaminations/', views.ajax_view_technicalExaminations, name='controllerTechnicalExaminations')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
