import sys
import math
import random
import threading
import urllib.request
import urllib.parse
import io
import pygame

# ==============================================================================
# BASE DE DONNÉES COMPLÈTE DES 50 PERSONNAGES
# ==============================================================================
CHARACTERS_DATA = {
    "Dieu": {
        "subtitles": ["Le Créateur Omniscient", "L'Architecte Céleste", "La Lumière Primordiale", "L'Arbitre de l'Infini"],
        "weapons": ["Le Verbe Divin", "Rayon d'Énergie Cosmique", "La Foudre Primordiale"],
        "ultimates": ["Genèse Instantanée", "Omnipotence Absolue", "Remise à Zéro de l'Univers"],
        "lores": [
            "Existant avant le néant, il observe les milliards d'étoiles naître et s'éteindre.",
            "D'une infinie bienveillance ou d'une impartialité absolue, son souffle régit la matière."
        ]
    },
    "Goku": {
        "subtitles": ["Le Guerrier Saiyan", "Défenseur de la Terre", "Maître des Dieux", "L'Innocent Bagarreur"],
        "weapons": ["Bâton Magique Nyoibo", "Nuage Magique Kinto-un", "Poings Renforcés de Ki"],
        "ultimates": ["Genkidama Universelle", "Kaméhaméha Divin", "Ultra Instinct Maîtrisé"],
        "lores": [
            "Envoyé sur Terre pour la détruire, un choc à la tête fit de lui son plus féroce gardien.",
            "Repoussant sans cesse ses limites physiques, il ne vit que pour affronter des rivaux légendaires."
        ]
    },
    "Batman": {
        "subtitles": ["Le Chevalier Noir", "Le Détective Suprême", "Le Justicier de l'Ombre", "L'Ombre de Gotham"],
        "weapons": ["Batarangs Explosifs", "Grappin Tactique", "Gantelets Renforcés"],
        "ultimates": ["Protocole Contingence", "Attaque de la Batmobile", "Disparition dans les Ténèbres"],
        "lores": [
            "Orphelin suite à une tragédie dans une ruelle sombre, il a juré d'éradiquer la peur par la peur.",
            "Dépourvu de super-pouvoirs, son intellect stratégique et sa fortune font plier les dieux."
        ]
    },
    "Naruto": {
        "subtitles": ["L'Enfant de la Prophétie", "L'Hôte de Kyûbi", "Le Septième Hokage", "L'Éternel Farceur"],
        "weapons": ["Kunai de l'Éclair Volant", "Shurikens Géants", "Rouleau de Sceaux"],
        "ultimates": ["Rasenshuriken Planétaire", "Mode Ermite d'Ashura", "Bijuu Dama Suprême"],
        "lores": [
            "Rejeté par tout son village, sa persévérance indomptable l'a propulsé au sommet du monde shinobi.",
            "Lié au puissant démon renard, il a transformé la haine en un lien d'amitié indestructible."
        ]
    },
    "Darth Vader": {
        "subtitles": ["Le Seigneur Sith", "L'Élu Déchu", "Le Poing de l'Empereur", "La Machine Inflexible"],
        "weapons": ["Sabre Laser Écarlate", "Choke Télékinétique", "Chasseur TIE Avancé"],
        "ultimates": ["Tempête de la Force Noire", "Écrasement Stellaire", "Rage du Côté Obscur"],
        "lores": [
            "Ancien prodige Jedi, corrompu par la peur de perdre l'amour, il est devenu le bourreau de la galaxie.",
            "Prisonnier d'une armure cybernétique respirante, sa seule présence glace le sang des rebelles."
        ]
    },
    "Spider-Man": {
        "subtitles": ["Le Tisseur Sympathique", "L'Araignée Masquée", "Le Prodige de New York", "L'Acrobate Vengeur"],
        "weapons": ["Lance-Toiles Web-Shooters", "Drones Araignées", "Toile Électrifiée"],
        "ultimates": ["Impact de Toile Maximal", "Sens d'Araignée Total", "Assaut Acrobatique 360°"],
        "lores": [
            "Mordu par une araignée radioactive, il apprit qu'un grand pouvoir implique de grandes responsabilités.",
            "Toujours prompt à lâcher un bon mot, il protège les innocents au détriment de sa propre vie privée."
        ]
    },
    "Thor": {
        "subtitles": ["Le Dieu du Tonnerre", "Le Prince d'Asgard", "Le Protecteur de Midgard", "Le Vengeur Cosmique"],
        "weapons": ["Mjolnir le Marteau Sacré", "Stormbreaker la Hache Briseuse", "Ceinture de Force Megingjord"],
        "ultimates": ["Frappe du Tonnerre Primordial", "Invocation du Bifröst", "Fureur d'Odin"],
        "lores": [
            "Fils aîné d'Odin, son arrogance de jeunesse a cédé la place à une noblesse héroïque sans faille.",
            "Il sillonne les neuf royaumes en déchaînant les éclairs pour terrasser les géants de glace."
        ]
    },
    "Kratos": {
        "subtitles": ["Le Fantôme de Sparte", "Le Tueur de Panthéons", "Le Père Sévère", "Le Destructeur Inarrêtable"],
        "weapons": ["Lames du Chaos", "Hache Léviathan", "Bouclier du Gardien"],
        "ultimates": ["Rage Spartiate", "Éruption du Chaos", "Fureur Glaciaire"],
        "lores": [
            "Trompé par Arès, la peau blanchie par les cendres de sa famille, il anéantit l'Olympe tout entier.",
            "Réfugié dans le grand Nord, il tente d'échapper à sa nature sanguinaire pour élever son fils."
        ]
    },
    "Harry Potter": {
        "subtitles": ["Le Survivant", "L'Attrapeur Émérite", "Le Maître de la Mort", "L'Élève Rebelle"],
        "weapons": ["Baguette de Houx et Plume de Phénix", "Cape d'Invisibilité", "Épée de Gryffondor"],
        "ultimates": ["Expelliarmus Suprême", "Patronus Cerf Lumineux", "Lien Sacré des Âmes"],
        "lores": [
            "Bébé marqué d'un éclair, il a survécu au mal absolu grâce au sacrifice d'une mère.",
            "À travers les dédales de Poudlard, il a mené ses camarades jusqu'au combat final pour la liberté."
        ]
    },
    "Gandalf": {
        "subtitles": ["Le Pèlerin Gris", "Le Cavalier Blanc", "Le Fléau du Balrog", "L'Émissaire d'Illuvatar"],
        "weapons": ["Glamdring l'Épée Féerique", "Bâton de Pouvoir Lumineux", "Anneau de Feu Narya"],
        "ultimates": ["Vous ne passerez pas !", "Aube Aveuglante d'Olorin", "Pulsation Mystique"],
        "lores": [
            "Envoyé sur la Terre du Milieu sous les traits d'un vieillard, son esprit abrite un pouvoir angélique.",
            "Stratège des peuples libres, il guida l'Anneau Unique au cœur de la montagne du Destin."
        ]
    },
    "Thanos": {
        "subtitles": ["Le Titan Fou", "Le Conquérant Implacable", "Le Chercheur d'Équilibre", "Le Fléau Cosmique"],
        "weapons": ["Gant de l'Infini", "Épée à Double Tranchant", "Armure Titanienne"],
        "ultimates": ["Le Claquement de Doigts", "Pluie de Météores Astrale", "Rayon d'Énergie Cosmique"],
        "lores": [
            "Témoin de l'effondrement de sa planète natale, il a juré de rééquilibrer le cosmos par la force brute.",
            "Inflexible et méthodique, il sacrifie tout sans sourciller pour accomplir son grand dessein."
        ]
    },
    "Superman": {
        "subtitles": ["L'Homme d'Acier", "Le Dernier Fils de Krypton", "Le Symbole d'Espoir", "Le Champion Métropolitain"],
        "weapons": ["Rayons Thermiques Oculaires", "Souffle Glacial", "Poings Solaires"],
        "ultimates": ["Impact Solaire Orbital", "Super-Éruption Thermique", "Vol Transsonique Écrasant"],
        "lores": [
            "Sauvé in extremis d'un monde mourant, il a grandi au Kansas avec des valeurs morales inébranlables.",
            "Nourri par les rayons de notre soleil jaune, il est le bouclier indestructible de l'humanité."
        ]
    },
    "Luffy": {
        "subtitles": ["Le Chapeau de Paille", "Le Garçon Élastique", "L'Affranchi des Mers", "Le Cinquième Empereur"],
        "weapons": ["Gomu Gomu Poings", "Tuyau en Fer d'Enfance", "Chapeau Indestructible"],
        "ultimates": ["Gear 5 - Dieu du Soleil Nika", "Bajrang Gun Colossal", "Gomu Gomu King Kong Gun"],
        "lores": [
            "Ayant mangé par mégarde un fruit démoniaque, il écume Grand Line en quête du trésor absolu.",
            "Son rire retentit sur les océans, libérant les peuples opprimés sous la bannière du crâne au chapeau."
        ]
    },
    "Saitama": {
        "subtitles": ["Le Chauve Héroïque", "Le Justicier pour le Plaisir", "Le Maître du One-Punch", "L'Exterminateur de Monstres"],
        "weapons": ["Gants de Vaisselle Rouges", "Sacs de Courses en Plastique", "Botte de Cuir Blindée"],
        "ultimates": ["Coup de Poing Sérieux", "Table Flip Omnidirectionnel", "Éternuement Gravitationnel"],
        "lores": [
            "À force de 100 pompes, 100 abdos et 10km quotidiens, il a brisé toutes les barrières biologiques.",
            "Lassé de triompher en un coup sans le moindre effort, il rêve secrètement d'un véritable défi."
        ]
    },
    "Pikachu": {
        "subtitles": ["La Souris Électrique", "La Mascotte Éclair", "Le Vétéran de Kanto", "L'Ami Loyal"],
        "weapons": ["Queue d'Acier Tranchante", "Balle Électro Magnétique", "Orbe Foudre"],
        "ultimates": ["Fatal-Foudre Gigavolt", "Électacle Foudroyant", "Danse du Tonnerre Z"],
        "lores": [
            "Compagnon obstiné d'un jeune dresseur, il a bravé les ligues et défait des créatures légendaires.",
            "Ses joues cramoisies accumulent une énergie statique capable de paralyser les plus féroces assaillants."
        ]
    },
    "Mario": {
        "subtitles": ["Le Plombier Moustachu", "Le Héros du Royaume Champignon", "Le Sauteur Émérite", "Le Superstar"],
        "weapons": ["Marteau en Acier Rustique", "Fleur de Feu Stellaire", "Super Étoile d'Invincibilité"],
        "ultimates": ["Super Slam Météorique", "Tornade Enflammée", "Barrage de Carapaces Bleues"],
        "lores": [
            "Plombier de quartier propulsé dans un monde féerique, il défie châteaux et volcans pour sauver la princesse.",
            "Du volant d'un kart aux étoiles lointaines de la galaxie, son courage sans égal ne faiblit jamais."
        ]
    },
    "Sonic": {
        "subtitles": ["L'Éclair Bleu", "Le Hérisson le Plus Rapide", "Le Briseur de Mach 3", "Le Vent de la Liberté"],
        "weapons": ["Anneaux Téléporteurs Dorés", "Baskets Power Sneakers", "Spin Dash Tranchant"],
        "ultimates": ["Super Sonic aux Chaos Emeralds", "Sonic Boom Hyper-Vitesse", "Light Speed Attack"],
        "lores": [
            "Né pour courir à des vitesses supersoniques, il fait tourner en bourrique le Dr Robotnik à chaque aube.",
            "Farouche défenseur de la faune et de la nature, rien ne peut enfermer sa fougue intrépide."
        ]
    },
    "Zelda/Link": {
        "subtitles": ["Le Héros du Temps", "Le Porteur de la Triforce", "Le Prodige d'Hyrule", "Le Chevalier Muet"],
        "weapons": ["Épée de Légende (Master Sword)", "Bouclier Hylien Antique", "Arc de Lumière Sacré"],
        "ultimates": ["Attaque Tourbillon Sacrée", "Colère d'Urbosa", "Flèche Stellaire Purificatrice"],
        "lores": [
            "Réincarnation éternelle du courage face au mal séculaire, il s'éveille dès qu'Hyrule sombre.",
            "De temple en sanctuaire, il surmonte chaque épreuve pour briser le sceau des ombres de Ganon."
        ]
    },
    "Shrek": {
        "subtitles": ["L'Ogre du Marais", "Le Monstre au Grand Cœur", "Le Champion des Oignons", "La Terreur Verte"],
        "weapons": ["Tronc d'Arbre Brut", "Gaz Maraîcher Toxique", "Poing Bourru en Boue"],
        "ultimates": ["Rugissement Briseur de Tympans", "Plongeon Bourbier Sismique", "Assaut des Créatures du Marais"],
        "lores": [
            "Il ne demandait qu'une paix tranquille dans sa tourbière, avant qu'un âne bavard ne change son existence.",
            "Sous ses couches rugueuses comme un oignon se cache l'âme la plus loyale de Fort Fort Lointain."
        ]
    },
    "Jack Sparrow": {
        "subtitles": ["Le Capitaine Maudit", "Le Flibustier Insaisissable", "Le Maître du Black Pearl", "Le Pirate Imprévisible"],
        "weapons": ["Sabre de Bord Ébréché", "Pistolet à Silex Unique", "Compas Mystique de Calypso"],
        "ultimates": ["Évasion Miraculeuse", "Tir d'Élite Bordée de Canons", "Feinte du Mort-Vivant"],
        "lores": [
            "Démarche chaloupée et bouteille de rhum à la main, nul ne sait s'il est un génie ou un parfait imbécile.",
            "Il a défié le Kraken, trompé Davy Jones et négocié avec la mort pour conserver son chapeau."
        ]
    },
    "Sherlock Holmes": {
        "subtitles": ["L'Esprit Déductif", "L'Enquêteur de Baker Street", "Le Maître du Bartitsu", "L'Ombre de Moriarty"],
        "weapons": ["Canne-Épée en Bois Rare", "Revolver Webley", "Loupe d'Analyse Millimétrée"],
        "ultimates": ["Désarmement Calculé (Discombobulate)", "Déduction Analytique Fatale", "Piège Méticuleux"],
        "lores": [
            "Capable de reconstituer un crime à partir d'une simple trace de cendre sur un tapis londonien.",
            "Son cerveau carbure à une cadence infernale, méprisant la sottise pour traquer la logique pure."
        ]
    },
    "Hercule": {
        "subtitles": ["Le Demi-Dieu Olympien", "Le Vainqueur des Douze Travaux", "La Force Invincible", "Le Champion de Zeus"],
        "weapons": ["Massue en Bois d'Olivier", "Peau du Lion de Némée", "Arc et Flèches Empoisonnées de l'Hydre"],
        "ultimates": ["Fissure Sismique d'Atlas", "Coup de Poing Olympien", "Fureur Héracléenne"],
        "lores": [
            "Nourri d'exploits mythiques, il a étranglé des serpents au berceau et dompté les bêtes du Tartare.",
            "Rachetant ses fautes par des labeurs colossaux, il s'est taillé une place parmi les immortels."
        ]
    },
    "Dracula": {
        "subtitles": ["Le Seigneur des Carpates", "Le Premier Nosferatu", "L'Empereur de la Nuit", "Le Buveur d'Âmes"],
        "weapons": ["Griffes Vampiriques Acérées", "Rapière d'Ombre Sanguine", "Nuée de Chauves-Souris"],
        "ultimates": ["Festin de Sang Nocturne", "Brume Démoniaque Évanescente", "Éclipse Éternelle"],
        "lores": [
            "Souverain millénaire tapi dans son château en Transylvanie, il règne sans partage sur les créatures nocturnes.",
            "Traversant les siècles dans un cercueil de terre noire, son baiser glace le sang et دامne l'esprit."
        ]
    },
    "Zeus": {
        "subtitles": ["Le Père des Dieux", "Le Maître de l'Olympe", "Le Seigneur du Ciel", "Le Foudroyeur"],
        "weapons": ["Éclair Primordial Forgé par les Cyclopes", "Égide Protectrice", "Sceptre Royal"],
        "ultimates": ["Tempête d'Éclairs Divine", "Châtiment de la Foudre Suprême", "Jugement Olympien"],
        "lores": [
            "Ayant renversé les Titans et son propre père Cronos, il règne sur les cieux d'une main de fer.",
            "Volage et impitoyable, ses colères foudroyantes font trembler la Terre jusqu'aux abysses."
        ]
    },
    "Anubis": {
        "subtitles": ["Le Guide des Âmes", "Le Maître de la Nécropole", "Le Chacal Funéraire", "Le Gardien des Morts"],
        "weapons": ["Sceptre Ouas Sacré", "Fléau Nekhekh Doré", "Lame Khépesh Rituelle"],
        "ultimates": ["La Pesée du Cœur (Jugement de Maât)", "Vague de Sables Momificateurs", "Malédiction Funèbre"],
        "lores": [
            "À la tête de chacal noir, il accueille les défunts dans la salle des deux vérités.",
            "Nul ne franchit le seuil du royaume d'Osiris sans que son cœur ne soit comparé au poids d'une plume."
        ]
    },
    "Sun Wukong": {
        "subtitles": ["Le Roi Singe", "Le Grand Sage Égal du Ciel", "Le Fauteur de Troubles Célestes", "L'Immortel Invaincu"],
        "weapons": ["Bâton Ruyi Jingu Bang", "Nuage Magique Somersault", "Poils aux Mille Clones"],
        "ultimates": ["Multiplication Gigantesque", "Regard aux Yeux de Feu", "Transformation des 72 Formes"],
        "lores": [
            "Né d'un rocher magique, il a rayé son nom du livre des morts et mis à sac les palais célestes.",
            "Emprisonné 500 ans sous une montagne, il escorta le moine Tang Sanzang vers les textes sacrés."
        ]
    },
    "Voldemort": {
        "subtitles": ["Le Seigneur des Ténèbres", "Celui-Dont-On-Ne-Doit-Pas-Prononcer-Le-Nom", "L'Héritier de Serpentard", "Le Maître des Serpents"],
        "weapons": ["Baguette d'If et Plume de Phénix", "Serpent Nagini", "Baguette de Sureau Convoitée"],
        "ultimates": ["Avada Kedavra Mortel", "Feu Démoniaque Feudeymon", "Brume Ténébreuse Spectrale"],
        "lores": [
            "Effrayé par la mort au point de déchirer son âme en sept morceaux cachés dans des Horcruxes.",
            "Son règne de terreur a plongé le monde sorcier dans le silence et le cauchemar absolu."
        ]
    },
    "Joker": {
        "subtitles": ["Le Prince Rieur du Crime", "L'Agent du Chaos", "Le Némésis du Chevalier Noir", "Le Clown Sinistre"],
        "weapons": ["Revolver à Bout 'BANG'", "Fleur à Acide Toxique", "Cartes à Jouer Tranchantes"],
        "ultimates": ["Gaz Rieur Hilarant Mortel", "Carnaval Explosif Imprévu", "Blague Dévastatrice"],
        "lores": [
            "Un mauvais jour a suffi pour plonger cet anonyme dans un bain d'acide et une folie sans remède.",
            "Il n'a cure de l'argent ou du pouvoir : son seul but est de prouver que le monde entier est fou."
        ]
    },
    "Deadpool": {
        "subtitles": ["Le Mercenaire Bavard", "Le Briseur de Quatrième Mur", "Le Régénéré Déjanté", "L'Arme XI Rejetée"],
        "weapons": ["Deux Katanas Croisés", "Pistolets Desert Eagle Dorés", "Poche à Grenades Illimitée"],
        "ultimates": ["Danse des Katanas Explosive", "Attaque avec la Barre de PV", "Bavardage Assommant"],
        "lores": [
            "Cobaye d'expérimentations militaires, son cancer et ses cellules mutants se battent en boucle.",
            "Conscient d'être un personnage de fiction, il passe son temps à s'adresser au lecteur ou au joueur."
        ]
    },
    "Wolverine": {
        "subtitles": ["Le mutant Griffu", "L'Arme X", "Le Berserker Canadien", "Le Féroce X-Man"],
        "weapons": ["Griffes d'Adamantium Rétractiles", "Squelette Blindé Métallique", "Poings Bruts"],
        "ultimates": ["Rage Berserker Frénétique", "Tornade Découpeuse X", "Régénération Cellulaire Éclair"],
        "lores": [
            "Vieux de plus d'un siècle, ses sens affûtés et son instinct animal font de lui le pisteur ultime.",
            "L'adamantium greffé sur ses os lui causa d'atroces souffrances, forgeant son caractère d'acier."
        ]
    },
    "Iron Man": {
        "subtitles": ["Le Génie Milliardaire", "L'Armure High-Tech", "L'Architecte des Avengers", "Le Playboy Philanthrope"],
        "weapons": ["Répulseurs Palmaires", "Unibeam Pectoral", "Micro-Missiles Guidés"],
        "ultimates": ["Protocole Veronica (Hulkbuster)", "Rayon Satellitaire Orbital", "Surcharge Énergétique Nanotech"],
        "lores": [
            "Blessé au cœur par des éclats d'obus, il construisit une armure dans une grotte pour s'échapper.",
            "Constamment à la pointe du futur, ses armures perfectionnées rivalisent avec les armées terrestres."
        ]
    },
    "Captain America": {
        "subtitles": ["La Sentinelle de la Liberté", "Le Premier Vengeur", "Le Soldat d'Élite", "Le Porte-Étendard"],
        "weapons": ["Bouclier en Vibranium", "Gants Renforcés", "Pistolet d'Époque 1945"],
        "ultimates": ["Rebond Tactique Suprême", "Charge du Dévouement Absolu", "Fierté Étoilée"],
        "lores": [
            "Jeune gringalet jugé inapte, sa bravoure sans égale lui valut d'être choisi pour le sérum expérimental.",
            "Endormi dans la glace pendant des décennies, il reste le phare moral d'un monde troublé."
        ]
    },
    "Hulk": {
        "subtitles": ["Le Colosse de Jade", "Le Géant Destructeur", "L'Alter Ego Gamma", "La Brute Indomptable"],
        "weapons": ["Mains Broyeuses Titanesques", "Poutrelles Métalliques Déformées", "Onde de Choc Manuelle"],
        "ultimates": ["Hulk Smash Sismique", "Claquement de Mains Sonique", "Rage Gamma Cataclysmique"],
        "lores": [
            "Le scientifique Bruce Banner fut irradié lors d'un test de bombe à rayons gamma.",
            "Plus il s'énerve, plus sa force physique grandit de façon exponentielle, ignorant toute douleur."
            ]
        },
        "Doctor Strange": {
            "subtitles": ["Le Sorcier Suprême", "Le Gardien du Temps", "Le Maître des Arts Mystiques", "Le Guérisseur d'Âmes"],
            "weapons": ["Œil d'Agamotto", "Cape de Lévitation", "Anneau Éléphantin de Téléportation"],
            "ultimates": ["Boucle Temporelle Infinie", "Miroir Dimensionnel Fractal", "Mille Mains de Vishanti"],
            "lores": [
                "Chirurgien réputé aux mains brisées dans un accident, il découvrit à Kamar-Taj la magie des dimensions.",
                "Il veille sur la Terre face aux menaces extradimensionnelles que les armes conventionnelles ignorent."
            ]
        },
        "Godzilla": {
            "subtitles": ["Le Roi des Monstres", "Le Léviathan Atomique", "La Force de la Nature", "L'Alpha Préhistorique"],
            "weapons": ["Rayon Atomique Thermonucléaire", "Queue Balayante Colossale", "Dents et Griffes d'Acier"],
            "ultimates": ["Pulse Nucléaire Éruptif", "Souffle Brûlant Rougeoyant", "Écrasement Titanien"],
            "lores": [
                "Réveillé et muté par les essais nucléaires de l'après-guerre, il incarne le courroux vengeur de la Terre.",
                "Monstre titanesque marchant sur les océans, il détruit villes et rivaux d'un rugissement légendaire."
            ]
        },
        "King Kong": {
            "subtitles": ["Le Monarque de Skull Island", "Le Primat Titanesque", "Le Gardien du Crâne", "Le Roi Déchu"],
            "weapons": ["Hache en Ossements de Titans", "Rochers Massifs Jetés", "Mains Broyeuses"],
            "ultimates": ["Frappe Sismique des Deux Poings", "Rugissement Primaire Écrasant", "Charge Furieuse de l'Île"],
            "lores": [
                "Dernier de sa lignée sur une île maudite, il protège son domaine des horreurs souterraines.",
                "Doté d'une sensibilité inattendue, sa force brute n'égale que sa détermination farouche."
            ]
        },
        "Neo (Matrix)": {
            "subtitles": ["L'Élu de la Matrice", "Le Hacker Solitaire", "Le Briseur de Code", "Le Messie Numérique"],
            "weapons": ["Pistolets Mitrailleurs Doubles", "Poings d'Arts Martiaux Virtuels", "Fusil à Pompe Tactique"],
            "ultimates": ["Arrêt des Balles Télékinétique", "Vol Supersonique Matriciel", "Réécriture du Code Réel"],
            "lores": [
                "Programmé pour croire au quotidien terne d'un employé de bureau, la pilule rouge lui ouvrit les yeux.",
                "Il comprit que la réalité n'était qu'un voile informatique malléable par la simple force de sa volonté."
            ]
        },
        "John Wick": {
            "subtitles": ["Le Boogeyman (Baba Yaga)", "L'Excommunicado Déterminé", "Le Tireur au Crayon", "L'Ombre du Continental"],
            "weapons": ["Pistolet TTI Combat Master 9mm", "Simple Crayon de Papier Bien Taillé", "Fusil à Pompe Benelli M4"],
            "ultimates": ["Gun-Fu Enchaîné à Bout Portant", "Exécution Sans Faillir", "Volonté Inflexible"],
            "lores": [
                "Tueur à gages légendaire retiré des affaires, le vol de sa voiture et le meurtre de son chiot rallumèrent le brasier.",
                "Craint par l'ensemble des syndicats criminels, il termine toujours les missions qu'il a entamées."
            ]
        },
        "Terminator": {
            "subtitles": ["Le Cyberdyne Model 101", "La Machine T-800", "L'Infiltrateur du Futur", "Le Gardien de Cuir"],
            "weapons": ["Fusil à Pompe Winchester Calibre 12", "Minigun Électrique Portatif", "Châssis d'Endosquelette Métallique"],
            "ultimates": ["Mode Scan Analytique I.A.", "Tir de Barrage Sans Recul", "Auto-Destruction Thermique"],
            "lores": [
                "Envoyé depuis un futur dévasté par Skynet, ce cyber-organisme est recouvert de tissus vivants.",
                "Dépourvu d'émotions, de remords ou de fatigue, il avance inéluctablement jusqu'à neutraliser sa cible."
            ]
        },
        "Geralt de Riv": {
            "subtitles": ["Le Loup Blanc", "Le Boucher de Blaviken", "Le Sorceleur Professionnel", "Le Chasseur de Monstres"],
            "weapons": ["Épée d'Argent contre les Monstres", "Épée d'Acier pour les Hommes", "Arbalète de Poing"],
            "ultimates": ["Signe d'Igni Pyrotechnique", "Élixir du Loup Supérieur", "Danse Tranchante du Sorceleur"],
            "lores": [
                "Muté lors de l'Épreuve des Herbes, ses yeux de chat voient clair dans les ténèbres les plus impénétrables.",
                "Parcourant les royaumes pour quelques bourses d'orins, il se retrouve toujours mêlé au destin des rois."
            ]
        },
        "Arthur Pendragon": {
            "subtitles": ["Le Roi de Camelot", "Le Porteur de Caliburn", "Le Souverain des Bretons", "Le Champion de la Table Ronde"],
            "weapons": ["Excalibur Épée Sainte", "Fourreau Enchanté d'Immortalité", "Lance Sacrée Rhongomyniad"],
            "ultimates": ["Frappe de Lumière d'Excalibur", "Rassemblement de la Table Ronde", "Bénédiction de la Dame du Lac"],
            "lores": [
                "Enfant caché qui retira la lame scellée dans la roche, devenant le guide éclairé de l'île de Bretagne.",
                "Symbole de justice et de chevalerie, sa cour de preux chevaliers cherchait le Saint Graal."
            ]
        },
        "Robin des Bois": {
            "subtitles": ["Le Voleur de Sherwood", "L'Archer d'Élite", "Le Prince des Hors-la-Loi", "L'Espoir des Opprimés"],
            "weapons": ["Grand Arc en Bois d'If", "Dague de Chasseur Furtif", "Bâton de Frêne Forestier"],
            "ultimates": ["Flèche Fendant la Flèche", "Pluie de Traits de Sherwood", "Embuscade Végétale Furtive"],
            "lores": [
                "Déclaré hors-la-loi par un shérif corrompu, il volait aux riches tyrans pour redistribuer aux plus démunis.",
                "Invisible sous la canopée de Nottingham, sa corde d'arc ne vibre jamais sans faire mouche."
            ]
        },
        "Satoru Gojo": {
            "subtitles": ["Le Plus Puissant des Exorcistes", "L'Héritier des Six Yeux", "Le Professeur Désinvolte", "Le Fléau des Fléaux"],
            "weapons": ["Poings d'Énergie Occulte", "Bandeau Noir Mystique", "Sceau d'Exorcisme"],
            "ultimates": ["Extension du Territoire: Sphère de l'Espace Infini", "Équation Violette (Murasaki)", "Infini Protecteur Absolu"],
            "lores": [
                "Sa seule naissance a fait basculer l'équilibre du monde occulte en terrorisant les esprits maudits.",
                "Derrière son sourire nonchalant et ses taquineries se cache une puissance divine intouchable."
            ]
        },
        "Eren Yeager": {
            "subtitles": ["Le Titan Assaillant", "Le Chercheur de Liberté", "L'Héritier du Fondateur", "Le Rebelle Inarrêtable"],
            "weapons": ["Lames en Acier Ultra-Dur", "Équipement Tridimensionnel", "Dents de Titan Cuirassées"],
            "ultimates": ["Le Grand Terrassement", "Cristallisation Offensive", "Rugissement de l'Émancipation"],
            "lores": [
                "Ayant vu sa mère dévorée derrière les murs géants, il a juré d'exterminer tous les titans jusqu'au dernier.",
                "Prêt à sacrifier sa propre humanité, il avance vers l'horizon pour arracher sa liberté au destin."
            ]
        },
        "Vegeta": {
            "subtitles": ["Le Prince des Saiyans", "La Fierté Guerrière", "Le Rival Éternel", "Le Guerrier Sans Pitié"],
            "weapons": ["Canon Garric", "Big Bang Attack", "Gants Saiyans Renforcés"],
            "ultimates": ["Final Flash Dévastateur", "Ultra Ego Destructeur", "Explosion Finale Sacrificielle"],
            "lores": [
                "Né pour commander une armée galactique, son orgueil royal a été brisé puis reforgé sur Terre.",
                "Travailleur acharné dans la salle de gravité, il ne reculera jamais devant la grandeur de Goku."
            ]
        },
        "Sephiroth": {
            "subtitles": ["L'Ange à une Aile", "Le Guerrier d'Élite SOLDIER", "La Calamité de Jenova", "Le Cauchemar du Mako"],
            "weapons": ["Masamune Katana de Deux Mètres", "Materia Noire Invocatrice", "Ailes d'Ombre Pure"],
            "ultimates": ["Supernova Galactique", "Octaslash Tranchant Éclair", "Cœur Obscur Flamboyant"],
            "lores": [
                "Héros adulé de la Shinra jusqu'à ce qu'il découvre les expériences atroces qui lui donnèrent la vie.",
                "Considérant la planète comme son héritage légitime, il fait pleuvoir les météores sur Gaïa."
            ]
        },
        "Homer Simpson": {
            "subtitles": ["L'Inspecteur Nucléaire", "L'Amateur de Donuts", "Le Citoyen de Springfield", "Le Paresseux Invincible"],
            "weapons": ["Barre d'Uranium Luminescente", "Bouteille de Bière Duff", "Télécommande Usée"],
            "ultimates": ["D'OH Catastrophique", "Bide d'Acier Rebondissant", "Sieste Réparatrice Absolue"],
            "lores": [
                "Travaillant dans une centrale atomique sans rien y comprendre, il survit miraculeusement à chaque accident.",
                "Un amour sincère pour sa famille et un appétit démesuré pour le gras font de lui un héros malgré tout."
            ]
        },
        "Shaggy (Ultra Instinct)": {
            "subtitles": ["Le Mystérieux Dévoreur", "L'Ami du Grand Dogue", "L'Entité Cosmique Cachée", "Le Peureux Omnipotent"],
            "weapons": ["Sandwich Géant à Triple Étage", "Poussière de Van Mystère", "Boîte de Scooby Snacks"],
            "ultimates": ["Déchaînement à 2% de Puissance", "Vitesse de Course Panique", "Cri Éthéré Brise-Réalité"],
            "lores": [
                "En apparence un adolescent froussard affamé sillonnant les manoirs hantés avec ses amis.",
                "Des rumeurs affirment qu'en puisant dans 1% de son énergie cachée, il terrasse les dieux sans transpirer."
            ]
        },
        "Sans (Undertale)": {
            "subtitles": ["Le Squelette Paresseux", "La Sentinelle de Snowdin", "L'Arbitre du Jugement", "Le Comédien Malicieux"],
            "weapons": ["Gaster Blasters Foudroyants", "Os Magiques Bleus et Blancs", "Coussin Péteur Tactique"],
            "ultimates": ["Attaque Infernale 'Bad Time'", "Manipulation Gravitationnelle Bleue", "Esquive Parfaite Infinie"],
            "lores": [
                "Frère aîné farceur adorant les blagues nulles, il garde un œil prudent sur l'humain tombé dans l'Underground.",
                "Quand retentit la fin des temps, il se dresse comme le juge implacable de vos péchés passés."
            ]
        },
        "Steve (Minecraft)": {
            "subtitles": ["Le Mineur Cubique", "L'Architecte des Mondes", "Le Pourfendeur de l'Ender Dragon", "Le Bâtisseur Silencieux"],
            "weapons": ["Pioche en Diamant Envoûtée", "Épée en Netherite Tranchante", "Seau de Lave Enflammée"],
            "ultimates": ["Plongeon TNT Explosif", "Armure Complète Netherite Protection IV", "Mangeoire de Pomme Dorée d'Enchantement"],
            "lores": [
                "Déposé les mains nues au milieu d'une nature cubique hostile, il coupe des troncs à coups de poing.",
                "Capable de transporter des millions de tonnes de pierre dans ses poches, il bâtit des cités éternelles."
            ]
        }
}

