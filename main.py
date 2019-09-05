# autoformation à openfoodfacts
# pour importer la lib openfoodfact : pip install git+https://github.com/openfoodfacts/openfoodfacts-python
"""
    Maintenant je dois placer ces données dans la base :
        -1 tester le remplissage de la table avec un set de valeurs

"""

import openfoodfacts
import database as db

class Product():

    TUP_CATEGORIES = openfoodfacts.facets.get_categories()
    SIZE_RESEARCH = 50
    TUP_CATEGORIES = ("Jus de fruits", "Céréales", "Confiture", "Barre chocolatee",\
    "Lait", "Chips", "Bretzels", "Yaourts", "Boissons Alcoolisées", "Gâteaux", "Pains de mie", "Charcuterie",\
    "Pizzas", "Tartes salées", "Spaghetti", "Riz", "Glaces", "Chocolat noir", "Soupes") #5+7+8
    TUP_CRIT = ("product_name_fr", "labels", "additives_original_tags", "packaging_tags", "nutrition_grades",\
    "nova_group", "traces","manufacturing_places_tags","minerals_tags",\
    "ingredients_from_or_that_may_be_from_palm_oil_n"\
    ,"link", "product_quantity", "brands_tags", "nutriments")

    def __init__(self):
        self.dict_prod = self.get_categories(self.TUP_CATEGORIES)


    def _selected_crit_for_prod(self, product):
        """Takes a product and keep only crit concerning itself based on a tuple of criterions"""

        final_product = {}
        for crit in self.TUP_CRIT:
            try :
                final_product[crit] = product[crit]
            except Exception as e:
                final_product[crit] = None
        return final_product


    def fill_table(self, name, labels, additives, packagings,nutrition_grade, nova_group, traces, manufacturing_places_tags, minerals_tags, palm_oil, link, quantity, brands, nutriments):
        """Fills the table of a given db from DbConnector
            -1 connection
            -2 request
        """
        try:
            db_conn = db.DbConnector()

            db_conn.add_substitute(name, labels, additives, packagings,nutrition_grade, nova_group, traces, manufacturing_places_tags, minerals_tags, palm_oil, link, quantity, brands, nutriments)
        except Exception as e:
            raise e
        pass

    def get_categories(self, list_selected):
        """Checks wether each element of the list contains at least 20 elements,
        then returns a liste of categories with 20 prod inside """

        dict_prod = {} #create dico

        print("Interroge l'API ! ")
        try :
            for category in list_selected:
                # je fais ma recherche
                results = openfoodfacts.products.advanced_search({
                    "search_terms":"",
                    "tagtype_0":"categories ",
                    "tag_contains_0":"contains",
                    "tag_0": category,
                    "tagtype_1":"countries  ",
                    "tag_contains_1":"contains",
                    "tag_1":"France",
                    "page_size": self.SIZE_RESEARCH})

                liste_prod = results["products"] #keeps only the products

                liste_nom_prod = []
                liste_final_prod = []

                for prod in liste_prod: #selects prod from list of products
                    nom_prod = prod["product_name_fr"]
                    if nom_prod not in liste_nom_prod and len(liste_nom_prod) < 20: #anti-duplicate
                        liste_nom_prod.append(nom_prod)
                        liste_final_prod.append(self._selected_crit_for_prod(prod))
                dict_prod[category] = liste_final_prod
            return dict_prod
        except Exception as e :
            raise e



    def get_products(self, categories):
        pass


def main():
    prod = Product()
    ajout = 0
    for category in prod.dict_prod:
        for product in prod.dict_prod[category]:
            name = product["product_name_fr"]
            labels = product["labels"]
            additives = product["additives_original_tags"]
            packagings = product["packaging_tags"]
            nutrition_grade = product["nutrition_grades"]
            nova_group = product["nova_group"]
            traces = product["traces"]
            manufacturing_places_tags = product["manufacturing_places_tags"]
            minerals_tags = product["minerals_tags"]
            palm_oil = product["ingredients_from_or_that_may_be_from_palm_oil_n"]
            link = product["link"]
            quantity = product["product_quantity"]
            brands = product["brands_tags"]
            nutriments = product["nutriments"]

            try:

                prod.fill_table(name, labels, additives, packagings,nutrition_grade, nova_group, traces, manufacturing_places_tags, minerals_tags, palm_oil, link, quantity, brands, nutriments)
                ajout += 1
            except Exception as e:
                ajout -= 1
                print("- - "*50)
                print(name, len(traces), traces)
                print("- - "*50)
                raise e

    print("ligne écrites = {}".format(ajout))

if __name__ == '__main__':
    main()
