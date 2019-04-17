# -*- coding: utf-8 -*-

from .items import NewsSpiderItem
from newspaper import Article

def common_parse_content(url, body, language='en', fetch_images=True):
    article = Article(url, language=language, keep_article_html=True, fetch_images=fetch_images)
    article.set_html(body)
    article.parse()
    item = NewsSpiderItem(
        title=article.title,
        content=article.text,
        tags=list(article.tags),
        images=article.images,
        movies=article.movies,
        authors=article.authors,
        publish_date=article.publish_date,
        meta_lang=article.meta_lang,
        article_html=article.article_html,
        link_hash=article.link_hash,
        source_url=article.source_url,
        url=article.url
    )
    return item
