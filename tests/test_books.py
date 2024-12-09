def test_add_book(client, auth_headers):
    response = client.post('/books', 
        headers=auth_headers,
        json={
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890',
            'quantity': 5
        })
    
    assert response.status_code == 201
    assert response.json['message'] == 'Book added successfully'

def test_get_books_pagination(client, auth_headers):
    # Add multiple books
    books = [
        {'title': f'Book {i}', 'author': f'Author {i}', 
         'isbn': f'ISBN{i}', 'quantity': 5} 
        for i in range(5)
    ]
    
    for book in books:
        client.post('/books', headers=auth_headers, json=book)
    
    # Test first page
    response = client.get('/books?page=1', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['books']) == 2  # ITEMS_PER_PAGE is 2
    assert response.json['total'] == 5
    assert response.json['pages'] == 3
    assert response.json['current_page'] == 1

def test_search_books(client, auth_headers):
    # Add test books
    books = [
        {'title': 'Python Programming', 'author': 'John Doe', 
         'isbn': 'ISBN1', 'quantity': 5},
        {'title': 'Java Basic', 'author': 'Jane Smith', 
         'isbn': 'ISBN2', 'quantity': 3},
        {'title': 'Advanced Python', 'author': 'Bob Wilson', 
         'isbn': 'ISBN3', 'quantity': 2}
    ]
    
    for book in books:
        client.post('/books', headers=auth_headers, json=book)
    
    # Test search by title
    response = client.get('/books?q=Python', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['books']) == 2
    
    # Test search by author
    response = client.get('/books?q=Jane', headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json['books']) == 1 