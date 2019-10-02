"""This script use OFF to find a substitute from a given product.

    It uses the module search.py to create a Search object.

    First the user selects a category. Then a product belonging to this category.
    Finally the system finds out an organic substitute of this product.
"""
import os, sys
import time
import modules.search as search
import mysql.connector


# ******************************************* variables
class Interaction():

    TUP_CATEGORY = ("Jus de fruits", "Céréales", "Confiture", "Barre chocolatee",\
    "Lait", "Chips", "Bretzels", "Yaourts", "Poissons", "Gâteaux", \
    "Pains de mie", "Charcuterie","Pizzas", "Tartes salées", "Spaghetti", "Riz",\
    "Glaces", "Chocolat noir", "Soupes", "Compotes" )


    def negatif_feed_back(self,msg):
        """ displays a negatif feed back then 1 sec break """
        print("\n", msg, "\n")
        time.sleep(1)

    def display_title(self,msg):
        """ displays a title a the top of the page """
        os.system("cls")
        print("\n", "-"*30, " PAGE DE RECHERCHE ", "-"*30)
        print(".... {} \n".format(msg))

    def input_cat_prod(self, wanted, my_liste):
        """ Lets the user choose a cat """
        print("Ecrivez un nombre pour choisir votre {} :".format(wanted))
        count = 1
        for i in my_liste:
            print("\t{} -> {}".format(count, i))
            count +=1
        print("21 : Revenir au menu principal")
        ind = input(">")

        return ind

    def display_choice_cat(self):
        """ permits user to make a choice among 20 categories"""
        answer = None
        while answer == None:
        #loop in order to repeat the input question until an acceptable answer
            self.display_title("Choisir une catégorie")
            ind = self.input_cat_prod("catégorie", self.TUP_CATEGORY) #input for cat
            answer = self._check_answer(ind, self.TUP_CATEGORY,"Un nombre entre 1 et 21 est attendu ! ")
            input("continue ? ")
        return answer

    def _check_answer(self, ind, my_list, error_msg):
        print("ind == 21", ind == "21")
        try:

            if ind == "21":
                input("Retour au menu principal ! ")
                sys.exit()
            elif int(ind) < 21:
                return my_list[int(ind)-1]
            else:
                self.negatif_feed_back(error_msg)
                return None
        except Exception as e:
            self.negatif_feed_back("except")
            return None




