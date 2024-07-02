import pandas as pd
import openpyxl as op

#product class
class product:
    def __init__(self, product_type, model, brand,product_id, yom, price, discount, avg_rating, total_ratings, teen_buyers,mid_buyers,old_buyers, es):
        self.product_type = product_type
        self.model = model
        self.brand = brand
        self.product_id = product_id
        self.yom = yom
        self.price = price
        self.discount = discount
        self.avg_rating = avg_rating
        self.total_ratings = total_ratings
        self.teen_buyers = teen_buyers
        self.mid_buyers = mid_buyers
        self.old_buyers = old_buyers
        self.es= []

    def add_es(self, es):
        self.es.append(es)

    def __str__(self):
        return f"product(product_type={self.product_type}, product_id={self.product_id}, model={self.model}, price={self.price}, brand={self.brand},es={self.es}\
            avg_rating={self.avg_rating}, total_ratings={self.total_ratings},teen_buyers={self.teen_buyers},mid_buyers={self.mid_buyers}, old_buyers={self.old_buyers})"

#class to rank shortlisted product
class product_rank:
    def __init__(self,product,es_matches, es_view_matches, normalized_age_buyers_to_avg_rating_value, normalized_total_buyers_to_avg_rating_value,final_marks):
        self.product=product
        self.es_matches = es_matches
        self.es_view_matches = es_view_matches
        #Example (teen_buyers/total_buyers) * avg_rating
        self.normalized_age_buyers_to_avg_rating_value = normalized_age_buyers_to_avg_rating_value
        #(total_ratings/total_buyers) * avg_rating
        self.normalized_total_buyers_to_avg_rating_value = normalized_total_buyers_to_avg_rating_value
        self.final_marks = final_marks
    def __str__(self):
        return f"product_rank(product={self.product},es_matches={self.es_matches},\
              es_view_matches={self.es_view_matches},normalized_age_buyers_to_avg_rating_value={self.normalized_age_buyers_to_avg_rating_value},\
                normalized_total_buyers_to_avg_rating_value={self.normalized_total_buyers_to_avg_rating_value},final_marks={self.final_marks})"

#user profile.pb is list of products bought, pv is list of products viewed.

class userprofile:
    def __init__(self, user_id, age, pincode, pb, pv):
        self.user_id = user_id
        self.age = age
        self.pincode = pincode
        self.pb = []
        self.pv = []

    def add_interaction(self, interaction):
        self.pv.append(interaction)

    def add_pb(self, pb):
        self.pb.append(pb)

    def add_pv(self, pv):
        self.pv.append(pv)

    def __str__(self):
        return f"userprofile(user_id={self.user_id}, age={self.age}, pb={self.pb}, pv={self.pv})"
    
#data sets for various categories
electronics = {}
clothing = {}
accessories = {}
furniture = {}
homeapplicances = {}

#users database
users = {}

#read users file and populate dataset
def build_users_dataset():
    df=pd.read_excel("./products.xlsx",sheet_name="users")
    cells = df.shape
    i=0
    for i in range(0,cells[0]):
        users[i]=userprofile(df["name"][i],df["age"][i],df["pincode"][i],df["pb1"][i],df["pv1"][i])
        users[i].add_pb(df["pb1"][i])
        users[i].add_pb(df["pb2"][i])
        users[i].add_pb(df["pb3"][i])
        users[i].add_pb(df["pb4"][i])
        users[i].add_pv(df["pv1"][i])
        users[i].add_pv(df["pv2"][i])
        users[i].add_pv(df["pv3"][i])
        users[i].add_pv(df["pv4"][i])

#read products file and populate dataset lists
def build_product_datasets():
##build electronics category
    df=pd.read_excel("./products.xlsx",sheet_name="electronics")
    cells = df.shape
    print(cells)
    i=0
    for i in range(0,cells[0]):
        electronics[i]=product(df["product_type"][i], df["model"][i], df["brand"][i], df["product_id"][i],\
                                df["yom"][i], df["price"][i], df["discount"][i], df["avg_rating"][i], \
                                    df["total_ratings"][i], df["teen_buyers"][i], df["mid_buyers"][i], df["old_buyers"][i],df["es1"][i])
        electronics[i].add_es(df["es1"][i])
        electronics[i].add_es(df["es2"][i])
        electronics[i].add_es(df["es3"][i])
        electronics[i].add_es(df["es4"][i])

 #product fields for each of the category may differ,
 #build clothing category
 #build accessories category
 #build furniture category
 #build homeapplicance category

