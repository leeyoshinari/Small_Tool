# CosmoLady
This is used to crawl comments of JD. crawling the CosmoLady JD Self-operated Store.

## OVerview
1. All bras' colors are as follow.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/original%20color.png)

2. Simply combine the colors, as follow.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/combine_color.png)

3. All cups are as follow.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/cups.png)

4. All bust are as follow.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/bust.png)

5. Number of cups under each bust, as follow.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/cups_num%20of%20per%20bust.png)

6. User membership level, as follow.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/userLevel.png)

7. The way users buy is as follow.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/uesrClient.png)

8. User comments of the product (word cloud) is as follow.<br>
   ![](https://github.com/leeyoshinari/Small_Tool/blob/master/CosmoLady/res/word_cloud.png)

9. Comments number of month, as follow.<br>
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