# ==============================================================================
# OPTIONS UNIVERSELLES & PONDÉRATIONS
# ==============================================================================
ARCHETYPES = [
    "Le Protecteur Dévoué", "L'Anti-Héros Solitaire", "Le Filou Indomptable",
    "Le Tyran Mercenaire", "L'Élu Malgré Lui", "Le Sage Mystérieux", "Le Chaotique Imprévisible"
]

FORCE_OPTIONS = [
    ("Trop faible", 35.0, 2),
    ("Squelette", 25.0, 5),
    ("Humain", 18.0, 10),
    ("Puissant", 11.0, 25),
    ("Bodybuilder", 6.0, 45),
    ("Colossal", 3.5, 70),
    ("Titanesque", 1.3, 90),
    ("Dieu", 0.2, 100)
]

SPEED_OPTIONS = [
    ("Tortue", 35.0, 2),
    ("Humain", 25.0, 10),
    ("Lent", 18.0, 5),
    ("Rapide", 11.0, 25),
    ("Supersonique", 6.0, 50),
    ("Hyper-vitesse", 3.5, 75),
    ("Vitesse de la lumière", 1.3, 95),
    ("Téléportation instantanée", 0.2, 100)
]

SIZE_OPTIONS = [
    ("30cm", 5.0),
    ("70cm/1m20", 35.0),
    ("1m60/1m70", 20.0),
    ("1m80", 15.0),
    ("2m00", 7.0),
    ("3m00", 4.0),
    ("5m00", 3.0),
    ("10m+", 1.0)
]

