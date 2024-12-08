Project Description
Scrape Athens Pharmacies Wolt Catalogue, to determine most popular brands and products and their min/max/average prices.

Key Points
Used Levenshtein ratio in order to group similar description as the Wolt website is not using product ID's
Enabled Multiprocessing to run the Levenshtein ratio faster.


TODO:

- create a seperate function to only extract categories without opening them in a new page
- Extract Categories to a Dataframe use the algorithm located at Datawars string manipuolation method to find similar
categories and merge them and Finally figure out the most popular categories
- after opening all products thorugh the night verify that their total number is greater or equal to 50 * 1500 -> they are not they 44,044
- Save levenstein filtered items to csv

NOTES:

Noticed that item extraction using selenium does not work as expected in another pc using
Firefox on linux mint. I do get the browser to open and run but probably some timeouts are needed there.
This is probably not worth my time at least for now because I am not planning to develop the extraction
code any further in the near future.
What I am working on right now is all sorts of data maniulation. The data retrieving is fully implemented. And this part is currently working as it should cross-platform. Even the parallel multiprocessing of the Levehnstein Ratio is working on the linux machine.
