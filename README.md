# Instacart-USDA
Merge of [Instacart dataset](https://www.instacart.com/datasets/grocery-shopping-2017)  and [USDA](https://ndb.nal.usda.gov/ndb/) Nutritional Information
on product Table.

**Important 1:** It's a merge based on USDA search engine and the accuracy of merge on a sample is about 80%

**Important 2:** NDB_No and ndbno columns are STRING not INT (if you don't consider this you will lose rows)

**Important 3:** In this repo is only product table of Instacart dataset and merge tables, the others are in this [link](https://www.instacart.com/datasets/grocery-shopping-2017)