productrank = {}
def list_products_in_price_range(product_type,price):
    num_products = len(electronics)
    j=0
    pri_recommendation = []
    sec_recommendation = []
    for i in range(0,num_products):
        if(electronics[i].product_type == product_type):
            if((electronics[i].price > (price-(price/100*10))) & (electronics[i].price < (price+(price/100*10)))):
                pri_recommendation.append(electronics[i].product_id)
                productrank[j]=product_rank(electronics[i],0,0,0,0,0)
                j=j+1
    
    print(pri_recommendation)

def rank_products(user_id):
    pb_list=[]
    pv_list=[]
    teen=False
    mid=False
    old=False
#find user to get this product bought list and product viewed lists
    num_users = len(users)
    for i in range(0,num_users):
        if(users[i].user_id == user_id):
            pb_list = users[i].pb
            pv_list = users[i].pv
            if(users[i].age < 20):
                teen=True
                break
            elif(users[i].age < 40):
                mid=True
                break
            else:
                old=True
            break
    print(len(pb_list),pb_list)
    print(len(pv_list),pv_list)
    
#iterate through productrank list which has products withing the price range, check the es list of the product against pb_list (product list) of user
    if((len(pb_list) > 0) | (len(pv_list) > 0)):
        print("calculating rank")
        for i in range(0,len(productrank)):
            for k in range(0,len(productrank[i].product.es)):
                for j in range(0,len(pb_list)):
                    if(pb_list[j] == productrank[i].product.es[k]):
                        productrank[i].es_matches+=1
    
            for j in range(0,len(pv_list)):
                if(pv_list[j] == productrank[i].product.product_id):
                    productrank[i].es_view_matches+=1
    
            productrank[i].es_matches*=5
            productrank[i].es_view_matches*=2
            total_buyers = productrank[i].product.teen_buyers + productrank[i].product.mid_buyers + productrank[i].product.old_buyers
            buyers_age_factor=0
            if(teen):
                buyers_age_factor = (productrank[i].product.teen_buyers/total_buyers)
            elif(mid):
                buyers_age_factor = (productrank[i].product.mid_buyers/total_buyers)
            else:
                buyers_age_factor = (productrank[i].product.old_buyers/total_buyers)
                print("old", buyers_age_factor)
            productrank[i].normalized_age_buyers_to_avg_rating_value = buyers_age_factor * productrank[i].product.avg_rating
            productrank[i].normalized_total_buyers_to_avg_rating_value = productrank[i].product.total_ratings/total_buyers * productrank[i].product.avg_rating
            
# Rank calculation with following weightage 
# 0.4 for products bought in eco system, 0.1 for products viewed in eco system, 0.2 for normzalised ratings, 0.3 for normazlised ratings within age group
            productrank[i].final_marks = (productrank[i].es_matches*0.4)+(productrank[i].es_view_matches*0.1)+\
                (productrank[i].normalized_age_buyers_to_avg_rating_value *0.3)+(productrank[i].normalized_total_buyers_to_avg_rating_value * 0.2)
            
#their should be easy way to sort this final list, but lets do it brute force
    print("\nRecommended Products")
    print("Category ID     Model   Brand   Price  Rating")
    
    while True:
        ii=0
        value=0
        for i in range(0,len(productrank)):
            if(productrank[i].final_marks > value):
                value = productrank[i].final_marks
                ii = i
        if(value > 0):
            print(productrank[ii].product.product_type,  productrank[ii].product.product_id,  productrank[ii].product.model,  productrank[ii].product.brand,  productrank[ii].product.price,  productrank[ii].product.avg_rating)
            productrank[ii].final_marks=0
            continue
        break


print("Initiliazing product data set")
build_product_datasets()
i = len(electronics)
print("num of products in dataset= ", i)
j=0
while j<i:
    print(electronics[j])
    j=j+1
print("Initiliazing users dataset")
build_users_dataset()
i = len(users)
print("num of users = ", i)
j=0
while j<i:
    print(users[j])
    j=j+1

user_name = input("Enter User Name  > ")
print(user_name)

product_type = input("Enter Product Type, available types ( mobile,swatch,laptop,earbuds)  > ")
print(product_type)

price = int(input("Enter Approximate price you are looking for  > "))
print(price)

list_products_in_price_range(product_type,price)
rank_products(user_name)
