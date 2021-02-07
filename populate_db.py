import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

django.setup()
from api.models import *

# random user
u1 = User(username="user1", email="user1@gmail.com")
u1.set_password("a")

user_pref1 = UserDietaryPreferences()
user_pref1.user=u1
user_pref1.dietary_preferences = DiertaryRequirements(has_halal=True)
user_pref1.dietary_preferences.save()
u2 = User(username="user2", email="user2@gmail.com")
u2.set_password("a")

user_pref2 = UserDietaryPreferences()
user_pref2.user=u2
user_pref2.dietary_preferences = DiertaryRequirements(has_gluten_free=True, has_lactose_free=True)
user_pref2.dietary_preferences.save()
u3 = User(username="user3", email="user3@gmail.com")
u3.set_password("a")

user_pref3 = UserDietaryPreferences()
user_pref3.user=u3
user_pref3.dietary_preferences = DiertaryRequirements(has_kosher=True, has_sanitary_products=True)
user_pref3.dietary_preferences.save()

# u1 = User.objects.get(username="user1")

#Foodbank 1
a1 = Address()
a1.address_line_1="Millbrix Avenue, Scotstoun"
a1.city="Glasgow"
a1.postcode="G14 0EP"
a1.longitude=-4.364900
a1.latitude= 55.885550

fb1 = CharityAccount()
fb1.user=u1
fb1.charityname="Blawarthill Parish Church"
fb1.email = "foodbank.parish.church@gmail.com"
fb1.phone = "44 141 579 6521"
fb1.address = a1

diet1 = DiertaryRequirements()
diet1.has_halal = True
diet1.has_sanitary_products = True
diet1.has_vegetarian = True
diet1.has_vegan = True
diet1.has_kosher = True
diet1.has_gluten_free = True
diet1.has_lactose_free = True

fb1diet= CharityDietaryOptions()
fb1diet.charity=fb1
fb1diet.dietary_options=diet1

#Foodbank 2
a2 = Address()
a2.address_line_1=" 142 Helenvale Street, Parkhead"
a2.city="Glasgow"
a2.postcode="G31 4NA"
a2.longitude=-4.195890
a2.latitude= 55.850680

fb2 = CharityAccount()
fb2.user=u1
fb2.charityname="Calton Parkhead Parish Church"
fb2.email = "foodbank.calton.parkhead@gmail.com"
fb2.phone = "07779224521"
fb2.address = a2

diet2 = DiertaryRequirements()
diet2.has_halal = False
diet2.has_sanitary_products = True
diet2.has_vegetarian = True
diet2.has_vegan = True
diet2.has_kosher = True
diet2.has_gluten_free = False
diet2.has_lactose_free = False

fb2diet= CharityDietaryOptions()
fb2diet.charity=fb2
fb2diet.dietary_options=diet2

#Foodbank 3
a3 = Address()
a3.address_line_1="Clifford Street"
a3.city="Glasgow"
a3.postcode="G51 1QL"
a3.longitude=-4.298760
a3.latitude= 55.850320

fb3 = CharityAccount()
fb3.user=u1
fb3.charityname="Ibrox Parish Church"
fb3.email = "foodbank.ibrox.church@gmail.com"
fb3.phone = "07950 771877"
fb3.address = a3

diet3 = DiertaryRequirements()
diet3.has_halal = False
diet3.has_sanitary_products = True
diet3.has_vegetarian = True
diet3.has_vegan = False
diet3.has_kosher = False
diet3.has_gluten_free = True
diet3.has_lactose_free = False

fb3diet= CharityDietaryOptions()
fb3diet.charity=fb3
fb3diet.dietary_options=diet3

#Foodbank 4
a4 = Address()
a4.address_line_1="Authurlie Street, Barrhead"
a4.city="Glasgow"
a4.postcode="G78 2RB"
a4.longitude=-4.386660
a4.latitude= 55.798260

