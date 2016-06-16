# -*- coding: utf-8 -*-
import re

from ..container.page import Page
from config import Config
from match import Match
from template_config import TemplateConfig
from type import Type


class HtmlCreator(object):
    u"""
    工具类，用于生成html页面
    """

    def __init__(self, image_container):
        self.image_container = image_container
        return

    def fix_image(self, content, recipe):
        content = Match.fix_html(content=content, recipe_kind=recipe)
        for img in re.findall(r'<img[^>]*', content):
            if recipe not in [Type.sinablog_author, Type.cnblogs_author]:
                # fix img
                if img[-1] == '/':
                    img = img[:-1]
            img += '>'
            src = re.search(r'(?<=src=").*?(?=")', img)
            if not src:
                new_image = img + '</img>'
                content = content.replace(img, new_image)
                continue
            else:
                src = src.group(0)
                if src.replace(' ', '') == '':
                    new_image = img + '</img>'
                    content = content.replace(img, new_image)
                    continue
            src_download = HtmlCreator.fix_image_src(src)
            if src_download:
                if recipe in Type.zhihu and not src_download.startswith('http'):
                    # fix zhuanlan image href
                    src_download = src_download.split('.')[0]
                    filename = self.image_container.add('https://pic2.zhimg.com/'+src_download+'_b.jpg')
                elif recipe in Type.generic:
                    filename = ''    # TODO
                else:
                    filename = self.image_container.add(src_download)
            else:
                filename = ''
            new_image = img.replace('"{}"'.format(src), '"../images/{}"'.format(filename))

            if recipe in Type.jianshu:
                new_image = new_image.replace('data-original-src', 'temppicsr')
                new_image = new_image.replace('src', 'falsesrc')
                new_image = new_image.replace('temppicsr', 'src')    # 应该有更好的方式, 暂时先这样写
                new_image += '</img>'
            elif recipe in Type.sinablog:
                # 硬编码, 可以优化?写到fix_html函数中
                new_image = new_image.replace('http://simg.sinajs.cn/blog7style/images/common/sg_trans.gif',\
                                          '../images/{}'.format(filename))
            elif recipe in Type.zhihu:
                new_image = new_image.replace('//zhstatic.zhihu.com/assets/zhihu/ztext/whitedot.jpg',
                                              '../images/{}'.format(filename))
                new_image += '</img>'
            elif recipe in Type.cnblogs:
                pass
            content = content.replace(img, '<div class="duokan-image-single">{}</div>'.format(new_image))

        return content

    @staticmethod
    def fix_image_src(href):
        if Config.picture_quality == 0:
            return ''
        if 'equation?tex=' in href:  # tex图片需要额外加上http协议头
            if not 'http:' in href:
                href = 'http:' + href
            return href
        if Config.picture_quality == 1:
            return href
        if Config.picture_quality == 2:
            if not ('_' in href):
                return href
            pos = href.rfind('_')
            return href[:pos] + href[pos + 2:]  # 删除'_m'等图片质量控制符，获取原图
        return href

    def create_comment_info(self, comment_info):
        template = self.get_template('info', 'comment')
        return template.format(**comment_info)

    def create_author_info(self, author_info):
        template = self.get_template('info', 'author')
        return template.format(**author_info)

    def wrap_title_info(self, title_image='', title='', description='', **kwargs):
        title_info = {
            'title_image': title_image,
            'title': title,
            'description': description,
        }
        return title_info

    def create_title_info(self, title_info):
        template = self.get_template('info', 'title')
        return template.format(**title_info)

    def create_answer(self, answer):
        result = {
            'author_info': self.create_author_info(answer),
            'comment': self.create_comment_info(answer),
            'content': answer['content']
        }
        template = self.get_template('question', 'answer')
        return template.format(**result)

    def create_question(self, package, prefix=''):
        question = package['question']
        answer_content = ''.join([self.create_answer(answer) for answer in package['answer_list']])
        title_info = self.wrap_title_info(**question)
        question['answer'] = answer_content
        question['question'] = self.get_template('info', 'title').format(**title_info)
        result = {
            'body': self.get_template('question', 'question').format(**question),
            'title': question['title'],
        }

        content = self.get_template('content', 'base').format(**result)
        page = Page()
        page.content = self.fix_image(content, recipe="question")
        page.filename = str(prefix) + '_' + str(question['question_id']) + '.xhtml'
        page.title = question['title']
        return page

    def create_article(self, article, prefix='', recipe=None):
        article['edit_date'] = article['publish_date']
        article['description'] = ''
        # TODO: 改掉硬编码
        if str(recipe) in (Type.sinablog+Type.jianshu+Type.csdnblog+Type.cnblogs):
            article['agree'] = u'暂无数据'
        result = {
            'answer': self.create_answer(article),
            'question': self.get_template('info', 'title').format(**article)
        }
        question = self.get_template('question', 'question').format(**result)
        result = {
            'body': question,
            'title': article['title'],
        }
        content = self.get_template('content', 'base').format(**result)
        page = Page()
        page.content = self.fix_image(content, recipe)
        page.filename = str(prefix) + '_' + str(article['article_id']) + '.xhtml'
        page.title = article['title']
        return page

    def wrap_front_page_info(self, kind, info):
        result = {}
        if kind == Type.csdnblog_author:
            result['title'] = u'csdn博客集锦'
            result['description'] = u''
        elif kind == Type.jianshu_author:
            result['title'] = u'简书文章集锦'
            result['description'] = u''   # TODO: description
        elif kind == Type.sinablog_author:
            result['title'] = u'新浪博客集锦'
            result['description'] = u''
        elif kind == Type.cnblogs_author:
            result['title'] = u'csblogs文章集锦'
            result['description'] = u''
        elif kind == Type.answer:
            result['title'] = u'知乎回答集锦'
            result['description'] = u''
        elif kind == Type.question:
            result['title'] = u'知乎问题集锦'
            result['description'] = u''
        elif kind == Type.article:
            result['title'] = u'知乎文章集锦'
            result['description'] = u''
        elif kind == Type.author:
            result['title'] = u'知乎_{name}的知乎回答集锦({author_id})'.format(**info)
        elif kind == Type.collection:
            result['title'] = u'知乎_收藏夹_{title}({collection_id})'.format(**info)
        elif kind == Type.column:
            result['title'] = u'知乎_{creator_name}的专栏_{name}({column_id})'.format(**info)
        elif kind == Type.topic:
            result['title'] = u'知乎_话题_{title}({topic_id})'.format(**info)
        return result

    def create_info_page(self, book):
        kind = book.kind
        info = book.info
        extend = self.wrap_front_page_info(kind, info)
        info.update(extend)
        result = {
            'detail_info': self.get_template('front_page', kind).format(**info),
            'title': info['title'],
            'description': info['description'],
        }
        result = {
            'title': info['title'],
            'body': self.get_template('front_page', 'base').format(**result),
        }
        content = self.get_template('content', 'base').format(**result)
        page = Page()
        page.content = self.fix_image(content, recipe=book.kind)
        page.filename = str(book.epub.prefix) + '_' + 'info.xhtml'
        page.title = book.epub.title
        if book.epub.split_index:
            page.title += "_({})".format(book.epub.split_index)
        return page

    def get_template(self, kind, name):
        file_path = getattr(TemplateConfig, "{}_{}_uri".format(kind, name))
        with open(file_path) as template:
            content = template.read()
        return content
