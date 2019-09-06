"""create a substitute object """

class Substitute():

    def __init__(self, name, category, label, brand, link):
        self.name = name.replace("'", "")
        self.category = category
        self.label = label.split(",")
        self.brand =brand.split(",")
        self.link = link

    def __str__(self):
        chain = "\nVoici le produit de substitution conseillé par l'app : \n\n"
        chain += "- "*30
        chain += "\n| Nom : {}\n| Categorie : {}\n| Label : {}".format(self.name, self.category, self.label)
        chain += "\n| Distributeur : {}\n| Lien : {}\n".format(self.brand, self.link)
        chain += "- "*30
        chain +=  "\n"
        return chain

