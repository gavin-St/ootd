# OOTD: Computer Vision Outfit Search

https://devpost.com/software/ootd-ae8si9

Ever scroll through TikTok or Instagram and find a super cool outfit, only to wonder where you can get those exact pieces? We noticed that many people face this dilemma daily. Our inspiration for OOTD came from a desire to ungatekeep fashion and make trendy outfits accessible to everyone. We wanted to bridge the gap between seeing a style you love and actually owning it, WITHOUT gatekeepers.

OOTD allows users to upload an image of an outfit they like. Once uploaded, users can click on any piece of clothing within the image, and the app will identify the item and provide information on where to purchase it or find similar styles. Whether it's a unique jacket or a pair of shoes, OOTD helps you find exactly what you're looking for.

Dataset: Google Shopping web scraper -> Computer Vision model -> Semantic Embedding -> Upload to Pinecode Vector DB Backend: We used Flask, Meta's Segment Anything Model (SAM), along with Pinecone DB and OpenAI Embeddings. Frontend: React.js + ShadCN UI Kit + Next.js

<img width="675" alt="ootd-1" src="https://github.com/user-attachments/assets/5d027b4f-fc28-44c5-839d-26073c68a92f" />
App flow


<img width="675" alt="ootd-2" src="https://github.com/user-attachments/assets/8cd22f04-7eae-4368-941f-715cc5e328a0" />
OOTD Demo #1


<img width="675" alt="ootd-5" src="https://github.com/user-attachments/assets/d9967cde-8cba-4b62-b559-0d46118d1c08" />
Mask for Demo #1 created by tuned SAM


<img width="675" alt="ootd-5" src="https://github.com/user-attachments/assets/0adaba3d-f25a-40b5-a72a-d24627ba2d91" />
OOTD Demo #2

<img width="675" alt="ootd-6" src="https://github.com/user-attachments/assets/9c4aa312-b204-44d7-bd48-4b40e0d6ada1" />
OOTD Demo #3