WEAKNESS_OPTIONS = [
    "Ne sait pas nager", "Peur du noir", "Myope", "Acrophobie",
    "Allergique au pollen", "Gourmandise impulsive", "Aucune", "Aucune"
]

PLOT_TWISTS = [
    {"label": "A trouvé des bottes ailées (+2 Vitesse)", "type": "BONUS", "speed": 2, "qi": 0, "force": 0},
    {"label": "A déchiffré un grimoire (+2 QI)", "type": "BONUS", "speed": 0, "qi": 2, "force": 0},
    {"label": "A bu un élixir d'ogre (+40 Force)", "type": "BONUS", "speed": 0, "qi": 0, "force": 5},
    {"label": "S'est tordu la cheville (-2 Vitesse)", "type": "PUNITION", "speed": -2, "qi": 0, "force": 0},
    {"label": "A pris un coup sur la tête (-2 QI)", "type": "PUNITION", "speed": 0, "qi": -2, "force": 0},
    {"label": "Est atteint de la goutte (-5 Force)", "type": "PUNITION", "speed": 0, "qi": 0, "force": -5},
    {"label": "A oublié ses clés (Aucun impact)", "type": "AUCUN", "speed": 0, "qi": 0, "force": 0},
    {"label": "Rien d'inhabituel (Aucun impact)", "type": "AUCUN", "speed": 0, "qi": 0, "force": 0}
]

