import requests
from bs4 import BeautifulSoup
import pandas as pd

# 전체 페이지 수를 알아내기 위한 함수
def get_total_pages():
    url = 'http://books.toscrape.com/catalogue/page-1.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pager = soup.find('li', class_='current')
    total_pages = int(pager.text.strip().split()[-1])
    return total_pages

# 각 책의 정보를 가져오기 위한 함수
def get_book_info(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 제목
    title = soup.find('h1').text
    
    # 카테고리
    category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
    
    # 가격
    price = soup.find('p', class_='price_color').text.strip()
    
    # 별점
    rating = soup.find('p', class_='star-rating')['class'][1]
    
    # 재고상황
    stock = soup.find('p', class_='instock availability').text.strip()
    
    return {
        'Title': title,
        'Category': category,
        'Price': price,
        'Rating': rating,
        'Stock': stock
    }

# 책 리스트를 가져오기 위한 함수
def get_books_from_page(page_num):
    url = f'http://books.toscrape.com/catalogue/page-{page_num}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    
    book_infos = []
    for book in books:
        book_url = 'http://books.toscrape.com/catalogue/' + book.find('h3').find('a')['href']
        book_info = get_book_info(book_url)
        book_infos.append(book_info)
        
        # 진행 상황 출력
        print(f"Processed: {book_info['Title']}")
    
    return book_infos

def main():
    # 전체 페이지 수 가져오기
    total_pages = get_total_pages()
    
    all_books = []
    for page_num in range(1, total_pages + 1):
        print(f"Processing page {page_num} of {total_pages}")
        books = get_books_from_page(page_num)
        all_books.extend(books)
    
    # 데이터프레임으로 변환
    df = pd.DataFrame(all_books)
    
    # CSV 파일로 저장
    df.to_csv('books.csv', index=False, encoding='utf-8')
    print("CSV 파일로 저장 완료!")

if __name__ == '__main__':
    main()
