"""Welome to the fifth project

    In this projet, I permit to my user to change their mind on food.
    I want to make them discover that for each product they have the same product
    with a label "bio". Respecting environnement is possible.
"""
import os
import sys
import find_sub as fd
import modules.user as us
import modules.database as db


#################################################################### main
def main():
    """ execute all the actions """
    os.system("cls")
    # input("\n\tBienvenu dans l'application Pur Beurre. Cette application a pour fonction"\
    # " de vous montrer que parmi des produits du quotidien vous pouvez trouver un "\
    # "substitut dont la fabrication est respectueuse de l'environnement.\n")

    my_user = us.User()
    loop = True
    while loop:
        os.system("cls")
        print("\n", "-"*30, " PAGE D'ACCUEIL ", "-"*30, "\n")
        if my_user.connected:
            print("Vous êtes connecté(e) en tant que : {}.".format(my_user.pseudo))
            answer = input("\nQue voulez-vous faire ?\n"\
                "  1 - Me déconnecter\n"\
                "  2 - Trouver un substitut, \n"\
                "  3 - Consulter votre base de données,\n"\
                "  4 - Quitter.\n ->")
        else:
            print("Vous n'êtes pas connecté(e).")
            my_user.pseudo = ""
            my_user.password = ""

            answer = input("\nQue voulez-vous faire ? "\
                " (Par exemple : Taper '1' et entrer pour vous connecter) \n"\
                "  1 - Me connecter, \n"\
                "  2 - Trouver un substitut, \n"\
                "  3 - Consulter votre base de données,\n"\
                "  4 - Quitter.\n ->")
##################################################################################### 1
        if answer == "1":
            #depend on my_user.connected
            if my_user.connected:
                my_user.connected = False
                my_user.pseudo = ""
                my_user.password = ""
            else:
                my_db = db.DbConnector()
                my_user = my_db.authentication(my_user)

##################################################################################### 2
        elif answer == "2":
            # my_user.connected = True
            # my_user.pseudo = "anna"
            # my_user.password = "123"
            # my_user.id = "2"
            #find_substitute has to find a substitute from a given product
            my_substitute, my_search, save_data = fd.main()
            #it returns an object substitute, search and save_data (True or False)

            if save_data:
                my_db = db.DbConnector()
                my_user = my_db.authentication(my_user)
                my_db.add_data_in_db(my_substitute, my_search, my_user)

##################################################################################### 3

        elif answer == "3":
            my_db = db.DbConnector()

            my_user = my_db.authentication(my_user)
            #consult_database permit to the user to access the database
            os.system("cls")
            print("\n", "-"*30, " BASE DE DONNEES ", "-"*30, "\n")
            loop2 = True #loop already exists
            while loop2:
                action = input("\nQue voulez-vous faire ?\n"\
                    "  1 - Consulter l'historique de recherche,\n"\
                    "  2 - Afficher la fiche info d'un substitut choisi,\n"\
                    "  3 - Quitter.\n ->")
                if action == "1":
                    my_db.history(my_user)
                    loop2 = False
                elif action == "2":
                    my_db.get_more_info(my_user)
                    loop2 = False
                elif action == "3":
                    loop2 = False
                else:
                    input("Je n'ai pas compris.")


##################################################################################### 4
        elif answer == "4":
            print("A bientôt !")
            sys.exit(2)
        else:
            print("Je n'ai pas compris.")

if __name__ == '__main__':
    main()

# my_user.pseudo = "adi"
# my_user.password = "123"
# my_user.connected = True
# my_user.id = "1"