PALETTE = [
    (230, 57, 70), (244, 162, 97), (233, 196, 106), (42, 157, 143),
    (38, 70, 83), (69, 123, 157), (168, 218, 220), (155, 93, 229),
    (241, 91, 181), (254, 217, 183), (0, 180, 216), (114, 9, 183)
]

# ==============================================================================
# OUTILS ANTI-DÉBORDEMENT (mesure réelle du texte via la police pygame)
# ==============================================================================
def fit_text(font, text, max_width, ellipsis=".."):
    """Renvoie 'text' tel quel s'il tient dans 'max_width' pixels avec cette police.
    Sinon, le tronque progressivement (en se basant sur la largeur réellement
    mesurée par pygame, pas sur un nombre de caractères) et ajoute une ellipse,
    pour ne jamais dessiner de texte qui dépasse la zone qui lui est réservée."""
    if not text:
        return text
    if max_width is None or max_width <= 0:
        return text
    if font.size(text)[0] <= max_width:
        return text
    if font.size(ellipsis)[0] > max_width:
        return ellipsis

    truncated = text
    while truncated and font.size(truncated + ellipsis)[0] > max_width:
        truncated = truncated[:-1]
    return (truncated + ellipsis) if truncated else ellipsis


def wrap_text(font, text, max_width):
    """Découpe 'text' en lignes qui tiennent chacune dans 'max_width' pixels,
    en mesurant la largeur réelle de chaque ligne au lieu de compter les
    caractères (évite qu'une ligne ne déborde du cadre qui l'affiche)."""
    words = text.split()
    if not words:
        return []
    lines = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if font.size(candidate)[0] <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


