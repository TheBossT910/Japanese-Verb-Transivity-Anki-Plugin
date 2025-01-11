//Taha Rashid
//Sunday May 26, 2024
//Jisho Scraper

//importing dependancies
const axios = require("axios");
const cheerio = require("cheerio")

//search query
let query = "hiraku"; //Super Mario 64

//creating object to save data to
let websiteInfo = {
    method: "GET",
    url: `https://jisho.org/search/${query}`,
    headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
}

//scraping html page from Jisho
const performScraping = async () => {
    try {
        //getting the html data
        const axiosResponse = await axios.request(websiteInfo);
        html = axiosResponse.data;

        //use Cheerio to parse the HTML
        const $ = cheerio.load(html);

        //select all the elements with the class name "meaning-tags"
        const meanings = $(".meaning-tags")

        //loop through the selected elements
        line = [];
        for (const meaning of meanings) {
            const text = $(meaning).text();
            //add each line to an array
            line.push(text)
        }

        //return the array
        return line
    
    } catch (err) {
        return ("performScraping Error! -> " + err);
    }
}


//run the scraping function
performScraping()
    .then((data) => {
        try {
            //console.log(data)
            for (x of data) {
                out = ""
                if (x.search("Intransitive verb") > 0)
                    out = out + "int,";
                if (x.search("Transitive verb") > 0)
                    out = out + "trans"
                console.log(out)
            }

        } catch (err) {
            console.log(err);
        }
    })
    .catch((err) => console.log(err))
