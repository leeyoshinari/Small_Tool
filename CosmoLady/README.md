# CosmoLady
This is used to crawl comments of JD. Crawling the CosmoLady JD Self-operated Store. <br>
75 bras are crawlled. And 18183 comments are saved to MySQL. Through analysis, cups and  colors of women's favorite are known.

## Overview
1. All bras' colors are as follow. A total of 52 colors. As can be seen from the figure, women prefer bras with black and skin color.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/original%20color.png)

2. Simply combine the colors, as follow. Black bras account for more than 1/4, skin bras account for more than 1/5, followed by red and pink bras. From the picture, it's gussed that almost women have black, skin, red and pink bras.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/combine_color.png)

3. All cups are as follow. More than 80% of women are A or B cups. It can be said that most women in China are small breasts.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/cups.png)

4. All bust are as follow. The under bust girth of the women are mainly distributed at 75cm and 80cm. Moreover, the number of the 70cm and 85cm, and, the number of 75cm and 80cm are basically the same. It is possible to say that the average under bust girth of the women is 77.5cm.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/bust.png)

5. Number of cups under each bust, as follow. It can be seen again from the figure that the Chinese women's chest is small. The 70C and 75D of women whoes body should be pretty good.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/cups_num%20of%20per%20bust.png)

6. User membership level, as follow. The PLUS membership is more.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/userLevel.png)

7. The way users buy bras is as follow. "Other" should be a web version. It can also be seen that the Jingdong's client installation rate is still relatively high.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/uesrClient.png)

8. User comments of the product (word cloud) is as follow. Overall, the comment is good.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/word_cloud.png)

   Some of the comments included the field “Buy for Wife (Girlfriends)”. By looking up the keywords, a total of 839 comments were found, accounting for 4.6%. In the same way, there is also “husband (boyfriend) feels very good” in the comments. By looking up the keywords, a total of 33 comments (so few, probably most women did not write) were found, accounting for 0.18%.<br>
   
9. Comments number of month, as follow. Because JD cannot display all the comments, the longer the time, the more inaccurate the data, but the data in recent months can still be referenced. As can be seen from the picture, as we approach the New Year, the sales volume is quite high.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/comments%20of%20month.png)

## Usage
1. clone CosmoLady repository
   ```shell
   git clone https://github.com/leeyoshinari/Small_Tool.git
   
   cd Small_Tool/CosmoLady
   ```

2. set the MySQL's `username` and `password`, etc.

3. run
   ```shell
   python SpiderBar.py
   ```
   
## Requirements
1. requests
2. pymysql
