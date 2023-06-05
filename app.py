# Importing Necessary Libraries
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)  # Initialising this flask app with the name 'app'


@app.route('/', methods=['GET'])

def homepage():
    return render_template('index.html')


@app.route('/scrap', methods=['POST']) # route with allowed methods as POST and GET


# Main Function
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ","") # Obtain the search string entered in the form
        try:
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString  # Creating url to search a product
            uClient = uReq(flipkart_url)  # requesting the webpage from the internet
            flipkartPage = uClient.read() # reading the webpage
            uClient.close() # closing the connection to the web server
            flipkart_html = bs(flipkartPage, "html.parser") # parsing the webpage as HTML

            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})  # Seacrhing for appropriate tag to redirect to the product link
            del bigboxes[0:3]
            box = bigboxes[0]  # Taking the first iteration for demo

            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']  # extracting the actual product link
            prodRes = requests.get(productLink) # getting the product page from server
            prod_html = bs(prodRes.text, "html.parser") # parsing the product page as HTML
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})  # Finding HTML section containing the customer comments

            reviews = []  # initializing an empty list for reviews

            for commentbox in commentboxes:

                # Name
                try:
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                except:
                    name = 'NaN'

                # Rating
                try:
                    rating = commentbox.div.div.div.div.text
                except:
                    rating = 'NaN'

                # Comment Heading
                try:
                    commentHead = commentbox.div.div.div.p.text
                except:
                    commentHead = 'NaN'

                # Customer's Comment
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    custComment = comtag[0].div.text
                except:
                    custComment = 'NaN'

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "Comments Heading": commentHead, "Comment": custComment}  # saving that detail to a dictionary
                reviews.append(mydict)
            return render_template('results.html', reviews=reviews)  # showing the review to the user

        except:
            return 'something is wrong'

if __name__ == "__main__":
    app.run(port=8000,debug=True)  # Running the app on the local machine on port 8000