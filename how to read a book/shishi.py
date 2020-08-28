import re
from bs4 import BeautifulSoup
str1 = '''
<li>
    <div class="list_num ">9.</div>   
    <div class="pic"><a href="http://product.dangdang.com/28470980.html" target="_blank"><img src="http://img3m0.ddimg.cn/65/35/28470980-1_l_5.jpg" alt="阴谋与爱情"  title="阴谋与爱情"/></a></div>    
    <div class="name"><a href="http://product.dangdang.com/28470980.html" target="_blank" title="阴谋与爱情">阴谋与爱情</a></div>    
    <div class="star"><span class="level"><span style="width: 89%;"></span></span><a href="http://product.dangdang.com/28470980.html?point=comment_point" target="_blank">68498条评论</a><span class="tuijian">100%推荐</span></div>    
    <div class="publisher_info">[德]<a href="http://search.dangdang.com/?key=J・B・卞若琳" title="[德]J・B・卞若琳 著，纳青苗/李倩 译" target="_blank">J・B・卞若琳</a> 著，<a href="http://search.dangdang.com/?key=纳青苗" title="[德]J・B・卞若琳 著，纳青苗/李倩 译" target="_blank">纳青苗</a>/<a href="http://search.dangdang.com/?key=李倩" title="[德]J・B・卞若琳 著，纳青苗/李倩 译" target="_blank">李倩</a> 译</div>    
    <div class="publisher_info"><span>2019-06-30</span>&nbsp;<a href="http://search.dangdang.com/?key=天津人民出版社" target="_blank">天津人民出版社</a></div>    

            <div class="biaosheng">五星评分：<span>65729次</span></div>
                      
    
    <div class="price">        
        <p><span class="price_n">&yen;30.30</span>
                        <span class="price_r">&yen;39.80</span>(<span class="price_s">7.6折</span>)
                    </p>
                    <p class="price_e"></p>
                <div class="buy_button">
                          <a ddname="加入购物车" name="" href="javascript:AddToShoppingCart('28470980');" class="listbtn_buy">加入购物车</a>
                        
                        <a ddname="加入收藏" id="addto_favorlist_28470980" name="" href="javascript:showMsgBox('addto_favorlist_28470980',encodeURIComponent('28470980&platform=3'), 'http://myhome.dangdang.com/addFavoritepop');" class="listbtn_collect">收藏</a>
     
        </div>

    </div>
  
    </li> 
'''

# <li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)" alt="(.*?)".*?<span class="tuijian">(.*?)</span>.*?<div class="publisher_info">.*?target="_blank">(.*?)</a>.*?<div class="publisher_info"><span>(.*?)</span>&nbsp.*?<span class="price_n">&yen;(.*?)</span>.*?<li>

# pattern = re.compile(
#     '<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)" alt="(.*?)".*?<span class="tuijian">(.*?)</span>.*?<div class="publisher_info">.*?target="_blank">(.*?)</a>.*?<div class="publisher_info"><span>(.*?)</span>&nbsp.*?<span class="price_n">&yen;(.*?)</span>.*?</li>',re.S)
# items = re.findall(pattern, str1)
# print(items)
soup = BeautifulSoup(str1,'lxml')
print(soup.a.string)

