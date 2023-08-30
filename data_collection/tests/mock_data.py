from data_structures.story import Story

mock_api_response = {
    "status": "ok",
    "totalResults": 3, 
    "articles": [
        {
            "source": {
                "id": "fauxnews",
                "name": "FauxNews", 
            }, 
            "author": "John Doe",
            "title": "title",
            "description": "description",
            "url": "www.example.com",
            "urlToImage": "www.example.com/image",
            "publishedAt": "2023-01-01T16:51:12Z",
            "content": "text..."
        }, {
            "source": {
                "id": "fauxnews",
                "name": "FauxNews", 
            }, 
            "author": "John Doe",
            "title": "title",
            "description": "description",
            "url": "www.example.com",
            "urlToImage": "www.example.com/image",
            "publishedAt": "2023-01-01T16:51:12Z",
            "content": "text..."
        }, {
            "source": {
                "id": "fauxnews",
                "name": "FauxNews", 
            }, 
            "author": "John Doe",
            "title": "title",
            "description": "description",
            "url": "www.example.com",
            "urlToImage": "www.example.com/image",
            "publishedAt": "2023-01-01T16:51:12Z",
            "content": "text..."
        }       
    ]
}

expected_stories = [
    # Should correspond to mock_api_response.json
    Story(
        source="fauxnews",
        title="title",
        url="www.example.com",
        article_text="Lorem ipsum",
        date="2023-01-01"
    ), Story(
        source="fauxnews",
        title="title",
        url="www.example.com",
        article_text="Lorem ipsum",
        date="2023-01-01"
    ),  Story(
        source="fauxnews",
        title="title",
        url="www.example.com",
        article_text="Lorem ipsum",
        date="2023-01-01"
    )
]