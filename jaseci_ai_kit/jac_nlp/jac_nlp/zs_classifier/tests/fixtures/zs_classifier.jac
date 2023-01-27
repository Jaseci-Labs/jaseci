walker test_zs_classify{
    can zs_classifier.classify;
     report zs_classifier.classify(text="I am so glad you liked it!",classes=["happy", "sad"]);
}

walker test_get_embedding{
    can zs_classifier.get_embeddings;
     report zs_classifier.get_embeddings(texts="I am so glad you liked it!");
}