# autoformation à openfoodfacts

"""
    Maintenant je dois placer ces données dans la base :
        -1 tester le remplissage de la table avec un set de valeurs

"""

import openfoodfacts
import database as db

class Category():

    TUP_CATEGORIES = openfoodfacts.facets.get_categories()
    SIZE_RESEARCH = 50
    TUP_CATEGORIES = ("Jus de fruits", "Céréales", "Confiture", "Barre chocolatee",\
    "Lait", "Chips", "Bretzels", "Yaourts", "Boissons Alcoolisées", "Gâteaux", "Pains de mie", "Charcuterie",\
    "Pizzas", "Tartes salées", "Spaghetti", "Riz", "Glaces", "Chocolat noir", "Soupes") #5+7+8
    TUP_CRIT = ("product_name_fr", "labels", "additives_original_tags", "packaging_tags", "nutrition_grades",\
    "nova_group", "traces","manufacturing_places_tags","minerals_tags",\
    "ingredients_from_or_that_may_be_from_palm_oil_n","ingredients_text_with_allergens_fr"\
    ,"link", "product_quantity", "brands_tags", "nutriments")

    def __init__(self):
        self.dict_prod= self.get_categories(self.TUP_CATEGORIES)
        # self.products = self.get_products(self.categories)
        # self.twenty_fr_categories_with_20_prod = self.get_categories(self.fr_categories, self.TUP_CATEGORIES)

    def selected_crit_for_prod(self, product):
        """Takes a product and keep only crit concerning itself based on a tuple of criterions"""

        final_product = {}
        for crit in self.TUP_CRIT:
            try :
                final_product[crit] = product[crit]
            except Exception as e:
                final_product[crit] = None
        return final_product

    def fill_table(self):
        """Fills the table of a given db
            -1 connexion
            -2 requête
        """
        try:
            db_conn = db.DbConnector()
            input("connexion réussie ! =) tentative d'insertion")
            db_conn.add_substitute("name", "labels", "additives", "packagings", "a", "a", "traces", "manufacturing_places_tags", "minerals_tags", "0", "composition", "link", "100g", "brands", "nutriments")
            print("Succès")
        except Exception as e:
            raise e
        pass

    def get_categories(self, list_selected):
        """Checks wether each element of the list contains at least 20 elements,
        then returns a liste of categories with 20 prod inside """

        dico_cat = {} #create dico

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
                        liste_final_prod.append(self.selected_crit_for_prod(prod))
                dico_cat[category] = liste_final_prod
            """
            GERE AFFICHAGE DU DICO PR DEBUG
            for cat in dico_cat:
                for dictionnaire in dico_cat[cat]:
                    if len(str(dictionnaire["ingredients_text_with_allergens_fr"])) > 1500:
                        print("\t--({}) : ".format(len(str(dictionnaire["ingredients_text_with_allergens_fr"]))),dictionnaire["ingredients_text_with_allergens_fr"])
            """
            return dico_cat
        except Exception as e :
            raise e



    def get_products(self, categories):
        pass


def main():
    # print("- "*30)
    # input_answer = input("\nChoisissez une catégorie parmi la liste suivante : {}\n  >"\
    #     .format(TUP_CATEGORIES))
    # print("- "*30)
    # print("\nVous avez choisi : {}".format(TUP_CATEGORIES[int(input_answer)]))

    cat = Category()
        # len_search = len(results)
        # print(str(i+1), j, "longueur de la recherche : {}".format(len_search))


if __name__ == '__main__':
    main()
"""
 {'product_name_fr': 'Velouté de potiron à la crème fraiche',
 'additives_original_tags': [],
 'packaging_tags': ['brique', 'carton'],
 'nutrition_grades': 'c',
 'nova_group': 4,
 'traces': 'en:celery,en:eggs,en:gluten,en:mustard',
 'manufacturing_places_tags': [],
 'minerals_tags': [],
 'ingredients_from_or_that_may_be_from_palm_oil_n': 0,
 'ingredients_text_with_allergens_fr': 'Légumes 53% (potiron 29%, carotte 16%, oignon, pomme de terre, tomate), eau,<span class="allergen">crème</span> fraîche 1,6%,<span class="allergen">beurre</span>,  sel, sucre, extrait de levure, arômes (dont_<span class="allergen">lait</span>_)',
 'link': '',
 'product_quantity': 1000,
 'brands_tags': ['knorr'],
 'nutriments': {'sugars_value': '2.2', 'saturated-fat_serving': 3, 'sugars_100g': '2.2', 'nutrition-score-fr_100g': 3, 'sodium_value': '0.28', 'salt': '0.7', 'carbohydrates_value': '3.9', 'energy_100g': 159, 'nutrition-score-uk_serving': 3, 'carbohydrates': '3.9', 'fiber_100g': 1, 'sodium_100g': '0.28', 'energy': 159, 'carbohydrates_100g': '3.9', 'nutrition-score-uk': 3, 'carbon-footprint-from-known-ingredients_product': 622, 'saturated-fat_value': '1.2', 'nutrition-score-fr_serving': 3, 'fat': '1.9', 'sugars_unit': 'g', 'nova-group': 4, 'proteins_value': '0.7', 'salt_unit': 'g', 'energy_serving': 398, 'salt_100g': '0.7', 'fiber_serving': '2.5', 'fat_100g': '1.9', 'sugars': '2.2', 'proteins_serving': '1.75', 'sodium_serving': '0.7', 'saturated-fat': '1.2', 'carbohydrates_serving': '9.75', 'fat_unit': 'g', 'sodium': '0.28', 'nova-group_serving': 4, 'carbon-footprint-from-known-ingredients_100g': '62.22', 'nutrition-score-fr': 3, 'energy_unit': 'kcal', 'carbon-footprint-from-known-ingredients_serving': 156, 'fiber_value': 1, 'fat_serving': '4.75', 'carbohydrates_unit': 'g', 'saturated-fat_unit': 'g', 'saturated-fat_100g': '1.2', 'salt_serving': '1.75', 'fiber_unit': 'g', 'fiber': 1, 'nutrition-score-uk_100g': 3, 'energy_value': 38, 'proteins': '0.7', 'proteins_100g': '0.7', 'sugars_serving': '5.5', 'nova-group_100g': 4, 'sodium_unit': 'g', 'fat_value': '1.9', 'proteins_unit': 'g', 'salt_value': '0.7'}}]}
 """
