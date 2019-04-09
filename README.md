# Hi10Anime-Download

Download Anime from [Hi10Anime](hi10anime.com) using Python


## How To Use

1) Install these modules :
    - selenium
    - requests
    - bs4

2) Download [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
   ```
   Make sure that the ChromeDriver version is same as your Chrome Browser version

   Put the .exe file in the same directory
   ```
3) Open cmd and run the script in this format

   >python Hi10Anime.py `username/email` `password` `anime name/id` `optional argument`
    ```
    anime name is the anime you want to download
        
        It finds all the animes under the given search query. 
        So if you are only looking for something sppecific then make your search query more specific. 
    
    anime id is the id of the anime page. 
       
        You can get it by going to that page on the website and then copying the numbers at the end of the url.
        The page looks like hi10anime.com/archives/1234 , 1234 being the anime id
        If you input the anime id then it would only download from that specfic page

    optional argument is the specification of the way you want the links
      
      if you type 'idm' then the download links gets added in the idm queue
      
      if you type 'txt' then it creats a text file, with all the download links, in the script directory.
      You can use those links to download the files in anyway you want
    ```
  
## To-Do

- get links for different seasons, ovas etc in same page
- check for other qualities (currently checks [1080p, 720p, 480p] in this order)
- search more pages
- download from old 'ddl' format like [this](https://hi10anime.com/archives/16951) [this](https://hi10anime.com/archives/44)
