dict_data = {
'http://netnews.vn':
[
    '//h1[@class="tn-detail-h1"]',
    ['//div[@class="detail-content"]//p'],
    '//div[@class="social-detail"]/p[@class="left-item-time"]/span[@class="sp-time"]',
    '//p[@class="p-tag-tn"]//a'
],
'http://www.baohaugiang.com.vn':
[
    '//h1[@class="view-page-Tit"]',
    ['//div[@class="divDetail newscontent"]//p'],
    '//div[@class="date"]',
    ''
],
'https://vietnammoi.vn':
    ['//h1[@id="title-article"]',
    ['//div[@class="sapo margin-20-bottom"]', '//div[@class="entry-body"]//p'],
    '//span[@class="time left"]/span',
    ''
],
'https://m.moitruongvadothi.vn':
    ['//div[@class="title_detail"]',
    ['//div[@class="sapo_news"]', '//div[@id="main-detail"]//p'],
    '//div[@class="fontnotiR f13 clearfix mar_bottom5"]/span[@class="time_home cl999"]',
    '//div[@class="tag_detail mar_bottom20"]//a'
],
'http://giadinh.net.vn':
    ['//h1[@data-field="title"]',
    ['//h2[@class="detail-sp"]', '//div[@class="content-new clear"]//p'],
    '//div[@class="title-detail"]/p/span',
    '//div[@class="tags"]//a'
],
'https://vn.sputniknews.com':
    ['//h1[@itemprop="headline"]',
    ['//div[@class="b-article"]//div[@class="b-article__lead"]//p', '//div[@class="b-article"]//div[@class="b-article__text"]//p'],
    '//time[@class="b-article__refs-date"]',
    '//div[@class="tags"]//a'
],
'https://eva.vn':
    ['//h1[@class="bvtit tuht_show"]/span[@class="clrTit bld"]',
    ['//div[@class="nsSap sap clrF"]//h2//span', '//div[@id="baiviet-container"]//div[@class="b-article__text"]//a'],
    '//div[@class="pubDte pdB10 pdT5"]/span[@class="clrGre"]',
    ''
],
'https://cungcau.vn':
    ['//div[@class="single"]//h1',
    ['//div[@class="single"]//div[@class="sapo"]', '//div[@class="single"]//div[@id="content"]//p'],
    '//div[@class="single"]//p[@class="author"]//span',
    '//div[@class="tags"]//ul//li//a'
],
'https://tuoitre.vn':
    ['//h1[@class="article-title"]',
    ['//div[@class="main-content-body"]//h2[@class="sapo"]', '//div[@id="main-detail-body"]//p'],
    '//div[@class="date-time"]',
    '//ul[@class="tags-wrapper"]//li//a'
],
'https://baoquocte.vn':
    ['//h1[@class="titleDetailNews"]',
    ['//h3[@class="f-16"]//strong','//div[@class="viewsDtailContent"]//p'],
    '//span[@class="format_time"]',
    '//ul[@class="tagsCould"]//li'
],
'https://vietnamnet.vn':
    ['//h1[@class="title f-22 c-3e"]',
    ['//div[@id="ArticleContent"]//div[@class="bold ArticleLead"]//h2', '//div[@id="ArticleContent"]//p'],
    '//span[@class="ArticleDate  right"]',
    '//ul[@class="clearfix"]//li'
],
'https://cuocsongantoan.vn':
    ['//h1[@class="post-title"]',
    ['//div[@class="post-sapo fw lt clearfix"]','//div[@class="fw lt clearfix"]//p'],
    '//span[@class="format_time"]',
    '//div[@class="post-tag fw lt clearfix"]//a'
],
'https://thanhnien.vn':
    ['//h1[@class="details__headline"]',
    ['//div[@id="chapeau"]','//div[@id="abody"]'],
    '//div[@class="details__meta"]//div[@class="meta"]//time',
    '//div[@class="details__tags"]//a'
],
'https://www.tinmoi.vn':
    ['//h1[@class="mb-4 post--title"]',
    ['//h2[@class="sapo mb-3"]','//div[@id="main-detail"]//p'],
    '//div[@class="post-time"]',
    '//div[@class="details__tags"]//a'
],
'https://vov.vn':
[
    '//div[@class="article__header"]//h2',
    ['//div[@class="article__sapo"]','//div[@id="article-body"]//p'],
    '//div[@class="article__meta"]//time',
    '//div[@class="article__tag"]//div[@class="box-content"]//a'
],
'https://baotintuc.vn':
    ['//h1[@class="title"]',
    ['h2[@class="sapo"]', '//div[@class="boxdetail"]//p'],
    '//div[@class="time"]',
    '//div[@class="tagname"]//a'
],
'https://news.zing.vn':
    ['//h1[@class="the-article-title"]',
    ['//p[@class="the-article-summary"]', '//div[@class="the-article-body"]//p'],
    '//li[@class="the-article-publish"]',
    '//p[@class="the-article-tags"]//a'
],
'http://kinhtedothi.vn':
    ['//h1[@class="title_detail_news"]',
    ['//div[@class="sapo_detail fr"]', '//div[@id="cotent_detail"]//div'],
    '//div[@class="time_detail_news f11 fl"]',
    '//div[@class="tag_detail mar_bottom15"]//a'
],
'https://vietnambiz.vn':
[
    '//h1[@class="vnbcb-title"]',
    ['div[@class="vnbcbc-sapo"]', '//div[@id="vnb-detail-content"]//p'],
    '//span[@class="vnbcbat-data "]',
    '//ul[@class="vnbcbcbst-ul"]//li//a'
],
'https://bnews.vn':
[
    '//div[@class="post-top-entry"]//h1',
    ['//div[@class="post-summary"]', '//div[@class="post-ct-entry"]//p'],
    '//div[@class="uk-width-expand@m uk-width-1-1 uk-first-column"]//span[@class="post-time"]',
    '//ul[@class="post-tags"]//li//a'
],
'https://baotainguyenmoitruong.vn':
[
    '//h1[@class="c-detail-head__title"]',
    ['//b[@class="fixh22"]', '//div[@class="b-maincontent"]//p'],
    '//div[@class="c-detail-head__time"]',
    '//div[@class="c-tags"]//ul//li//a'
],
'http://dangcongsan.vn':
[
    '//h1[@class="post-title"]',
    ['//div[@class="post-summary"]//h2', '//div[@itemprop="articleBody"]//p'],
    '//div[@class="col-md-6 col-sm-12 lbPublishedDate"]',
    ''
],
'https://thethaovanhoa.vn':
[
    '//div[@class="divContent"]//h1',
    ['//div[@id="divcontentwrap"]//div'],
    '//div[@class="ovh pub_time"]',
    '//div[@class="ovh tag_dtl"]//ul//li//a'
],
'https://kenh14.vn':
[
    '//h1[@class="kbwc-title"]',
    ['//h2[@class="knc-sapo"]', '//div[@class="knc-content"]//p'],
    '//span[@class="kbwcm-time"]',
    '//ul[@class="knt-list"]//li//a'
],
'https://laodong.vn':
[
    '//div[@class="title"]//h1',
    ['//p[@class="abs"]', '//div[@class="article-content"]//p'],
    '//time[@class="f-datetime"]',
    '//span[@class="keywords"]//a'
],
'https://soha.vn':
[
    '//h1[@class="news-title"]',
    ['//h2[@class="news-sapo"]', '//div[@class="clearfix news-content"]//p'],
    '//time[@class="op-published"]',
    '//div[@class="clearfix mgt20 tags"]//h3//a'
],
'https://forbesvietnam.com.vn':
[
    '//div[@class="box-title"]//h4',
    ['//div[@class="sapo_detail cms-desc"]//p', '//div[@id="wrap-detail"]//p'],
    '//ul[@class="first-li"]',
    '//div[@class="tu-khoa"]//ul//li//a'
],
'https://www.thegioididong.com':
[
    '//h1[@class="titledetail"]',
    ['//article//h2', '//article//p'],
    '//div[@class="userdetail"]//span',
    ''
],
'http://nguoilambao.vn':
[
    '//h1[@class="title"]',
    ['//div[@class="summary"]//h2', '//div[@class="description"]//p'],
    '//div[@class="news-detail"]//div[@class="info"]',
    '//div[@class="tags"]//a'
],
'http://cadn.com.vn':
[
    '//div[@id="contentnew"]//h1//span',
    ['//div[@class="content"]//p'],
    '//span[@class="lbTime"]',
    '//span[@id="ctl00_ContentPlaceHolder1_lblGetTag"]//a'
],
'https://nld.com.vn':
[
    '//h1[@class="title-content"]',
    ['//h2[@class="sapo-detail"]', '//div[@class="contentbody"]//p'],
    '//span[@class="pdate fl"]',
    '//div[@class="listtags"]//ul//li//a'
],
'https://www.thiennhien.net':
[
    '//h1[@class="entry-title"]',
    ['//div[@class="td-post-content tagdiv-type"]//p'],
    '//time[@class="entry-date updated td-module-date"]',
    '//ul[@class="td-tags td-post-small-box clearfix"]//li//a'
],
'http://www.hanoimoi.com.vn':
[
    '//h1[@class="caption"]',
    ['//div[@class="article"]//p'],
    '//div[@class="definfo"]//div[@class="period"]',
    '//div[@class="taglist"]//a'
],
'https://cuocsongantoan.vn':
[
    '//h1[@class="bx-post-title"]',
    ['//div[@class="bx-desc"]', '//div[@class="__MB_CONTENT fw lt clearfix"]//p'],
    '//span[@class="format_time"]',
    '//div[@class="post-tag fw lt clearfix"]//a'
],
'http://hanoitv.vn':
[
    '//div[@class="title_detail_news"]',
    ['//div[@class="sapo_detail"]', '//div[@class="story-body article"]//p'],
    '//span[@class="cl888 f14"]//span[@class="fa fa-clock-o"]',
    '//div[@class="word"]//a'
],
'https://www.ntdvn.com':
[
    '//div[@class="post_title"]/h1',
    ['//article[@class="post_content"]//p'],
    '//span[@class="publish"]',
    '//div[@class="pricat_name"]//a'
],
'https://vnexpress.net':
[
    '//h1[@class="title-detail"]',
    ['//p[@class="description"]', '//article[@class="fck_detail"]//p'],
    '//span[@class="date"]',
    '//div[@class="tags"]//h2//a'
],
'https://cafebiz.vn':
[
    '//h1[@class="title"]',
    ['//h2[@class="sapo"]', '//div[@class="detail-content"]//p'],
    '//div[@class="timeandcatdetail"]//span[@class="time"]',
    '//span[@class="tags-item"]//a'
],
'https://plo.vn':
[
    '//h1[@class="main-title cms-title"]',
    ['//div[@class="sapo cms-desc"]//div', '//div[@id="abody"]//p'],
    '//div[@class="meta clearfix"]//time',
    '//ul[@class="tags"]//li'
],
'https://haiquanonline.com.vn':
[
    '//h1[@class="detail-title"]',
    ['//p[@class="detail-sapo"]', '//div[@id="__MB_MASTERCMS_EL_3"]//p'],
    '//span[@class="datetime"]',
    '//div[@class="category tags clearfix"]//a'
],
'http://daidoanket.vn':
[
    '//div[@class="txtNewsDetail fl w100pt"]//h1',
    ['//div[@class="txtNewsDetail fl w100pt"]//strong', '//div[@class="left content-newsTxt"]//p'],
    '//div[@class="left time-day"]',
    '//div[@class="fl w100pt list-tab-detai"]//ul//li//a'
],
'https://www.tinmoi.vn':
[
    '//h1[@class="mb-4 post--title"]',
    ['//h2[@class="sapo mb-3"]', '//div[@id="main-detail"]//p'],
    '//div[@class="post-time"]',
    '//div[@class="tags-box mt-3 py-3 border-top"]//a'
],
'http://baodansinh.vn':
[
    '//h1[@class="title m-30-b"]',
    ['//h2[@class="detail-sapo m-20-b"]', '//div[@class="entry-body m-30-b clearafter dtdefault"]//p'],
    '//div[@class="info-time"]',
    '//ul[@class="detail-tags"]//li//a'
],
'https://vtv.vn':
[
    '//h1[@class="title_detail"]',
    ['//h2[@class="sapo"]', '//div[@id="entry-body"]//p'],
    '//span[@class="time"]',
    '//div[@class="news_keyword"]//a'
],
'https://www.tienphong.vn':
[
    '//h1[@id="headline"]',
    ['//p[@class="article-sapo cms-desc"]', '//div[@id="article-body"]//p'],
    '//p[@class="byline-dateline"]//time',
    '//div[@class="article-tags"]//p//a'
],
'https://www.vietnamplus.vn':
[
    '//h1[@class="details__headline cms-title"]',
    ['//div[@class="details__summary cms-desc"]', '//div[@class="content article-body cms-body AdAsia"]//p'],
    '//div[@class="source"]//time',
    '//div[@class="tags"]//a'
],
'http://baoquangninh.com.vn':
[
    '//h1[@id="title"]',
    ['//div[@id="content"]//p'],
    '//div[@id="date"]',
    ''
],
'http://www.bienphong.com.vn':
[
    '//h1[@class="bp-detail-content-title-h1"]',
    ['//p[@class="bp-detail-sapo"]', '//div[@class="bp-detail-text-content"]//p'],
    '//span[@class="bp-date-time"]',
    ''
],
'http://vncdc.gov.vn':
[
    '//div[@class="detail_new"]//h1',
    ['//div[@class="detail_new"]//p', '//div[@class="bp-detail-text-content"]//p'],
    '//div[@class="detail_new"]//h1//span',
    ''
],
'https://moh.gov.vn':
[
    '//h3[@class="text-change-size"]',
    ['//div[@class="journal-content-article"]//p', '//div[@class="bp-detail-text-content"]//p'],
    '//p[@class="time-post text-change-size"]',
    ''
],
'https://ncov.moh.gov.vn':
[
    '//h3[@class="header-title"]//span',
    ['//div[@class="journal-content-article"]//p'],
    '//span[@class="text-ngayxam-page"]',
    ''
],
'https://baoquocte.vn':
[
    '//h1[@class="titleDetailNews"]',
    ['//div[@class="padB10"]', '//div[@class="viewsDtailContent"]//p'],
    '//span[@class="format_time"]',
    '//ul[@class="tagsCould"]//li//a'
],
'https://nhandan.com.vn':
[
    '//div[@class="item-container"]//h3',
    ['//div[@class="item-container"]//p'],
    '//h5[@class="date-created"]',
    ''
],
'https://thuvienphapluat.vn':
[
    '//div[@class="col-lg-9 col-md-9 col-sm-9 col-xs-12"]//h1',
    ['//div[@class="newcontent"]//p'],
    '//div[@class="col-lg-9 col-md-9 col-sm-9 col-xs-12"]/span',
    '//div[@class="tag-pos"]//a'
],
}
