![logo_ironhack_blue](https://user-images.githubusercontent.com/23629340/40541063-a07a0a8a-601a-11e8-91b5-2f13e4e6b441.png)

# Project | Business Case: Automated Customer Reviews

<br>

## Project Goal

This project aims to develop a product review system powered by NLP models that aggregate customer feedback from different sources. The key tasks include classifying reviews, clustering product categories, and using generative AI to summarize reviews into recommendation articles.

<br>

## Problem Statement

With thousands of reviews available across multiple platforms, manually analyzing them is inefficient. This project seeks to automate the process using NLP models to extract insights and provide users with valuable product recommendations.

<br>

## Datasets

- **Primary Dataset**: [Amazon Product Reviews from Kaggel](https://www.kaggle.com/datasets/datafiniti/consumer-reviews-of-amazon-products/data)
- **Larger Dataset**: [Amazon Reviews Dataset](https://cseweb.ucsd.edu/~jmcauley/datasets.html#amazon_reviews)
- **Additional Datasets**: You are free to use other datasets from sources like HuggingFace, Kaggle, or any other platform.


<br>

## Main Tasks


### 1. Build a model for Sentiment Analysis

- **Goal**: Classify customer reviews into **positive**, **negative**, or **neutral** categories to help the company improve its products and services.
- **Task**: Develop, train, and evaluate a supervised multi-class classification model to classify the **textual content** of customer reviews as positive, negative, or neutral.

<br>

**Mapping Star Ratings to Sentiment Classes:**

Since the dataset contains **star ratings (1 to 5)**, you should map them to three sentiment classes as follows:  

| **Star Rating** | **Sentiment Class** |
|---------------|------------------|
|  1 - 2     | **Negative**  |
|  3         | **Neutral**  |
|  4 - 5     | **Positive**  |

 This is a simple approach, but you are encouraged to experiment with different mappings! 


**Model Building:**

For classifying customer reviews into **positive, negative, or neutral**, use **pretrained transformer-based models** to leverage powerful language representations without training from scratch.  

**Suggested Pretrained Models:**

- **`distilbert-base-uncased`** – Lightweight and fast, ideal for limited resources.  
- **`bert-base-uncased`** – A strong general-purpose model for sentiment analysis.  
- **`roberta-base`** – More robust to nuanced sentiment variations.  
- **`nlptown/bert-base-multilingual-uncased-sentiment`** – Handles multiple languages, useful for diverse datasets.  
- **`cardiffnlp/twitter-roberta-base-sentiment`** – Optimized for short texts like social media reviews.  

Explore models on [Hugging Face](https://huggingface.co/models) and experiment with fine-tuning to improve accuracy.

**Model Evaluation:**

Evaluate the model's performance on a separate test dataset using various evaluation metrics:
- Accuracy: Percentage of correctly classified instances.
- Precision: Proportion of true positive predictions among all positive predictions.
- Recall: Proportion of true positive predictions among all actual positive instances.
- F1-score: Harmonic mean of precision and recall.

Calculate the confusion matrix to analyze model's performance across different classes.


**Results:**

Summarize the performance of your model on the held-out test dataset using both quantitative metrics and visual analysis.

- Report the overall accuracy: Show the percentage of correctly classified test samples (X%).
- Analyze classification performance: Present precision, recall, and F1-score for each sentiment class to provide insights into the model’s performance:
   - Class 1: Precision = X%, Recall = X%, F1-score = X%
   - Class 2: Precision = X%, Recall = X%, F1-score = X%
   - Class 3: Precision = X%, Recall = X%, F1-score = X%
- Generate and interpret the confusion matrix: Include both a table and a visual representation to highlight correct predictions, misclassifications, and class-specific performance.

<br>

### 2. Build a model for Product Category Clustering

- **Goal**: Simplify the dataset by clustering product categories into **4-6 meta-categories**.
- **Task**: Develop and apply an unsupervised clustering model to group product reviews into 4–6 meaningful meta-categories based on similarities in their textual content and product characteristics.
- **Notes**: 
   - Analyze the dataset in depth to determine the most appropriate categories.
   - After applying clustering, you can analyze the characteristics of each cluster (e.g., keywords, products, and reviews) and assign meaningful names to the identified groups to improve interpretability. For example:
      - Ebook readers
      - Batteries
      - Accessories (keyboards, laptop stands, etc.)
      - Non-electronics (Nespresso pods, pet carriers, etc.)


<br>

### 3. Build a Model for Product Review Summarization Using Generative AI

- **Goal**: Summarize reviews into articles that recommend the top products for each category.
- **Task**: Create a model that generates a short article (like a blog post) for each of the product categories you created in the previous step. 


**Example Format**:

For the summary of each category, you can include:

- **Top 3 products** and key differences between them.
- **Top complaints** for each of those products.
- **Worst product** in the category and why it should be avoided.

This is just an example. You can get more ideas from other consumer Reviews websites, Amazon, The Verge, The Wirecutter, etc.

**Some options**:

- Consider using **Pretrained Generative Models** like **T5**, **GPT-3**, or **BART** for generating coherent and well-structured summaries. These models excel at tasks like summarization and text generation, and can be fine-tuned to produce high-quality outputs based on the extracted insights from reviews.
- You are encouraged to explore other **Transformer-based models** available on platforms like **Hugging Face**. Fine-tuning any of these pre-trained models on your specific dataset could further improve the relevance and quality of the generated summaries.
- You can also use an LLM API (e.g., OpenAI API) to generate the summaries -it will give good results. However, we encourage you to try a pretrained model first.


<br>

### 4. Deployment

Finally, put everything together and make it available for final users.

- **Goal**: expose some of the functionality you've created, in a way that makes it useful for final users.


**Some Ideas**:

We provide you with some ideas below. However, you are not limited to these options. Feel free to build a web app or website that does different things to what listed below.

1. **Create a website for the marketing department in your company**, who needs to gain insights on how well the products are received by customers (from reviews) and what other competitive products exist in the market.  For example, users in your webpage can choose between product categories and be shown statistics insights (distribution of ratings, best product ratings, etc), and text summarization for that specific category (which are the best product in this category, etc).
2. **Build a live review aggregator**: this could be a website like, for example, https://www.trustpilot.com/ or https://www.yelp.com/, organizing reviews strategically for buyers. You could add functionality for users to add reviews (for example, through a form, a user could write about a product, selecting which cluster category it belongs to and the rating given). Once a review is submitted, it could be displayed on the page as a ‘recently added review’. Feel free to come up with your own ideas about how you would like your live review aggregator to look like and behave
3. **Develop a website that generates recommendations by allowing users to upload a csv file with reviews**. For example, this website could allow business owners to upload a dataset of their products and respective reviews. Your website would process these, classifying them, clustering them, and showing insights in the form of small articles listing top products, main product issues, etc., for example (e.g., a list of articles, one per product; a list of articles, one per cluster).
4. **Develop a website that allows users to search for information about a product or product category through a text box**. This could be a text box where users type in what they are looking for / would like to buy. The output could display recommendations of products in text summary format, the category of the product, and the sentiment distribution for that product.


<!-- ## Deployment -->

<!-- - **Hosting**: You are free to host the models on your laptop or any cloud platform.
- **Framework**: You can use any framework of your choice (e.g., Gradio, AWS, etc.).

- **Options**:
  - List the models on HuggingFace.
  - Deploy a text file with the final results.
  - Create a website that displays the final results.
  - Build a live review aggregator.
  - Develop a website that generates recommendations by uploading a file with reviews.

- **Inspiration**: Look at websites like Consumer Reviews, The Verge, or The Wirecutter for ideas. 

-->


<!--
### Expectations

- You are expected to showcase a webpage or web app in which some simple user interactions are possible (for example through buttons, text boxes, sliders, ...).
- All your three components (classification, clustering, and text summarizer) should be visible or possible to interact with on the page in some form.
- You are free to host the models on your laptop or any cloud platform (e.g., Gradio, AWS, etc.).

-->


<br>


## Suggested Workflow

1. **Data Collection**: Gather and preprocess the dataset(s).
2. **Model Development**:
   - Create and evaluate the review classification model.
   - Create and test the clustering model.
   - Create and test the summarization model using Generative AI.
3. **Deployment**: Deploy the models using your chosen framework.
4. **Documentation**: Prepare the README, report, and presentation.
5. **Final Delivery**: Submit all deliverables, including the deployed app and final output.

