"""This script use OFF to find a substitute from a given product, then permit to add into bdd or not

    It uses the module search.py to create a Search object.

    First the user selects a category. Then a product belonging to this category.
    Finally the system finds out an organic substitute of this product.
"""
import os
import time
import modules.search as search
import mysql.connector


# ******************************************* variables

class Choice():

    TUP_CATEGORY = ("Jus de fruits", "Céréales", "Confiture", "Barre chocolatee",\
        "Lait", "Chips", "Bretzels", "Yaourts", "Boissons Alcoolisées", "Gâteaux", "Pains de mie", "Charcuterie",\
        "Pizzas", "Tartes salées", "Spaghetti", "Riz", "Glaces", "Chocolat noir", "Soupes", "Compotes")


    def __init__(self):
        self.cat = self.display_choice_cat()
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="123",
            database="python"
        )
        self.my_cursor = self.mydb.cursor()


# ******************************************* main

    def _negatif_feed_back(msg):
        """ displays a negatif feed back then 1 sec break """
        print("\n", msg, "\n")
        time.sleep(1)


    def _display_title(self,msg):

        os.system("cls")
        print("\n", "-"*30, " PAGE DE RECHERCHE ", "-"*30)
        print(".... Choisir {} ....\n".format(msg))


    def _get_prod_from_cat(self, cat):
        """ returns 20 prod from db found with a given category and gather them in list """

        sql = 'select name from product where category = "{}";'.format(cat)
        self.my_cursor.execute(sql)
        my_result = self.my_cursor.fetchall()

        list_prod = []

        for i in my_result:
            list_prod.append(i)

        return list_prod


    def display_choice_cat(self):
        """ permits user to make a choice among 20 categories"""

        self._display_title("une catégorie")

        not_acceptable_answer = True
        while not_acceptable_answer:
        #loop in order to repeat the input question until an acceptable answer

            print("Ecrivez un nombre pour choisir votre catégorie :")
            count = 1
            for i in self.TUP_CATEGORY:
                print("\t{} -> {}".format(count, i))
                count +=1
            print("21 : Revenir au menu principal")
            ind_category = input(">")

            try:
                if ind_category == "21":
                    input("Retour au menu principal ! ")
                    return None, None, False
                elif int(ind_category) < 21:
                    print("Vous avez choisi : {}".format(self.TUP_CATEGORY[int(ind_category)-1]))
                    return self.TUP_CATEGORY[int(ind_category)-1]
                else:
                    print("Un nombre entre 1 et 21 est attendu ! ")
            except:
                print("Un nombre entre 1 et 21 est attendu ! ")


    def display_choice_prod(self, cat):
        """ permits user to make a choice among 20 categories"""

        self._display_title("un produit")

        list_prod = self._get_prod_from_cat(cat)

        not_acceptable_answer = True
        while not_acceptable_answer:
        #loop in order to repeat the input question until an acceptable answer
            print("Ecrivez un nombre pour choisir votre produit :")
            count = 1
            for i in list_prod:
                print("\t{} -> {}".format(count, i))
                count +=1
            print("21 : Revenir au menu principal")
            ind_prod = input(">")

            try :
                ind_prod = int(ind_prod)
                if ind_prod == "21":
                    input("Retour au menu principal ! ")
                    return None, None, False
                elif ind_prod < 21:
                    print("Vous avez choisi : {}".format(list_prod[int(ind_prod)-1]))
                    return list_prod[int(ind_prod)-1]
                else:
                    print("Un nombre entre 1 et 21 est attendu ! ")
            except:
                print("Un nombre entre 1 et 21 est attendu ! ")


        # not_acceptable_answer = True
        # while not_acceptable_answer:
        # #loop in order to repeat the input question until an acceptable answer
        #     print("Ecrivez un nombre pour choisir votre produit :")
        #     count = 1
        #     for i in self.TUP_CATEGORY:
        #         print("\t{} -> {}".format(count, i))
        #         count +=1
        #     print("21 : Revenir au menu principal")
        #     ind_category = input(">")

        #     if ind_category == "21":
        #         input("Retour au menu principal ! ")
        #         return None, None, False
        #     elif int(ind_category) > 21:
        #         continue
        #     else:
        #         print("Vous avez choisi : {}".format(self.TUP_CATEGORY[int(ind_category)]))
        #         return self.TUP_CATEGORY[int(ind_category)]

def main():

    choice = Choice()
    selected_cat = choice.cat
    selected_prod = choice.display_choice_prod(selected_cat)


main()
# def find_substitute():
#     """ finds a substitute from a given product from a given category """
#     os.system("cls")
#     print("\n", "-"*30, " PAGE DE RECHERCHE ", "-"*30, "\n")

#     not_acceptable_answer = True
#     while not_acceptable_answer:
#     #loop in order to repeat the input question until an acceptable answer

#         ind_category = input("Choisissez une catégorie à partir de son numéro : \n  1 - {},\n  2 - {},"\
#             "\n  3 - {},\n  4 - {},\n  5 - Sortir.\n ->".format(TUP_CATEGORY[0], \
#                 TUP_CATEGORY[1], TUP_CATEGORY[2], TUP_CATEGORY[3]))


#         if ind_category == "5":
#             input("Retour au menu principal ! ")
#             return None, None, False

#         try:
#             category_name = TUP_CATEGORY[int(ind_category)-1] #necessary for my search object

#             tup_product = DICT_CATEGORY[int(ind_category)]

#             ind_product = input("\nChoisissez un produit :  \n  1 - {},\n  2 - {},"\
#             "\n  3 - {},\n  4 - {},\n  5 - Sortir.\n ->"\
#             .format(tup_product[0], tup_product[1], tup_product[2], tup_product[3]))

#             if ind_product == "5":
#                 input("Retour au menu principal ! ")
#                 return None, None, False

#             product_name = tup_product[int(ind_product)-1]
#             not_acceptable_answer = False

#         #tup_product[int(ind_product)-1] can raise an error
#         except IndexError:
#             _negatif_feed_back("Il faut donner un nombre entre 1 et 5 !")



#     os.system("cls")
#     print("\n", "-"*30, " PAGE DU RESULTAT ", "-"*30, "\n")

#     my_search = search.Search(category_name, product_name)
#     #Search object is necessary to write in db

#     my_substitute = my_search.get_substitute()#Search object can manage the search

#     print(my_substitute) #no need to input because another input after

#     not_acceptable_answer = True
#     while not_acceptable_answer:

#         save = input("Voulez-vous enregistrer ces résultats ? \n  1 - Oui,\n  2 - Non.\n ->")

#         if save == "1":
#             return my_substitute, my_search, True
#         elif save == "2":
#             print("\nJe vous ramène à la page principale. ")
#             return None, None, False
#         else:
#             _negatif_feed_back("Il faut donner comme réponse oui ou non !")
