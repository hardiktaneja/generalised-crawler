**Python Flask App: Intelligent E-commerce Website Crawler**

**Steps to run:**
1. ```pip3 install -r requirements.txt```
2. ```export OPENAI_API_KEY="YOUR_OPEN_AI_API_KEY"```
3. ```python3 -m flask run```

curl of the API to begin the crawl:
```curl --location 'localhost:5000/crawl-website?url=https%3A%2F%2Fwww.flipkart.in%2F'```

**Problems Solved:**
This crawler takes URL as input, and makes a directory "custom-data-directory-{uuid}" in this, the "default" folder contains the Product URLs for the website.
- Multiple Websites can be crawled simultaneously.
- Intelligently identifies the pattern in product URL like (e.g., /product/, /item/, /p/).
- Filters out the product URLs and saves them in sequential files.
- Takes care of infinite scrolling pages

**Approach:**
1. Crawl the input website initially and gather a few hundered URLs.
2. Use AI to figure out the pattern in URLs - I used GPT 4o Mini coupled with LlamaIndex Structured Output
3. Find the regex pattern in the URLs.
4. Begin the Main-Infinite Crawl of the website, filter out the non-product pages using the regex pattern.
5. I used "crawlee" library for the actual crawling.
6. Added config to take care of scalability, "crawlee" is capable of autoscaling based on available resources and fixing the number of concurrent tasks it can perform.
7. "crawlee" also helps in PROXY management, we can give it multiple proxy URLs as input to help if our IP gets blocked.
8. "crawlee" also gives method to do infinite scrolling.
