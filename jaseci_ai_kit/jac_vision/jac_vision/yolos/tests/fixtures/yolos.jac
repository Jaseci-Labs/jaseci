walker test_detect { 
    can yolos.detect;
    can file.load_to_b64;

    image = file.load_to_b64("jac_vision/jac_vision/yolos/tests/data/person_street_walking.webp");
    report yolos.detect(image, true);
}

walker test_detect_batch {
    can yolos.detect_batch;

    images = ['jac_vision/jac_vision/yolos/tests/data/person_street_walking.webp', 'jac_vision/jac_vision/yolos/tests/data/small_image_person.jpg'];
    report yolos.detect_batch(images);
}