class Database(Interaction):


    LIST_BIO_LABELS = ["Bio","Bio européen","FR-BIO-01","AB Agriculture Biologique", "Eco-Emballages","Organic", "EU Organic"]

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="123",
            database="python"
        )
        self.my_cursor = self.mydb.cursor()



    def _get_prod_from_cat(self, cat):
        """ returns 20 prod from db found with a given category and gather them in list """

        sql = 'select name from product where category = "{}";'.format(cat)
        self.my_cursor.execute(sql)
        my_result = self.my_cursor.fetchall()

        list_prod = []

        for tup in my_result: #permits to get str type
            for string in tup:
                if len(string) != 0:
                    list_prod.append(string)
        return list_prod

    def display_choice_prod(self, cat):
        """ permits user to make a choice among 20 categories"""

        list_prod = self._get_prod_from_cat(cat)
        while True:
        #loop in order to repeat the input question until an acceptable answer
            self.display_title("Choisir un produit")
            ind = self.input_cat_prod("produit", list_prod) #input for cat
            try :
                ind = int(ind)
                if ind == 21:
                    input("Retour au menu principal ! ")
                    return None, None, False
                elif ind < 21:
                    self.display_title("Choisir un produit")
                    return list_prod[int(ind)-1]
                else:
                    self.negatif_feed_back("Un nombre entre 1 et 21 est attendu ! ")
            except:
                self.negatif_feed_back("Un nombre entre 1 et 21 est attendu ! ")

    # *******************************************
    def _get_infos(self, cat, prod, criterion):
        """ Returns informations from db based on parameters """

        dico = {} #not precise but short name for lines 182-189
        if criterion == "1":
            sql = 'select name, additives, nutrition_grade from product where category = "{}" and'\
            ' name = "{}";'.format(cat, prod)
            self.my_cursor.execute(sql)
            my_results = self.my_cursor.fetchall()
            for mr in my_results:
                dico["name"],dico["additives"],dico["nutrition_grade"] = mr[0], mr[1], mr[2]
        else :
            sql = 'select name, labels, manufacturing_places_tags, palm_oil, nova_group '\
            'from product where category = "{}" and name = "{}";'.format(cat, prod)
            self.my_cursor.execute(sql)
            my_results = self.my_cursor.fetchall()
            for mr in my_results:
                dico["name"],dico["labels"], dico["manufacturing_places_tags"], \
                dico["palm_oil"], dico["nova_group"] = mr[0], mr[1], mr[2], mr[3],mr[4]
        return dico

    def _display_prod_info(self, info_products):
        """ Creates a tab to display infos about product """

        self.display_title("Afficher le produit")
        chain = ""
        for key in info_products:
            chain += "------"*15
            chain += "\n{} : {}\n".format(key, info_products[key])
        chain += "------"*15
        return chain

    # *******************************************GET INFOS ABOUT SEL_PROD

    def _get_NS_selected_prod(self,name_selected_prod):
        """ Returns the NS of the choosen prod """
        sql = 'select nutrition_grade from product where name = "{}";'\
            .format(name_selected_prod)
        self.my_cursor.execute(sql)
        my_result = self.my_cursor.fetchone()
        NS = my_result[0]
        return NS
    def _get_NA_selected_prod(self, name_selected_prod):
        """ Returns the len(add) of the choosen prod """
        sql = 'select nb_additives from product where name = "{}";'\
            .format(name_selected_prod)
        self.my_cursor.execute(sql)
        my_result = self.my_cursor.fetchone()
        nb_add = my_result[0]
        return nb_add
    def _get_PO_selected_prod(self, name_selected_prod):
        """ Returns True or False based on the presence of palm oil in the choosen prod """
        sql = 'select palm_oil from product where name = "{}";'\
            .format(name_selected_prod)
        self.my_cursor.execute(sql)
        my_result = self.my_cursor.fetchone()
        if my_result[0] == "0":
            return False
        else:
            return True
    def _get_MIF_selected_prod(self, name_selected_prod):
        """ Returns True or False based on the presence of palm oil in the choosen prod """
        sql = 'select manufacturing_places_tags from product where name = "{}";'\
            .format(name_selected_prod)
        self.my_cursor.execute(sql)
        my_result, substitute = self.my_cursor.fetchone(), None
        try :
            list_origin = my_result[0].split(",")
            for origin in list_origin:
                if origin in ["france","France"]:
                    substitute = name_selected_prod
                    return True
            return False
        except:
            return False
    def _get_bio_selected_prod(self, name_selected_prod):
        """ Return True if product has a bio label. """
        sql = 'select labels from product where name = "{}";'\
            .format(name_selected_prod)
        self.my_cursor.execute(sql)
        my_result, substitute = self.my_cursor.fetchone(), None
        try :
            list_label = my_result[0].split(",")
            for label in list_label:
                if label in self.LIST_BIO_LABELS:
                    return True
            return False
        except:
            return False

    # *******************************************HEALTHY FOOD

    def _find_list_low_NS(self,cat,name_selected_prod):
        """ Returns a list of prod with the lowest letter for NS
            1/ for each prod of my_results checks the NS
            2/ gets lower => the lower letter of the list
            3/ for each prod of my_results checks wether their NS == lower
            4/ appends the good ones in list_low_NS
            5/ returns list
        """
        sql = 'select name, nutrition_grade, nb_additives from product where category = "{}";'\
            .format(cat)
        self.my_cursor.execute(sql)
        my_results = self.my_cursor.fetchall()

        NS_selected_prod = self._get_NS_selected_prod(name_selected_prod)

        lower_NS = NS_selected_prod
        list_low_NS = [] #stock all the prod with a lower_NS NS

        for prod in my_results:             #1 -------------
            if prod[1]<lower_NS:
                lower_NS = prod[1]
        # input("NS_selected_prod = {}".format(NS_selected_prod))    #2 -------------

        for prod in my_results:             #3 -------------
            if prod[1] == lower_NS:
                list_low_NS.append(prod)    #4 -------------
        # print("\nVoici la liste des prod à garder :\n", list_lowest)
        return list_low_NS, lower_NS       #5 -------------

    def _compare_additives(self,my_list,lower_NS,name_selected_prod):
        """ Returns the 1st substitute present in list with the lowest number of additives (lower_NA)
            1/ for each prod checks the len(list_additives)
            2/ gets the lower len(list_additives)
            3/ returns the sub with len(list_additives) == lower
        """

        list_prod_low_nb_add, substitute, lower_NA = [], None, 100
        # print("len de my_list :", len(my_list))
        for prod in my_list:
            if prod[2] <= lower_NA:
                lower_NA = prod[2]
        # print("test lower_NA : ", lower_NA)
        for prod in my_list:
            if prod[2] == lower_NA :
                substitute = prod[0]

        # input("> substitute = {}".format(substitute))
        return substitute, lower_NS, lower_NA

    def _test_if_healthier(self, name_selected_prod,lower_NS,lower_NA):
        """ Tests if my prod is healthier than sub and returns True or False"""
        count = 0
        NS = self._get_NS_selected_prod(name_selected_prod)
        NA = self._get_NA_selected_prod(name_selected_prod)
        if NS <= lower_NS and NA <= lower_NA:
            return True,name_selected_prod, NS, NA
        else:
            return False, None, None, None

    def _find_healthy_sub(self,cat,name_selected_prod):
        """ Compares our prod with the others in its cat to perhaps return a better one for health  """

        list_low_NS, lower_NS  = self._find_list_low_NS(cat, name_selected_prod)
        substitute, lower_NS, lower_NA = self._compare_additives(list_low_NS,lower_NS,name_selected_prod)
        my_prod_healthier = self._test_if_healthier(name_selected_prod,lower_NS,lower_NA)

        if my_prod_healthier[0]:
            return True, my_prod_healthier[1], my_prod_healthier[2], my_prod_healthier[3]
        else:
            return False, substitute, lower_NS, lower_NA

    # *******************************************RESPONSIBLE FOOD
    def _get_sub_palm_oil_free(self, cat,name_selected_prod):
        """Return a palm_oil_free sub"""

        PO_in_selected_prod = self._get_PO_selected_prod(name_selected_prod)
        if PO_in_selected_prod == False:
            return "Gardez", name_selected_prod, "il est sans huile de palme."
        else:
            sql = 'select name, palm_oil from product where category = "{}";'\
                .format(cat)
            self.my_cursor.execute(sql)
            my_results, substitute = self.my_cursor.fetchall(), None

            for prod in my_results:
                if prod[1] == "0": #prod[1] = palm_oil
                    substitute = prod[0] #prod[0] = name

            if substitute:
                return "Prenez",substitute, "il est sans huile de palme."
            else:
               return None

    def _get_sub_made_in_FR(self, cat, name_selected_prod):
        """Return a Made In France (MIF) product"""
        prod_MIF = self._get_MIF_selected_prod(name_selected_prod)
        if prod_MIF:
            return "Gardez", name_selected_prod, "il est fabriqué en France."
        else:
            sql = 'select name, manufacturing_places_tags from product where category = "{}";'\
                .format(cat)
            self.my_cursor.execute(sql)
            my_results = self.my_cursor.fetchall()
            substitute = None
            for prod in my_results:
                list_origin = prod[1].split(",")
                for origin in list_origin:
                    if origin in ["france","France"]:
                        substitute = prod[0]
                        return "Prenez", substitute, "il est produit en France."
                    else:
                       return None

    def _get_sub_bio_labels(self, cat, name_selected_prod):
        """ Returns perhaps a sub with a bio label
        1/ for each product in the list
        2/ checks wether at least 1 label belongs to the list_bio_labels
        3/ if conditions are validated, appends it to list

        """
        prod_BIO = self._get_bio_selected_prod(name_selected_prod)
        if prod_BIO:
            return "Gardez", name_selected_prod, "il est fabriqué en France."
        else:
            sql = 'select name, labels from product where category = "{}";'\
                .format(cat)
            self.my_cursor.execute(sql)
            my_results = self.my_cursor.fetchall()
            for prod in my_results : #1
                list_labels = prod[1].split(",") #prod[1]=label

                for label in list_labels :
                    if label in self.LIST_BIO_LABELS:
                        substitute = prod[0] #prod[0]=name
                        return "Prenez", substitute, "il est bio ! "
            return None

    def _find_responsible_sub(self,cat,name_selected_prod):
        title = "Recherche d'un substitut à ce produit {}".format(name_selected_prod)
        self.display_title(title)
        precision = ""
        while precision not in ["1","2","3","4"]:
            precision = input("Pour cette catégorie, je vous propose 3 nouveaux critères:\n"\
        "1/ Sans Huile de Palme,\n2/ Produit en France,\n3/ Produit Bio,"\
        "\n4/ Revenir au menu principal.\n>")
            if precision == "1":
                substitute = self._get_sub_palm_oil_free(cat,name_selected_prod)
            elif precision == "2":
                substitute = self._get_sub_made_in_FR(cat, name_selected_prod)
            elif precision == "3":
                substitute = self._get_sub_bio_labels(cat, name_selected_prod)
            elif precision == "4":
                print("Retour au menu principal")
            else:
                self.negatif_feed_back("Un nombre entre 1 et 4 est attendu")
        return substitute

    # *******************************************COMPARISON
    def _display_sub_found(self, cat, name_selected_prod, criterion):
        """ Tries to find a substitute based on criterion

            for health : NutriScore(NS) and Additives
            for Environnement
        """
        self.display_title("Affichage du substitut")
        #for health
        if criterion == "1": #searches prod from cat
            ok, substitute, lower_NS, lower_NA = self._find_healthy_sub(cat, name_selected_prod)
            self.display_title("Affichage du substitut")
            if ok:
                print("\n","***"*20,"\n\nJe recommande de garder {}.\n>Il a un nutriscore de {} "\
                "et possède le moins d'additifs ({})\n dans sa catégorie ({}).".\
                format(substitute, lower_NS, lower_NA, cat),"\n\n","***"*20,)
            else:
                print("\n","***"*20,"\n\nJe recommande ce produit : {}.\n>Il a un nutriscore de {} "\
                "et possède le moins d'additifs ({})\n dans sa catégorie ({}).".\
                format(substitute, lower_NS, lower_NA, cat),"\n\n","***"*20,)

        elif criterion == "2":
            substitute = self._find_responsible_sub(cat,name_selected_prod)

            if substitute:
                print("{} ce produit {} car {}".format(substitute[0], substitute[1], substitute[2]))
            else:
                print("Aucun substitut trouvé pour cette catégorie ({}).\n"\
                    "Vous pouvez garder {}".format(cat, name_selected_prod))

    def compare_prod_with_sub(self, cat, name_selected_prod):
        """ Searchs informations about prod and compare them with other prod in the table

        1/ Lets user to choose a criterion : health / environnement
        2/ Selects a substitute according to the choice if it is possible
        3/ Displays this sub if found one

        """
        #1
        criterion = ""
        title = "Recherche d'un substitut à ce produit {}".format(name_selected_prod)
        self.display_title(title)
        while criterion not in ["1", "2"]:
            criterion = input("Je vais essayer de vous trouver un substitut à ce produit qui sera soit :\n"\
            "1) Meilleur pour votre santé,\n2) Respectueux de l'environnement.\n Que voulez-vous ?\n> ")
            if criterion not in ["1", "2"]:
                self.negatif_feed_back("Réponse attendue 1 ou 2.")
        #2
        self._display_sub_found(cat, name_selected_prod, criterion)

        #3

    # *******************************************FOR THE LOOP
    def ask_user(self):
        """ Ask the user wether he wants to make another search"""
        loop = True
        while loop:
            more_search = input("Voulez-vous faire une autre recherche ?\n"\
            "> 1/ Oui,\n> 2/ Non.")
            if more_search == "1" or more_search == "2":
                return more_search
            else:
                self.negatif_feed_back("Réponse attendue 1 ou 2")

def main():

    choice = Database()
    selected_cat = choice.display_choice_cat()
    name_selected_prod = choice.display_choice_prod(selected_cat)
    print("* * "*20)
    print("\nVous avez choisi : {} > {}\n".format(selected_cat, name_selected_prod))
    print("* * "*20)
    input("\n")
    choice.compare_prod_with_sub(selected_cat, name_selected_prod)

    #******************************************* THE LOOP
    more_search = "1"
    while more_search == "1":
        more_search = choice.ask_user()
        if more_search == "1":
            os.system("cls")
            print("...\nje choisis une autre catégorie : ")
            selected_cat = choice.display_choice_cat()
            name_selected_prod = choice.display_choice_prod(selected_cat)
            choice.compare_prod_with_sub(selected_cat, name_selected_prod)

    os.system("cls")
    print("Au revoir :)")
    sys.exit(0)



main()
