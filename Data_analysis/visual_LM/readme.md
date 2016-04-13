# visualize language model
You may refer to LM_usage.ipynb for running a quick demo.

[Notice] currently, the LM.py only support inner-product distance

## Analysis
After we built the language models, we can try to do some analysis on top of the language models. 
However, the language models space is very sparse, which make distance metric like L2 (the most commonly seen one) meaningless. To enable analysis on language models, we use the inner_product similarity metric. 

After computed the similarity matrix of chatrooms, we visualize the similarity matrix by plotting it out.
![Similarity Matrix](https://github.com/tsaiJN/DataScienceFinal/blob/master/Data_analysis/visual_LM/Similarity_matrix.png?raw=true "similarity Matrix")

<p align="center">
  <img src="Similarity_matrix.png" width="350"/>
</p>
