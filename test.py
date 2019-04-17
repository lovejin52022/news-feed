
from newspaper import Article

article = Article('http://biofuelsdigest.com/nuudigest/2018/11/14/air-bp-invests-in-upgraded-terminal-to-deliver-biofuel/')
article.download()
article.parse()

print(article.title)
