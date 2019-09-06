"""Create an object from Search, in order to give an substitute to a given product"""
import openfoodfacts
import modules.substitute as substitute

class Search():
    """class that realises the serach from a category and a product name"""

    def __init__(self, category, product_name):
        self.category = category
        self.product_name = product_name
        self.pseudo = ""
        self.substitute = self.get_substitute()

    def _improve_readability(self, word):
        """gets off all spaces and returns line to improve readability"""
        list_word = list(word)
        word = ""
        for i in list_word:
            if i == " " or i == "\n":
                continue
            word += i
        return word

    def get_substitute(self):
        """return a substitute object of a given product

            this substitute is selected according to :
                1/ a given name
                2/ a given category
                3/ a bio label
                4/ sales in France

        """

        search_result = openfoodfacts.products.advanced_search({ \
            #name
            "search_terms":self.product_name,
            #category
            "tagtype_0":"categories ",
            "tag_contains_0":"contains",
            "tag_0":self.category,
            #label
            "tagtype_1":"labels",
            "tag_contains_1":"contains",
            "tag_1":"Bio",
            #country
            "tagtype_2":"countries ",
            "tag_contains_2":"contains",
            "tag_2":"France",
            "page_size":"1"
})
        #takes the list of products
        liste_prod = search_result["products"]



        if len(liste_prod) == 0: #message if search finds nothing
            print("Nous n'avons rien trouvé")
        else :
            produit = liste_prod[0] #takes the first substitute
            label = self._improve_readability(produit["labels"])

            my_substitute = substitute.Substitute(produit["product_name_fr"], self.category, \
                label, produit["brands"], produit["url"]  )

            return my_substitute