fb4 = CharityAccount()
fb4.user=u2
fb4.charityname="United Reformed Church"
fb4.email = "United.Reformed.church@gmail.com"
fb4.address = a4

diet4 = DiertaryRequirements()
diet4.has_halal = False
diet4.has_sanitary_products = False
diet4.has_vegetarian = True
diet4.has_vegan = False
diet4.has_kosher = False
diet4.has_gluten_free = True
diet4.has_lactose_free = False

fb4diet= CharityDietaryOptions()
fb4diet.charity=fb4
fb4diet.dietary_options=diet4

#Foodbank 5
a5 = Address()
a5.address_line_1="89 Dumbarton Rd"
a5.city="Glasgow"
a5.postcode=" G11 6PW"
a5.longitude=-4.297830
a5.latitude= 55.870060

fb5 = CharityAccount()
fb5.user=u2
fb5.charityname="Vineyard Church "
fb5.email = "foodbank.Vineyard.church@gmail.com"
fb5.phone = "41 334 6746"
fb5.address = a5

diet5 = DiertaryRequirements()
diet5.has_halal = False
diet5.has_sanitary_products = True
diet5.has_vegetarian = True
diet5.has_vegan = False
diet5.has_kosher = False
diet5.has_gluten_free = False
diet5.has_lactose_free = False

fb5diet= CharityDietaryOptions()
fb5diet.charity=fb5
fb5diet.dietary_options=diet5

#Foodbank 6
a6 = Address()
a6.address_line_1="Trinity Cottage, 96 Union Street"
a6.city="Larkhall"
a6.postcode=" ML9 1EF"
a6.longitude=-3.973580
a6.latitude= 55.739240

fb6 = CharityAccount()
fb6.user=u2
fb6.charityname="Clyde, Avon & Nethan"
fb6.email = "Clyde.Avon.Nethan@gmail.com"
fb6.phone = "07591 104027"
fb6.address = a6

diet6 = DiertaryRequirements()
diet6.has_halal = False
diet6.has_sanitary_products = True
diet6.has_vegetarian = True
diet6.has_vegan = False
diet6.has_kosher = False
diet6.has_gluten_free = False
diet6.has_lactose_free = False

fb6diet= CharityDietaryOptions()
fb6diet.charity=fb6
fb6diet.dietary_options=diet6

#Foodbank 7
a7 = Address()
a7.address_line_1="52 Townhead, Kirkintilloch"
a7.city="Glasgow"
a7.postcode="G66 1NL"
a7.longitude=-4.153040
a7.latitude= 55.936640

fb7 = CharityAccount()
fb7.user=u3
fb7.charityname="East Dunbartonshire foodbank"
fb7.email = "Dunbartonshire.foodbank@gmail.com"
fb7.phone = "0141 578 6006"
fb7.address = a7

diet7 = DiertaryRequirements()
diet7.has_halal = True
diet7.has_sanitary_products = True
diet7.has_vegetarian = True
diet7.has_vegan = True
diet7.has_kosher = True
diet7.has_gluten_free = True
diet7.has_lactose_free = True

fb7diet= CharityDietaryOptions()
fb7diet.charity=fb7
fb7diet.dietary_options=diet7
def populate():

    u1.save()
    user_pref1.save()
    u2.save()
    user_pref2.save()
    u3.save()
    user_pref3.save()

    a1.save()
    fb1.save()
    diet1.save()
    fb1diet.save()
    a2.save()
    fb2.save()
    diet2.save()
    fb2diet.save()
    a3.save()
    fb3.save()
    diet3.save()
    fb3diet.save()
    a4.save()
    fb4.save()
    diet4.save()
    fb4diet.save()
    a5.save()
    fb5.save()
    diet5.save()
    fb5diet.save()
    a6.save()
    fb6.save()
    diet6.save()
    fb6diet.save()
    a7.save()
    fb7.save()
    diet7.save()
    fb7diet.save()

# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()