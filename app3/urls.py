from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
urlpatterns=[
    path("",views.index),
    path("login1/",views.login1),
    path("checklogin/",views.checklogin),
    path("contact/",views.contact),
    path("dashboard/",views.dashboard),
    path("brands/",views.brands),
    path("category/",views.category),
    path("products/",views.products),
    path("addcountry/",views.addcountry),
    path("savecountry/",views.savecountry),
    path("addbrands/",views.addbrands),
    path("savebrands/",views.savebrands),
    path("addcategory/",views.addcategory),
    path("savecategory/",views.savecategory),
    path("addproducts/",views.addproducts),
    path("saveproducts/",views.saveproducts),
    path("deleteproducts/<id>",views.deleteproducts),
    path("editproducts/<id>",views.editproducts),
    path("updateproducts/<id>",views.updateproducts),
    path("deletecategory/<id>",views.deletecategory),
    path("editcategory/<id>",views.editcategory),
    path("updatecategory/<id>",views.updatecategory),
    path("deletebrands/<id>",views.deletebrands),
    path("editbrands/<id>",views.editbrands),
    path("updatebrands/<id>",views.updatebrands),
    path("deletecountry/<id>",views.deletecountry),
    path("editcountry/<id>",views.editcountry),
    path("updatecountry/<id>",views.updatecountry),
    path("productsview/",views.productsview),
    path("productcart/",views.productcart),
    path("addtocart/<id>",views.addtocart),
    path("remove/<id>",views.remove),
    path("checkout/",views.checkout),
    path("save/",views.save),
    path("vieworders/",views.vieworders),
    path("delivery/",views.delivery),
    path("adddelivery/",views.adddelivery),
    path("savedelivery/",views.savedelivery),
    path("deletedelivery/<id>",views.deletedelivery),
    path("editdelivery/<id>",views.editdelivery),
    path("updatedelivery/<id>",views.updatedelivery),
    path("outfordelivery/",views.outfordelivery),
    path("save_assigned_delivery/",views.save_assigned_delivery),
    path("search/",views.search_delivery),
    path("update_status/",views.update_status),
    path("savecontact/",views.savecontact),
    path("viewcontact/",views.viewcontact),
    path("cancelledproducts/",views.cancelledproducts),
    path("cancel_order/<str:order_id>",views.cancel_order),
    path("updatepassword/", views.update_password),
    path("myorders/",views.myorders),
    path("cancelorder/<str:order_id>/",views.cancelorder),

]






