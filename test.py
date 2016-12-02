#encoding: utf-8
from app.models import User, session, Message, Grade, Article, ArticleToUser, Comment
from flask import url_for
from app import bbs_app
from datetime import datetime
import json

if __name__ == '__main__':
    u = User.getById(1)
    u.priv = 'teacher'
    uu = User.getById(2)
    uu.group_id = 3
    base_score = 80
    res = session.query(Grade).all()
    for t in res:
        t.name = u'习习蛤蛤'
        t.teacher_id = 1
    al = session.query(Article).all()
    for a in al:
        a.title = u'视察二院'
        a.author_id = 1 
        a.tags = json.dumps([u'个人的奋斗', u'历史的行程'])
        a.intro = u'''
            我的经历就是到了上海， 到了89年的年初的时候， 我在想我估计是快要离休了，
            我想我应该去当教授。 于是我就给朱物华校长、张钟俊院长， 给他们写了一个报告。
            他们说欢迎你来， 不过这个Apply for Professor...
        '''
        a.content = u"""
           我的经历就是到了上海，到了89年初的时候，我在想我估计也快离休了，我想我应该去当教授。
人呐就都不知道，自己不可以预料，一个人的命运啊，当然要靠自我奋斗，但是也要考虑历史的行程。我绝对不知道，我作为一个上海市委书记怎么把我选到北京去了。
所以邓小平同志同我讲话，说“中央都决定了，你来当总书记”。我说另请高明吧，我实在也不是谦虚。我一个上海市委书记怎么到北京来了呢？但是，小平同志讲“大家已经研究决定了”。后来我念了两首诗，叫“苟利国家生死以，岂因祸福避趋之”。
所以我就到了北京，到了北京我干了这十几年也没有什么别的，大概三件事。一个，确立了社会主义市场经济；第二个，把邓小平理论列入党章；第三个，就是“三个代表”。如果说还有一点成绩就是军队一律不得经商。这个对军队的命运有很大的关系，因为我后来又干了一年零八个月，等于说我在部队干了15年军委主席，还有98年的抗洪也是很大的。但是这些都是次要的，我主要的就是三件事情。很惭愧，就做了一点微小的工作，谢谢大家！ 
        """
    c = Comment()
    c.user_id = 2
    c.article_id = 1
    c.content = u"现在的年轻人整天习习蛤蛤， 胡搞毛搞， 长大了都没出习"
    session.add(c)
    c2 = Comment()
    c2.user_id = 4
    c2.article_id = 1
    c2.content = u"江来报道要是除了偏差， 你们是要负泽任的， 民不民白？"
    session.add(c2)

    session.commit()
    


