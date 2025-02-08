document.addEventListener('DOMContentLoaded', function() {
    fetch('books.json')
        .then(response => response.json())
        .then(data => {
            const bookContainer = document.getElementById('book-container');
            Object.keys(data).forEach(category => {
                const categoryElement = document.createElement('div');
                const categoryTitle = document.createElement('h1');
                categoryTitle.textContent = `${category.charAt(0).toUpperCase() + category.slice(1)} Books`;
                categoryElement.appendChild(categoryTitle);

                data[category].forEach(book => {
                    const bookElement = document.createElement('div');
                    bookElement.classList.add('book');

                    const titleElement = document.createElement('h2');
                    titleElement.textContent = `Title: ${book.title}`;
                    bookElement.appendChild(titleElement);

                    if (book.image) {
                        const imageElement = document.createElement('img');
                        imageElement.src = book.image;
                        imageElement.alt = `${book.title} cover`;
                        bookElement.appendChild(imageElement);
                    }

                    const contentElement = document.createElement('p');
                    contentElement.textContent = book.content;
                    bookElement.appendChild(contentElement);

                    if (book.flipbook) {
                        const flipbookLink = document.createElement('a');
                        flipbookLink.href = `${book.flipbook}/index.html`;
                        flipbookLink.textContent = "View Flipbook";
                        flipbookLink.target = "_blank";
                        bookElement.appendChild(flipbookLink);
                    }

                    categoryElement.appendChild(bookElement);
                });

                bookContainer.appendChild(categoryElement);
            });
        })
        .catch(error => console.error('Error fetching books:', error));
});