# ==============================================================================
# CLASSE DE GESTION DE ROUE GRAPHIQUE PYGAME
# ==============================================================================
class WheelItem:
    def __init__(self, label, weight, data=None):
        self.label = label
        self.weight = weight
        self.data = data

class Wheel:
    def __init__(self, title, items, center=(460, 390), radius=250):
        self.title = title
        self.items = items
        self.center = center
        self.radius = radius
        self.current_angle = 0.0
        self.is_spinning = False
        self.start_angle = 0.0
        self.target_angle = 0.0
        self.spin_timer = 0.0
        self.spin_duration = 3.2
        self.selected_item = None
        self.colors = [PALETTE[i % len(PALETTE)] for i in range(len(items))]

        total_weight = sum(item.weight for item in self.items)
        self.proportions = [item.weight / total_weight for item in self.items]
        self.slice_angles = [p * 360.0 for p in self.proportions]

    def spin(self):
        chosen_item = random.choices(self.items, weights=[it.weight for it in self.items], k=1)[0]
        self.selected_item = chosen_item
        chosen_idx = self.items.index(chosen_item)

        start_deg = sum(self.slice_angles[:chosen_idx])
        end_deg = start_deg + self.slice_angles[chosen_idx]
        mid_deg = (start_deg + end_deg) / 2.0

        target_mod = (270 - mid_deg) % 360
        full_turns = random.randint(5, 7) * 360
        current_mod = self.current_angle % 360
        delta = (target_mod - current_mod) % 360
        if delta < 180:
            delta += 360

        self.start_angle = self.current_angle
        self.target_angle = self.current_angle + full_turns + delta
        self.spin_timer = 0.0
        self.is_spinning = True

    def update(self, dt):
        if not self.is_spinning:
            return False
        self.spin_timer += dt
        t = min(1.0, self.spin_timer / self.spin_duration)
        ease = 1.0 - math.pow(1.0 - t, 3.0)
        self.current_angle = self.start_angle + (self.target_angle - self.start_angle) * ease

        if t >= 1.0:
            self.is_spinning = False
            self.current_angle = self.target_angle
            return True
        return False

    def draw(self, surface, font, title_font, title_max_width=560, title_y=70):
        # Certains titres de roue intègrent le nom du personnage (ex: "Roue 8 :
        # Capacité Ultime de Shaggy (Ultra Instinct)") et peuvent devenir très
        # longs : on les borne pour qu'ils ne débordent jamais de l'écran, quelle
        # que soit la largeur de l'écran cible.
        title_text = fit_text(title_font, self.title, title_max_width)
        t_surf = title_font.render(title_text, True, (255, 215, 0))
        t_rect = t_surf.get_rect(center=(self.center[0], title_y))
        surface.blit(t_surf, t_rect)

        cx, cy = self.center
        r = self.radius

        pygame.draw.circle(surface, (15, 18, 28), (cx + 6, cy + 8), r + 8)
        pygame.draw.circle(surface, (212, 175, 55), (cx, cy), r + 8)

        accum_angle = self.current_angle
        for i, item in enumerate(self.items):
            span = self.slice_angles[i]
            color = self.colors[i]
            start_a = accum_angle

            steps = max(2, int(span / 3))
            points = [(cx, cy)]
            for s in range(steps + 1):
                cur_a = math.radians(start_a + (span * s / steps))
                px = cx + r * math.cos(cur_a)
                py = cy + r * math.sin(cur_a)
                points.append((px, py))

            pygame.draw.polygon(surface, color, points)
            pygame.draw.polygon(surface, (30, 30, 40), points, 1)

            if span >= 4.5:
                mid_a = math.radians(start_a + span / 2.0)
                txt_dist = r * 0.65
                tx = cx + txt_dist * math.cos(mid_a)
                ty = cy + txt_dist * math.sin(mid_a)

                # Largeur réellement disponible pour ce libellé à cette distance
                # du centre (longueur de l'arc de la part). Avec 50 personnages
                # sur la Roue 1, chaque part ne fait qu'environ 7°, donc un
                # nombre fixe de caractères (l'ancien "16 max") débordait très
                # largement sur les parts voisines. On mesure la vraie largeur
                # du texte et on l'adapte à la place réellement disponible ;
                # si la part est trop étroite pour rester lisible, on n'affiche
                # simplement rien plutôt que de laisser le texte déborder.
                available_width = txt_dist * math.radians(span)
                min_readable_width = font.size("A..")[0]

                if available_width >= min_readable_width:
                    label_clean = fit_text(font, item.label, available_width)
                    rot_deg = -(start_a + span / 2.0)

                    rot_deg_norm = rot_deg % 360
                    if 90 < rot_deg_norm < 270:
                        rot_deg_norm += 180

                    lbl_surf = font.render(label_clean, True, (255, 255, 255))
                    shadow_surf = font.render(label_clean, True, (10, 10, 10))
                    rot_lbl = pygame.transform.rotate(lbl_surf, rot_deg_norm)
                    rot_shadow = pygame.transform.rotate(shadow_surf, rot_deg_norm)

                    surface.blit(rot_shadow, rot_shadow.get_rect(center=(tx + 1, ty + 1)))
                    surface.blit(rot_lbl, rot_lbl.get_rect(center=(tx, ty)))

            accum_angle += span

        pygame.draw.circle(surface, (20, 24, 36), (cx, cy), 36)
        pygame.draw.circle(surface, (212, 175, 55), (cx, cy), 36, 4)
        pygame.draw.circle(surface, (255, 215, 0), (cx, cy), 12)

        tip_y = cy - r - 2
        p1 = (cx, tip_y + 24)
        p2 = (cx - 18, tip_y - 12)
        p3 = (cx + 18, tip_y - 12)
        pygame.draw.polygon(surface, (0, 0, 0, 120), [(p1[0], p1[1] + 3), (p2[0] + 2, p2[1] + 3), (p3[0] + 2, p3[1] + 3)])
        pygame.draw.polygon(surface, (240, 50, 50), [p1, p2, p3])
        pygame.draw.polygon(surface, (255, 255, 255), [p1, p2, p3], 2)

