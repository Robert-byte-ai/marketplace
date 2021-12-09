from main.models import Tag, User, Seller, Category, Ad

tags_names = ['Другое', 'Искусство', 'Наука>', 'Ремонт', 'Автолюбителям', 'Кулинария', 'Красота', 'Хобби', 'Ретро']
for tag in tags_names:
    Tag.objects.create(name=tag)

Tag.objects.all()
# <QuerySet [<Tag: Другое>, <Tag: Искусство>, <Tag: Наука>, <Tag: Ремонт>, <Tag: Автолюбителям>, <Tag: Кулинария>,
# <Tag: Красота>, <Tag: Хобби>, <Tag: Ретро>]>

usernames = ['robert', 'Robert1', 'Robert2', 'Robert3']

for username in usernames:
    User.objects.create_user(username=username)

User.objects.all()
# <QuerySet [<User: robert>, <User: Robert1>, <User: Robert2>, <User: Robert3>]>

for user in User.objects.all():
    Seller.objects.create(user=user)

Seller.objects.all()
# <QuerySet [<Seller: Robert2>, <Seller: Robert1>, <Seller: robert>]>

categoryies = ['Садоводство', 'Музыка', 'Одежда', 'Книги']

for category in categoryies:
    Category.objets.create(name=category)

Category.objects.all()
# <QuerySet [<Category: Садоводство>, <Category: Музыка>, <Category: Одежда>, <Category: Книги>]>

Seller.objects.get(pk=1).ads.create(name='something', category=Category.objects.get(pk=1))
# <Ad: something>

Seller.objects.get(pk=1).ads.create(name='Товар 1', category=Category.objects.get(pk=2))
# <Ad: Товар 1>

Seller.objects.get(pk=1).ads.create(name='Товар 2', category=Category.objects.get(pk=3))
# <Ad: Товар 2>

Seller.objects.all()[0].ads.create(name='Что-нибудь', category=Category.objects.get(pk=3))
# <Ad: Что-нибудь>

Seller.objects.all()[0].ads.create(name='Что-нибудь 1', category=Category.objects.get(pk=4))
# <Ad: Что-нибудь 1>

Seller.objects.all()[0].ads.create(name='Что-нибудь 2', category=Category.objects.get(pk=1))
# <Ad: Что-нибудь 2>

Ad.objects.all()
# <QuerySet [<Ad: Что-нибудь 2>, <Ad: Что-нибудь 1>, <Ad: Что-нибудь>, <Ad: Товар 2>, <Ad: Товар 1>, <Ad: something>]>

Seller.objects.all()[1].ads.create(name='some else', category=Category.objects.get(pk=2))
# <Ad: some else>

Seller.objects.all()[1].ads.create(name='some else 1', category=Category.objects.get(pk=3))
# <Ad: some else 1>

Seller.objects.all()[1].ads.create(name='some else 2', category=Category.objects.get(pk=1))
# <Ad: some else 2>

Seller.objects.all()[1].ads.all()[1].tags.set(Tag.objects.all()[0:3])
Seller.objects.all()[1].ads.all()[1].tags.all()
# <QuerySet [<Tag: Другое>, <Tag: Искусство>, <Tag: Наука>]>

Seller.objects.all()[0].ads.all()[0].tags.set(Tag.objects.all()[3:6])
Seller.objects.all()[0].ads.all()[0].tags.all()
# <QuerySet [<Tag: Ремонт>, <Tag: Автолюбителям>, <Tag: Кулинария>]>

Seller.objects.all()[2].ads.all()[2].tags.set(Tag.objects.all()[6:9])
Seller.objects.all()[2].ads.all()[2].tags.all()
# <QuerySet [<Tag: Красота>, <Tag: Хобби>, <Tag: Ретро>]>


Ad.objects.filter(category__name='Садоводство')
# <QuerySet [<Ad: Что-нибудь 1>]>

Ad.objects.filter(category__name='Музыка')
# <QuerySet [<Ad: some else 1>, <Ad: Что-нибудь>, <Ad: Товар 2>]>

Ad.objects.filter(category__name='Одежда')
# <QuerySet [<Ad: some else>, <Ad: Товар 1>]>

Ad.objects.filter(category__name='Книги')
# <QuerySet [<Ad: some else 2>, <Ad: Что-нибудь 2>, <Ad: something>]>
