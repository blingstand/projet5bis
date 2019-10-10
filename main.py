#pb : recherche/idtf_refusé -> peut quand même rechercher
#pb : histo/idtf_refusé -> peut quand même rechercher
"""Welome to the fifth project

    In this projet, I permit to my user to change their mind on food.
    I want to make them discover that for each product they have the same product
    with a label "bio". Respecting environnement is possible.
"""
import os, sys, webbrowser, time

import modules.user as us
import modules.database as db
import modules.db_users as dbu


#################################################################### main
def main():
    """ execute all the actions """
    os.system("cls")
    # input("\n\tBienvenu dans l'application Pur Beurre. Cette application a pour fonction"\
    # " de vous montrer que parmi des produits du quotidien vous pouvez trouver un "\
    # "substitut dont la fabrication est respectueuse de l'environnement.\n")

    my_user = us.User("adi", "123", True)
    # input(my_user.id)
    loop = True
    while loop:
        os.system("cls")
        print("\n", "-"*30, " PAGE D'ACCUEIL ", "-"*30, "\n")
        if my_user.connected:
            print("Vous êtes connecté(e) en tant que : {}.".format(my_user.pseudo))
            answer = input("\nQue voulez-vous faire ?\n"\
                "  1 - Me déconnecter\n"\
                "  2 - Remplacer un aliment, \n"\
                "  3 - Retrouver mes aliments substitués,\n"\
                "  4 - Quitter.\n ->")
        else:
            print("Vous n'êtes pas connecté(e).")
            my_user.pseudo = ""
            my_user.password = ""

            answer = input("\nQue voulez-vous faire ? "\
                " (Par exemple : Taper '1' et entrer pour vous connecter) \n"\
                "  1 - Me connecter, \n"\
                "  2 - Remplacer un aliment, \n"\
                "  3 - Retrouver mes aliments substitués,\n"\
                "  4 - Quitter.\n ->")
##################################################################################### 1
        if answer == "1":
            #depend on my_user.connected
            if my_user.connected:
                my_user.connected = False
                my_user.pseudo = ""
                my_user.password = ""
            else:
                my_db = dbu.DbUser()
                my_user = my_db.authentication(my_user)

##################################################################################### 2
        elif answer == "2":
            if not my_user.connected:
                my_db = dbu.DbUser()
                my_user = my_db.authentication(my_user)
            if not my_user.connected:
                print("Retour au menu principal ! ")
                time.sleep(1)
                continue
            loop = True
            while loop:
                choice = db.Database()
                selected_cat = choice.display_choice_cat()
                if selected_cat == "menu":
                    break
                selected_prod = choice.display_choice_prod(selected_cat)
                if selected_prod == "menu":
                    break
                stop = choice.compare_prod_with_sub(selected_cat, selected_prod, my_user)
                if stop == "menu":
                    break
                after_search = choice.after_search("3")
                if after_search == "1":
                    url = choice.display_more_info_about_product(selected_prod)
                    webbrowser.open_new(url)
                    after_web = choice.after_search("2")
                    if after_web == "2":
                        break
                elif after_search == "2":
                    pass
                elif after_search == "3":
                    break
                else:
                    break


##################################################################################### 3

        elif answer == "3":
            my_db = dbu.DbUser()
            if not my_user.connected:
                my_user = my_db.authentication(my_user)
            if not my_user.connected:
                print("Retour au menu principal ! ")
                time.sleep(1)
                continue
            #consult_database permit to the user to access the database
            os.system("cls")
            print("\n", "-"*30, " BASE DE DONNEES ", "-"*30, "\n")
            chain = my_db.history(my_user)
            print(chain)
            input("Appuyez sur 'entrer' pour revenir au menu principal.")


##################################################################################### 4
        elif answer == "4":
            print("A bientôt !")
            time.sleep(1)
            os.system("cls")
            sys.exit(2)
        else:
            print("Je n'ai pas compris.")

if __name__ == '__main__':
    main()

# my_user.pseudo = "adi"
# my_user.password = "123"
# my_user.connected = True
# my_user.id = "1"
