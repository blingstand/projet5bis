""" This script contains the database object and all methodes it needs"""

import os
import time
import mysql.connector
import modules.substitute as sub


def negatif_feed_back(msg):
    """ display a negative feed_back message and let 1sec to read it """
    print("\n", msg, "\n")
    time.sleep(1)

class DbConnector():
    """class that manage the connection to the database and the fonction related to db"""

    COLUMNS = 'name, labels, additives, packagings,nutrition_grade, nova_group, traces, manufacturing_places_tags,\
    minerals_tags, palm_oil, composition, link, quantity, brands, nutriments'

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="123",
            database="python",
            auth_plugin='mysql_native_password'
        )
        self.my_cursor = self.mydb.cursor()

    def add_substitute(self, name, labels, additives, packagings,nutrition_grade, nova_group, traces, manufacturing_places_tags, minerals_tags, palm_oil, composition, link, quantity, brands, nutriments):
        """
        Inserts a line in the table product
        """
        sql = 'INSERT INTO Product ({})'\
        'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}",'\
        ' "{}", "{}");'.format(self.COLUMNS, name, labels, additives, packagings,nutrition_grade, nova_group, traces, \
        manufacturing_places_tags, minerals_tags, palm_oil, composition, link, quantity, brands, nutriments)
        input(sql)
        try:
            self.my_cursor.execute(sql)
            self.mydb.commit() #has to commit the change
            print("-- db good.")
        except Exception as e:
            raise e



    def inscription(self, user):
        """ checks whether the pseudo is available :
                if yes creates account,
                if not offers 3 possibilities (connection with these id, start again, exit)  ."""
        if user.pseudo == "":
            user.pseudo = input("\n  Pseudo : ")
            user.password = input("  Mot de passe : ")

        while True:
            # manage the no answer situation
            if user.pseudo == "":
                negatif_feed_back("Fournissez un pseudo !")
                user.pseudo = input("\n  Pseudo : ")
                continue
            if user.password == "":
                negatif_feed_back("Fournissez un mot de passe !")
                user.password = input("  Mot de passe : ")
                continue

            #try is a necessity here to manage the mysql error if the value already exists
            try:
                sql = "INSERT INTO User (pseudo, password) "\
                " VALUES ('{}','{}');".format(user.pseudo, user.password)
                self.my_cursor.execute(sql)
                self.mydb.commit()
                user.connected = True

                #app will need user.id later
                sql = "SELECT id from User WHERE pseudo = '{}'".format(user.pseudo)
                self.my_cursor.execute(sql)
                user_id = self.my_cursor.fetchone()
                user.id = user_id[0]
                return user

            except mysql.connector.errors.IntegrityError:
                # raise e    #for the debug
                print("\nCet identifiant n'est pas disponible :(")

                #Manage the input after no working id, offers 3 possibilities
                while True:
                    answer = input("Peut-être voulez-vous :"\
                        "\n1/ Vous authentifier avec ces identifiants,"\
                        "\n2/ Essayer de nouveau,\n3/ Abandonner.\n ->")

                    if answer == "1":
                        #tries a connection with these id
                        user = self.connection(user)
                        return user
                    elif answer == "2":
                        #tries again
                        break
                    elif answer == "3":
                        #exits the inscription function
                        user.connected = "Exit"
                        return user
                    else:
                        negatif_feed_back("Je n'ai pas compris.")
                        continue
            user.pseudo = input("\n  Pseudo : ")
            user.password = input("  Mot de passe : ")

    def connection(self, user):
        """ checks whether the pseudo is present in the user table.
            if yes creates checks whether the password
                from user table is the same than user.password,
            if not offers 3 possibilities
                (inscription with these id, start again, exit)  ."""
        if user.pseudo == "":
            user.pseudo = input("\n  Pseudo : ")
            user.password = input("  Mot de passe : ")

        while True:

            #no need to use the try expression
            sql = "SELECT password FROM user WHERE pseudo = '{}';".format(user.pseudo)
            self.my_cursor.execute(sql)
            resultat = self.my_cursor.fetchone()
            #resultat can be empty or not
            if resultat:
                if resultat[0] == user.password:
                    user.connected = True
                    #app will need user.id later
                    sql = "SELECT id from User WHERE pseudo = '{}';".format(user.pseudo)
                    self.my_cursor.execute(sql)
                    user_id = self.my_cursor.fetchone()
                    user.id = user_id[0]
                    return user
                else:
                    print("\nMot de passe incorrect ! ")
            else:
                print("\nPseudo inconnu : {} ".format(user.pseudo))

            #if user is not returned start the loop
            while True:
                answer = input("Peut-être voulez-vous :\n1/ Vous inscrire avec ces identifiants,"\
                "\n2/ Essayer de nouveau,\n3/ Abandonner.\n ->")

                if answer == "1":
                    #tries to subscribe with these id
                    user = self.inscription(user)
                    return user
                elif answer == "2":
                    #tries again with new id
                    break
                elif answer == "3":
                    #exits the connection function
                    user.connected = "Exit"
                    return user
                else:
                    negatif_feed_back("Je n'ai pas compris.")
                    continue
            user.pseudo = input("\n  Pseudo : ")
            user.password = input("  Mot de passe : ")

    def authentication(self, user):
        """ connectes a user if user.connected is False

            Therefore it calls inscription() or connection(),
            depending on the user answer to the input.
            Permits also to get user.id (for the next sql querries will be usefull)
        """

        while not user.connected:
            os.system("cls")
            print("\n", "-"*30, " PAGE D'AUTHENTIFICATION ", "-"*30, "\n")

            #the question
            new = input("Il faut vous connecter : \n  1 - Inscription,\n "\
                " 2 - Connexion,\n  3 - Quitter,\n ->")

            #condition
            if new in ("1", ""):
                os.system("cls")
                print("\n", "-"*30, " PAGE D'AUTHENTIFICATION ", "-"*30, "\n")
                print("- - - - Inscription - - - -")
                user = self.inscription(user)
                #to manage the exit option and remain user.connected False
                if user.connected == "Exit":
                    user.connected = False
                    break

            elif new == "2":
                os.system("cls")
                print("\n", "-"*30, " PAGE D'AUTHENTIFICATION ", "-"*30, "\n")
                print("- - - - Connexion - - - -")
                user = self.connection(user)
                if user.connected == "Exit":
                    user.connected = False
                    break

            elif new == "3":
                break

            else:
                negatif_feed_back("Il faut donner comme réponse oui ou non !")

        return user

    def add_data_in_db(self, substitute, search, user):
        """ Checks whether user_id is in search where the
        id of Substitute.name(table) = substitute.name(object attribut)
            3 different cases managed by a try expression :
                1/ the querry works ...
                    1.a and the id is present
                        -> functiondoes nothing
                    1.b and the id is absent
                        -> function adds a line in search
                2/ the querry raises error
                (because no id for this substitute, so no substitute in table)
                    -> function has to add it
         """

        #checks the db
        sql = "SELECT user_id FROM Search WHERE substitute_id = "\
            "(SELECT id FROM Substitute WHERE name = '{}');".format(substitute.name)
        self.my_cursor.execute(sql)
        id_found = self.my_cursor.fetchall()
        id_present = False
        try: # 1/ ...
            for i in id_found:

                if user.id == i[0]: #this can raise an error
                    id_present = True
                    break

            if id_present: # 1.a
                input("\nCette recherche est déjà présente dans votre table ! ")

            elif not id_present:# 1.b
                #adds a day_date for the next function history
                sql = 'INSERT INTO Search (user_id, substitute_id,'\
                ' day_date, category, product_name) VALUES ('\
                '"{}",(SELECT id FROM Substitute WHERE name = "{}"), '\
                ' NOW(), "{}", "{}");'.format(user.id, substitute.name,\
                 substitute.category, search.product_name)
                self.my_cursor.execute(sql)
                self.mydb.commit() #has to commit the change
                input("\nCette recherche a été ajoutée à votre table.")

        except mysql.connector.errors.IntegrityError: # 2/ ...
            #add name, cat, link only if this sub is not in database
            sql = 'INSERT INTO Substitute(name, category, link)'\
            'VALUES("{}","{}","{}");'.format(substitute.name, \
                substitute.category, substitute.link)
            self.my_cursor.execute(sql)
            self.mydb.commit()


            #add label, I can have numerous label, so I need to add it one by one
            for i in substitute.label:
                if i[0] == " ": #del annoying first character "space"
                    i = i[1:]
                sql = 'INSERT INTO Label (substitute_id, name) VALUES '\
                ' ((SELECT id FROM Substitute WHERE name = "{}"), "{}");'\
                .format(substitute.name, i)

                self.my_cursor.execute(sql)
                self.mydb.commit()

            #add brand,it can have numerous brand, so function needs to add it one by one
            for i in substitute.brand:
                if i[0] == " ": #del annoying first character "space"
                    i = i[1:]

                sql = 'INSERT INTO Brand (substitute_id, name) VALUES ( '\
                '(SELECT id FROM Substitute WHERE name = "{}"), "{}");'\
                .format(substitute.name, i)
                self.my_cursor.execute(sql)
                self.mydb.commit()


            #add in search
            sql = 'INSERT INTO Search (user_id, substitute_id,'\
            ' day_date, category, product_name) VALUES ('\
            '"{}",(SELECT id FROM Substitute WHERE name = "{}"), '\
            'NOW(), "{}", "{}");'.format(user.id, substitute.name, \
                substitute.category, search.product_name)

            self.my_cursor.execute(sql)
            self.mydb.commit()

            input("\nLe substitut a été ajouté à votre base de données.")

    def history(self, user):
        """ Permits to display the previous search.name connected to a given pseudo """

        os.system("cls")
        print("\n", "-"*30, " PAGE DE L'HISTORIQUE DE RECHERCHE ", "-"*30, "\n")
        print("Voici les précédentes recherches que vous avez effectuées : \n")

        sql = "SELECT substitute_id, " \
        "DATE_FORMAT(day_date, '%e/%m/%y - %k:%i:%s') as 'date',product_name "\
        "FROM Search WHERE user_id = '{}' "\
        "ORDER BY 'date' DESC;".format(user.id)
        self.my_cursor.execute(sql)
        resultat = self.my_cursor.fetchall()

        print("- "*35)
        print("  substitute_id  | date \t\t | substitut")
        print("- "*35)
        for i in resultat:
            print("  {} \t\t | {} \t | {} ".format(i[0], i[1], i[2]))
        print("- "*35)

        input("Appuyer sur entrer pour continuer.")

    def get_more_info(self, user):
        """User chooses a prod or a sub and give 1 word (or more), functions makes a search"""
        os.system("cls")
        print("\n", "-"*20, " PAGE D'AFFICHAGE DE LA FICHE D'UN SUBSTITUT ", "-"*20, "\n")
        while True:
            given_word = input("\nDonnez moi un élément pour la recherche :\n ->")

            sql = 'SELECT Substitute.name, Substitute.category, '\
            'GROUP_CONCAT(Label.name),GROUP_CONCAT(Brand.name),Substitute.link FROM Substitute '\
            'INNER JOIN Search ON Search.substitute_id = Substitute.id '\
            'INNER JOIN Label ON Label.substitute_id = Substitute.id '\
            'INNER JOIN Brand ON Brand.substitute_id = Substitute.id '\
            'WHERE Search.user_id = {} AND Substitute.name LIKE "%{}%";'.format(user.id, given_word)

            try: #necessary because resultat[0] can raise an error
                resultat = self.my_cursor.execute(sql)
                resultat = self.my_cursor.fetchall()
                tup = resultat[0]
                sheet = sub.Substitute(tup[0], tup[1], tup[2], tup[3], tup[4])
                input("{} \nTouche 'entrer' pour continuer".format(sheet))
                return True

            except:
                while True:
                    action = input("\n---------- Erreur ----------\nLa recherche n'a rien donné."\
                        " Vous devriez vérifier revenir au menu pour vérifier votre "\
                        "historique de recherche.\n"\
                        "Que voulez-vous faire ?\n"\
                        "  1 - Donner un autre mot,\n"\
                        "  2 - Revenir au ménu principal. \n")
                    if action == "1":
                        break
                    elif action == "2":
                        return True
                    else:
                        print("Je n'ai pas compris ! ")