# ==============================================================================
# GESTIONNAIRE PRINCIPAL DU JEU
# ==============================================================================
class DestinyGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("La Roue du Destin - Générateur Procédural de Légendes")

        # Canevas mobile portrait au format 9:16. Toute la mise en page ci-dessous
        # (roue, bouton, fiche, écran final) est calculée à partir de self.width /
        # self.height et des vraies métriques de police, pour que rien ne dépasse
        # jamais de cette fenêtre.
        self.width = 540
        self.height = 960
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.margin = 16

        self.font_title = pygame.font.SysFont("georgia", 22, bold=True)
        self.font_subtitle = pygame.font.SysFont("trebuchetms", 15, bold=True)
        self.font_slice = pygame.font.SysFont("arial", 10, bold=True)
        self.font_btn = pygame.font.SysFont("impact", 18)
        self.font_card = pygame.font.SysFont("arial", 12)
        self.font_card_bold = pygame.font.SysFont("arial", 12, bold=True)
        self.font_lore = pygame.font.SysFont("georgia", 11, italic=True)

        self.char_data = {
            "name": None,
            "subtitle": None,
            "archetype": None,
            "force_label": None,
            "force_val": 10,
            "speed_label": None,
            "speed_val": 10,
            "qi_val": 10,
            "size": None,
            "weapon": None,
            "ultimate": None,
            "weakness": None,
            "twist": None,
            "twist_obj": None,
            "lore": None
        }

        # Étapes de la progression (10 roues)
        self.current_step = 0
        self.wheels = []
        self.post_spin_delay = 0.0
        self.waiting_next_step = False
        self.last_result_label = ""

        # Statut du rendu final & téléchargement image
        self.final_image = None
        self.image_downloading = False
        self.image_prompt = ""

        # --- Mise en page de l'écran "roue", reprenant les coordonnées que tu as
        #     réglées dans l'aperçu interactif. ---
        # Roue : cadre demandé x=40, y=18, largeur=462, hauteur=400. Comme tu l'as
        # remontée presque jusqu'en haut de l'écran, il ne restait plus de place pour
        # le grand titre habituel au-dessus : je l'ai remplacé par un tout petit titre,
        # et la roue est très légèrement plus bas/petite (rayon 175 au lieu de ~185)
        # juste assez pour que ce titre reste lisible sans jamais sortir de l'écran.
        self.font_wheel_title = pygame.font.SysFont("georgia", 15, bold=True)
        self.wheel_title_max_width = self.width - 2 * self.margin
        self.wheel_title_y = self.margin + self.font_wheel_title.get_height() // 2

        self.wheel_radius = 170
        self.wheel_center = (268, 230)

        # Bouton "Lancer la roue" : repris tel quel de tes coordonnées.
        self.spin_btn_rect = pygame.Rect(101, 470, 334, 50)

        # Fiche compacte : reprise telle quelle de tes coordonnées.
        self.wheel_panel_rect = pygame.Rect(13, 562, 508, 392)

        # Initialisation de la première roue
        self.setup_wheel_1()

    def setup_wheel_1(self):
        items = []
        for name in CHARACTERS_DATA.keys():
            # Dieu est plus rare (0.3), les autres sont équiprobables (1.5)
            weight = 0.3 if name == "Dieu" else 1.5
            items.append(WheelItem(name, weight))
        self.wheels.append(Wheel("Roue 1 : Choix du Personnage Sacré", items, center=self.wheel_center, radius=self.wheel_radius))

    def create_adapted_wheels(self):
        p_name = self.char_data["name"]
        p_info = CHARACTERS_DATA[p_name]

        # Roue 2 : Sous-titre adapté
        sub_items = [WheelItem(sub, 1.0) for sub in p_info["subtitles"]]
        self.wheels.append(Wheel(f"Roue 2 : Quel genre de {p_name} ?", sub_items, center=self.wheel_center, radius=self.wheel_radius))

        # Roue 3 : Archétype (Universel)
        arch_items = [WheelItem(arch, 1.0) for arch in ARCHETYPES]
        self.wheels.append(Wheel("Roue 3 : Archétype de l'Âme", arch_items, center=self.wheel_center, radius=self.wheel_radius))

        # Roue 4 : Force (Pondérée)
        force_items = [WheelItem(lbl, w, val) for lbl, w, val in FORCE_OPTIONS]
        self.wheels.append(Wheel("Roue 4 : Puissance Physique Brutale", force_items, center=self.wheel_center, radius=self.wheel_radius))

        # Roue 5 : Vitesse (Pondérée)
        speed_items = [WheelItem(lbl, w, val) for lbl, w, val in SPEED_OPTIONS]
        self.wheels.append(Wheel("Roue 5 : Vélocité & Agilité Céleste", speed_items, center=self.wheel_center, radius=self.wheel_radius))

        # Roue 6 : Taille (Pondérée, petites tailles larges)
        size_items = [WheelItem(lbl, w) for lbl, w in SIZE_OPTIONS]
        self.wheels.append(Wheel("Roue 6 : Gabarit Corporel", size_items, center=self.wheel_center, radius=self.wheel_radius))

        # Roue 7 : Arme adaptée
        wep_items = [WheelItem(wep, 1.0) for wep in p_info["weapons"]]
        self.wheels.append(Wheel(f"Roue 7 : Arme Emblématique de {p_name}", wep_items, center=self.wheel_center, radius=self.wheel_radius))

        # Roue 8 : Capacité Ultime adaptée
        ult_items = [WheelItem(ult, 1.0) for ult in p_info["ultimates"]]
        self.wheels.append(Wheel(f"Roue 8 : Capacité Ultime de {p_name}", ult_items, center=self.wheel_center, radius=self.wheel_radius))

        # Roue 9 : Faiblesse
        weak_items = [WheelItem(wk, 1.0) for wk in WEAKNESS_OPTIONS]
        self.wheels.append(Wheel("Roue 9 : Talon d'Achille & Faiblesse", weak_items, center=self.wheel_center, radius=self.wheel_radius))

        # Roue 10 : Plot Twist
        twist_items = [WheelItem(tw["label"], 1.0, tw) for tw in PLOT_TWISTS]
        self.wheels.append(Wheel("Roue 10 : Coup de Théâtre du Destin", twist_items, center=self.wheel_center, radius=self.wheel_radius))

        # Tirage automatique d'un des Lores
        self.char_data["lore"] = random.choice(p_info["lores"])

    def apply_current_result(self, item):
        self.last_result_label = item.label
        if self.current_step == 0:
            self.char_data["name"] = item.label
            self.create_adapted_wheels()
        elif self.current_step == 1:
            self.char_data["subtitle"] = item.label
        elif self.current_step == 2:
            self.char_data["archetype"] = item.label
        elif self.current_step == 3:
            self.char_data["force_label"] = item.label
            self.char_data["force_val"] = item.data
        elif self.current_step == 4:
            self.char_data["speed_label"] = item.label
            self.char_data["speed_val"] = item.data
        elif self.current_step == 5:
            self.char_data["size"] = item.label
        elif self.current_step == 6:
            self.char_data["weapon"] = item.label
        elif self.current_step == 7:
            self.char_data["ultimate"] = item.label
        elif self.current_step == 8:
            self.char_data["weakness"] = item.label
        elif self.current_step == 9:
            self.char_data["twist"] = item.label
            self.char_data["twist_obj"] = item.data
            # Application des modificateurs de stats
            self.char_data["force_val"] = max(1, self.char_data["force_val"] + item.data["force"])
            self.char_data["speed_val"] = max(1, self.char_data["speed_val"] + item.data["speed"])
            self.char_data["qi_val"] = max(1, self.char_data["qi_val"] + item.data["qi"])

    def trigger_image_generation(self):
        """Lance la génération et le téléchargement autonome en arrière-plan sans bloquer l'UI."""
        name = self.char_data["name"]
        sub = self.char_data["subtitle"]
        size = self.char_data["size"]
        weapon = self.char_data["weapon"]
        force = self.char_data["force_label"]

        prompt = (
            f"Epic digital masterpiece portrait of {name}, {sub}, body size {size}, wielding {weapon}, "
            f"demonstrating {force} strength, fantasy cinematic lighting, hyper-detailed, dynamic composition, 8k"
        )
        self.image_prompt = prompt
        self.image_downloading = True

        thread = threading.Thread(target=self._download_image_thread, args=(prompt,), daemon=True)
        thread.start()

    def _download_image_thread(self, prompt):
        try:
            encoded = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512&nologo=true&seed={random.randint(1, 999999)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'PygameDestinyWheel/2.6.1'})
            with urllib.request.urlopen(req, timeout=12) as response:
                img_data = response.read()
                raw_image = pygame.image.load(io.BytesIO(img_data))
                self.final_image = pygame.transform.smoothscale(raw_image, (320, 320))
        except Exception:
            # Fallback procédural en cas d'absence de connexion Internet
            fallback = pygame.Surface((320, 320))
            fallback.fill((28, 32, 48))
            pygame.draw.rect(fallback, (212, 175, 55), (8, 8, 304, 304), 3)
            pygame.draw.circle(fallback, (45, 55, 80), (160, 130), 75)

            initials = "".join([w[0] for w in self.char_data["name"].split()[:2]]).upper()
            f_big = pygame.font.SysFont("georgia", 52, bold=True)
            txt = f_big.render(initials, True, (255, 215, 0))
            fallback.blit(txt, txt.get_rect(center=(160, 130)))

            f_sub = pygame.font.SysFont("arial", 13, bold=True)
            msg1 = f_sub.render("AVATAR ÉTHÉRÉ GÉNÉRÉ", True, (220, 220, 220))
            msg2 = f_sub.render("(Mode Hors-Ligne Actif)", True, (160, 170, 190))
            fallback.blit(msg1, msg1.get_rect(center=(160, 245)))
            fallback.blit(msg2, msg2.get_rect(center=(160, 270)))
            self.final_image = fallback
        finally:
            self.image_downloading = False

    def draw_character_sheet(self, surface, x, y, w, h):
        """Dessine la fiche récapitulative dynamique sur le volet du bas (mode mobile portrait).
        Toutes les dimensions sont calculées à partir de (x, y, w, h) et des vraies
        métriques de police, afin que le contenu ne dépasse jamais cette zone."""
        pygame.draw.rect(surface, (20, 24, 38), (x, y, w, h), border_radius=12)
        pygame.draw.rect(surface, (212, 175, 55), (x, y, w, h), 2, border_radius=12)

        # En-tête de la fiche
        header_h = self.font_subtitle.get_height() + 14
        hdr_rect = pygame.Rect(x, y, w, header_h)
        pygame.draw.rect(surface, (32, 38, 60), hdr_rect, border_top_left_radius=12, border_top_right_radius=12)
        pygame.draw.line(surface, (212, 175, 55), (x, y + header_h), (x + w, y + header_h), 2)

        t_surf = self.font_subtitle.render("FICHE DU PERSONNAGE", True, (255, 215, 0))
        surface.blit(t_surf, t_surf.get_rect(center=(x + w // 2, y + header_h // 2)))

        # Lignes d'informations
        fields = [
            ("Nom", self.char_data["name"]),
            ("Sous-titre", self.char_data["subtitle"]),
            ("Archétype", self.char_data["archetype"]),
            ("Force", f"{self.char_data['force_label']} ({self.char_data['force_val']}/100)" if self.char_data['force_label'] else None),
            ("Vitesse", f"{self.char_data['speed_label']} ({self.char_data['speed_val']}/100)" if self.char_data['speed_label'] else None),
            ("Intelligence (QI)", f"{self.char_data['qi_val']}" if self.char_data['name'] else None),
            ("Gabarit", self.char_data["size"]),
            ("Arme", self.char_data["weapon"]),
            ("Capacité Ultime", self.char_data["ultimate"]),
            ("Faiblesse", self.char_data["weakness"]),
            ("Plot Twist", self.char_data["twist"])
        ]

        # Largeur de la colonne "libellé" mesurée sur le libellé le plus large,
        # pour que la colonne "valeur" démarre toujours au bon endroit.
        label_col_width = max(self.font_card_bold.size(f"{label} :")[0] for label, _ in fields)
        value_x = x + 12 + label_col_width + 10
        value_max_width = (x + w - 12) - value_x
        row_h = self.font_card.get_height() + 8

        show_result_box = bool(self.last_result_label) and self.current_step < 10
        result_box_h = 0
        if show_result_box:
            result_box_h = self.font_slice.get_height() * 2 + self.font_subtitle.get_height() + 40

        # On ne dessine que le nombre de lignes qui tient réellement dans la
        # hauteur disponible : le reliquat sert au bloc "dernier tirage" plus
        # bas, ce qui garantit qu'on ne déborde jamais du panneau, quelle que
        # soit la taille de police effective.
        reserved_bottom = (result_box_h + 10) if show_result_box else 6
        available_for_rows = (y + h) - (y + header_h + 6) - reserved_bottom
        max_visible_rows = max(1, int(available_for_rows // row_h))
        visible_fields = fields[:max_visible_rows]

        curr_y = y + header_h + 6
        for label, val in visible_fields:
            lbl_surf = self.font_card_bold.render(f"{label} :", True, (170, 185, 215))
            surface.blit(lbl_surf, (x + 12, curr_y))

            val_str = val if val else "--- En attente ---"
            val_color = (255, 255, 255) if val else (100, 110, 130)
            if label == "Nom" and val:
                val_color = (255, 215, 0)
            elif label == "Plot Twist" and val:
                val_color = (130, 255, 140) if "BONUS" in str(self.char_data.get("twist_obj", {}).get("type")) else (255, 130, 130)

            val_str = fit_text(self.font_card, val_str, value_max_width)

            val_surf = self.font_card.render(val_str, True, val_color)
            surface.blit(val_surf, (value_x, curr_y))
            curr_y += row_h

        # Résultat immédiat du tour
        if show_result_box:
            res_box = pygame.Rect(x + 10, y + h - result_box_h - 8, w - 20, result_box_h)
            pygame.draw.rect(surface, (28, 35, 52), res_box, border_radius=8)
            pygame.draw.rect(surface, (70, 130, 200), res_box, 1, border_radius=8)

            r_title = self.font_slice.render("DERNIER TIRAGE OBTENU :", True, (255, 215, 0))
            surface.blit(r_title, (res_box.x + 10, res_box.y + 8))

            res_label_max_width = res_box.width - 20
            res_label_text = fit_text(self.font_subtitle, self.last_result_label, res_label_max_width)
            res_name = self.font_subtitle.render(res_label_text, True, (255, 255, 255))
            surface.blit(res_name, (res_box.x + 10, res_box.y + 8 + self.font_slice.get_height() + 4))

            if self.waiting_next_step:
                cnt_txt = self.font_slice.render("Roue suivante imminente...", True, (150, 230, 150))
                surface.blit(cnt_txt, (res_box.x + 10, res_box.y + 8 + self.font_slice.get_height() + 4 + self.font_subtitle.get_height() + 4))

    def draw_final_screen(self, surface):
        """Écran récapitulatif (portrait mobile) : tout est empilé verticalement
        et chaque bloc est positionné à partir de la fin du précédent, avec le
        bouton "Recommencer" ancré en bas et l'encadré Lore qui absorbe l'espace
        restant — le contenu ne peut donc jamais dépasser le canevas 9:16."""
        content_w = self.width - 2 * self.margin
        cursor_y = self.margin

        # --- Titre ---
        title_lines = wrap_text(self.font_title, "L'INCARNATION DE LA DESTINÉE EST ACCOMPLIE", content_w)
        title_line_h = self.font_title.get_height() + 2
        for line in title_lines:
            t_surf = self.font_title.render(line, True, (255, 215, 0))
            surface.blit(t_surf, t_surf.get_rect(center=(self.width // 2, cursor_y + title_line_h // 2)))
            cursor_y += title_line_h
        cursor_y += 6

        # --- Nom + sous-titre ---
        nom_complet = f"{self.char_data['name']} - {self.char_data['subtitle']}"
        nom_complet = fit_text(self.font_title, nom_complet, content_w)
        h_surf = self.font_title.render(nom_complet, True, (255, 225, 80))
        surface.blit(h_surf, h_surf.get_rect(center=(self.width // 2, cursor_y + title_line_h // 2)))
        cursor_y += title_line_h + 10

        # --- Portrait ---
        img_size = min(int(self.width * 0.42), 240)
        img_frame = pygame.Rect((self.width - img_size) // 2 - 6, cursor_y, img_size + 12, img_size + 12)
        pygame.draw.rect(surface, (18, 22, 34), img_frame, border_radius=10)
        pygame.draw.rect(surface, (212, 175, 55), img_frame, 3, border_radius=10)

        if self.final_image:
            scaled_img = pygame.transform.smoothscale(self.final_image, (img_size, img_size))
            surface.blit(scaled_img, (img_frame.x + 6, img_frame.y + 6))
        elif self.image_downloading:
            pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1.0) / 2.0
            col = (int(100 + pulse * 140), int(150 + pulse * 100), 255)
            load_txt = fit_text(self.font_subtitle, "Matérialisation de l'image...", img_frame.width - 16)
            load_txt_surf = self.font_subtitle.render(load_txt, True, col)
            surface.blit(load_txt_surf, load_txt_surf.get_rect(center=(img_frame.centerx, img_frame.centery - 12)))

            load_sub = fit_text(self.font_slice, "Connexion à l'I.A. générative...", img_frame.width - 16)
            load_sub_surf = self.font_slice.render(load_sub, True, (180, 190, 210))
            surface.blit(load_sub_surf, load_sub_surf.get_rect(center=(img_frame.centerx, img_frame.centery + 14)))
        cursor_y = img_frame.bottom + 12

        # --- Grille d'attributs ---
        stats_fields = [
            ("Archétype", self.char_data["archetype"]),
            ("Gabarit", self.char_data["size"]),
            ("Arme", self.char_data["weapon"]),
            ("Capacité Ultime", self.char_data["ultimate"]),
            ("Faiblesse", self.char_data["weakness"]),
            ("Twist du Destin", self.char_data["twist"])
        ]
        label_col_width = max(self.font_card_bold.size(f"{label} :")[0] for label, _ in stats_fields)
        value_x = self.margin + label_col_width + 10
        value_max_width = (self.margin + content_w) - value_x
        row_h = self.font_card_bold.get_height() + 8

        for label, val in stats_fields:
            l_render = self.font_card_bold.render(f"{label} :", True, (160, 185, 220))
            surface.blit(l_render, (self.margin, cursor_y))
            val_str = fit_text(self.font_card, str(val), value_max_width)
            v_render = self.font_card.render(val_str, True, (255, 255, 255))
            surface.blit(v_render, (value_x, cursor_y))
            cursor_y += row_h

        cursor_y += 6
        pygame.draw.line(surface, (50, 60, 90), (self.margin, cursor_y), (self.margin + content_w, cursor_y), 1)
        cursor_y += 12

        # --- Barres visuelles de statistiques ---
        bars = [
            ("FORCE", self.char_data["force_val"], (230, 60, 60)),
            ("VITESSE", self.char_data["speed_val"], (60, 190, 240)),
            ("INTELLIGENCE (QI)", self.char_data["qi_val"] * 5, (180, 90, 240))
        ]
        bar_h = 14
        for name_stat, val_stat, bar_col in bars:
            val_stat_clamped = max(0, min(100, val_stat))
            s_lbl = self.font_card_bold.render(f"{name_stat} : {val_stat}/100", True, (230, 230, 230))
            surface.blit(s_lbl, (self.margin, cursor_y))
            cursor_y += self.font_card_bold.get_height() + 3

            bar_bg = pygame.Rect(self.margin, cursor_y, content_w, bar_h)
            pygame.draw.rect(surface, (35, 40, 55), bar_bg, border_radius=6)
            bar_fill = pygame.Rect(self.margin, cursor_y, int(content_w * (val_stat_clamped / 100.0)), bar_h)
            pygame.draw.rect(surface, bar_col, bar_fill, border_radius=6)
            pygame.draw.rect(surface, (255, 255, 255), bar_bg, 1, border_radius=6)
            cursor_y += bar_h + 10

        # --- Bouton Recommencer, ancré en bas de l'écran ---
        btn_w, btn_h = min(content_w, 320), 46
        restart_rect = pygame.Rect((self.width - btn_w) // 2, self.height - self.margin - btn_h, btn_w, btn_h)
        self.restart_rect = restart_rect

        # --- Encadré Lore : occupe tout l'espace restant entre les stats et le
        #     bouton, avec un minimum garanti pour ne jamais avoir une hauteur
        #     négative si les blocs au-dessus ont pris plus de place que prévu.
        lore_top = cursor_y + 6
        lore_bottom = restart_rect.top - 10
        lore_box = pygame.Rect(self.margin, lore_top, content_w, max(50, lore_bottom - lore_top))
        pygame.draw.rect(surface, (18, 22, 34), lore_box, border_radius=10)
        pygame.draw.rect(surface, (70, 130, 200), lore_box, 1, border_radius=10)

        l_title = fit_text(self.font_slice, "ANCIENNES CHRONIQUES & LORE", lore_box.width - 20)
        l_title_surf = self.font_slice.render(l_title, True, (255, 215, 0))
        surface.blit(l_title_surf, (lore_box.x + 10, lore_box.y + 8))

        lore_text = self.char_data["lore"] or "Une légende inscrite au firmament..."
        lore_max_width = lore_box.width - 20
        lines = wrap_text(self.font_lore, lore_text, lore_max_width)

        ly = lore_box.y + 8 + self.font_slice.get_height() + 8
        lore_bottom_limit = lore_box.bottom - 14
        lore_line_h = self.font_lore.get_height() + 4
        for line in lines:
            if ly + lore_line_h > lore_bottom_limit:
                break
            rendered = self.font_lore.render(line, True, (220, 225, 240))
            surface.blit(rendered, (lore_box.x + 10, ly))
            ly += lore_line_h

        # --- Dessin du bouton (par-dessus, ancré en bas) ---
        pygame.draw.rect(surface, (180, 40, 50), restart_rect, border_radius=8)
        pygame.draw.rect(surface, (255, 215, 0), restart_rect, 2, border_radius=8)
        btn_txt_str = fit_text(self.font_btn, "RÉINCARNER À NOUVEAU", restart_rect.width - 16)
        btn_txt = self.font_btn.render(btn_txt_str, True, (255, 255, 255))
        surface.blit(btn_txt, btn_txt.get_rect(center=restart_rect.center))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            current_wheel = self.wheels[self.current_step] if self.current_step < 10 else None

            # ------------------------------------------------------------------
            # GESTION DES ÉVÉNEMENTS
            # ------------------------------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mpos = event.pos

                    # Clic sur SPIN
                    if self.current_step < 10:
                        can_spin = (not current_wheel.is_spinning) and (not self.waiting_next_step)
                        if can_spin and self.spin_btn_rect.collidepoint(mpos):
                            current_wheel.spin()

                    # Clic sur Réincarner
                    elif self.current_step == 10:
                        if hasattr(self, 'restart_rect') and self.restart_rect.collidepoint(mpos):
                            self.__init__()
                            return self.run()

            # ------------------------------------------------------------------
            # LOGIQUE DU JEU & TRANSITIONS
            # ------------------------------------------------------------------
            if current_wheel:
                finished = current_wheel.update(dt)
                if finished:
                    self.apply_current_result(current_wheel.selected_item)
                    self.waiting_next_step = True
                    self.post_spin_delay = 1.5

                if self.waiting_next_step:
                    self.post_spin_delay -= dt
                    if self.post_spin_delay <= 0:
                        self.waiting_next_step = False
                        self.current_step += 1
                        if self.current_step == 10:
                            # Déclenchement automatique de la génération d'image
                            self.trigger_image_generation()

            # ------------------------------------------------------------------
            # DESSIN / RENDU GRAPHIQUE
            # ------------------------------------------------------------------
            self.screen.fill((12, 15, 24))

            if self.current_step < 10:
                current_wheel.draw(
                    self.screen, self.font_slice, self.font_wheel_title,
                    title_max_width=self.wheel_title_max_width, title_y=self.wheel_title_y
                )

                can_spin = (not current_wheel.is_spinning) and (not self.waiting_next_step)
                btn_color = (40, 167, 69) if can_spin else (70, 75, 85)
                pygame.draw.rect(self.screen, btn_color, self.spin_btn_rect, border_radius=8)
                pygame.draw.rect(self.screen, (255, 215, 0) if can_spin else (110, 115, 125), self.spin_btn_rect, 2, border_radius=8)

                label_spin = "LANCER LA ROUE" if can_spin else ("ROTATION..." if current_wheel.is_spinning else "RÉSULTAT !")
                label_spin = fit_text(self.font_btn, label_spin, self.spin_btn_rect.width - 16)
                btn_surface = self.font_btn.render(label_spin, True, (255, 255, 255))
                self.screen.blit(btn_surface, btn_surface.get_rect(center=self.spin_btn_rect.center))

                # Fiche du personnage, compacte, sous le bouton
                self.draw_character_sheet(
                    self.screen, self.wheel_panel_rect.x, self.wheel_panel_rect.y,
                    self.wheel_panel_rect.width, self.wheel_panel_rect.height
                )
            else:
                self.draw_final_screen(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = DestinyGame()
    game.run()
         