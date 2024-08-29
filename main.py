import requests 
from bs4 import BeautifulSoup
import csv
import json
"""
        1. First function: Get the HTML layout 
            * Identification of the file:
                - if the file don´t exit of local way, make it
                - But if the file exit of local way, get the content
        2. Get the information
            * Get feature
                - Cast
                - Movies name
                - Categories
        3. Make a CSV file with the HTML layout
"""
URL='https://www.imdb.com/calendar/?ref_=rlm&region=MX&type=MOVIE'

def get_imdb_content():
    """
    This function get a petition to server
    """
    headers={
        'User-Agent': "Mozzila/5.0"
    }
    response= requests.get(URL, headers=headers) #peticion al servidor y su argumento URL
    if response.status_code == 200:
        return response.text
    else:
        return None
    #print(response.status_code)#20X(OK) 30X(Move, redirect) 40X(error's cliente) 50X(error's server)
    #print(response.text) #visualizar el maquetado se almacenara en un archivo txt, para evitar que el servidor piense que es un ataque

def create_imdb_file_local(content):
    """
    This function create a file with a content
    args: Content
    """
    try:
        with open('imdb_test.html', 'w') as file: #este archivo sierve para hacer test de forma local
            file.write(content)
    except:
        pass   

def get_imdb_file_local():
    """
    This function read a file with a content
    args: Content
    """
    content=None
    try:
        with open('imdb_test.html', 'r') as file: #este archivo sierve para hacer test de forma local
            content = file.read()
    except:
        pass 
    return content    

def get_local_imdb_content():
    """
    This function get the content of local way or create file
    """
    content= get_imdb_content()
    if content:
        return content
    else:
        content= get_imdb_content()
        create_imdb_file_local(content)

def create_movie(tag):
    main_div = tag.find('div',{'class':'ipc-metadata-list-summary-item__c'})
    
    movies_name = main_div.div.a.text
    ul_categories = main_div.find_all('ul',{
        'class':"ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__tl base"
    })
    ul_cast = main_div.find_all('ul',{
        'class':"ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base"
    })
    
    categories = []    
    for ul in ul_categories:
        categories.extend([category.span.text for category in ul.find_all('li')])  # Encuentra 'li' en cada 'ul' y extrae el texto

    cast = []    
    for ul in ul_cast:
        cast.extend([casting.span.text for casting in ul.find_all('li')])  
    #print(movies_name.text, '-', ', '.join(categories), '-', ', '.join(cast))
    return(movies_name, categories, cast) #tuple
    
def main():
    """
    Main function
    """
    content= get_imdb_content()
    soup = BeautifulSoup(content, 'html.parser')
    #attributs
    li_tags= soup.find_all('li', {
        'data-testid':"coming-soon-entry",
        'class':"ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-8c2b7f1f-0 dKSSmX"
    })
    movies =[]
    for tag in li_tags:
        movie = create_movie(tag)
        movies.append(movie)
        
    with open('movies.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['movie_name','categories','cast'])
        for movie in movies:
            writer.writerow([
                movie[0], #movie name
                ",".join(movie[1]),#categories
                ",".join(movie[2]) #cast
            ])
    
if __name__ == '__main__':
    main()