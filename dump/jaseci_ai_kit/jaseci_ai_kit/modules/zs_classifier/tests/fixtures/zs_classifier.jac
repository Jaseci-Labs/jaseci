walker test_zs_classify{
    can zs_classifier.classify;
     report zs_classifier.classify(text="I am so glad you liked it!",classes=["happy", "sad"]);
}
