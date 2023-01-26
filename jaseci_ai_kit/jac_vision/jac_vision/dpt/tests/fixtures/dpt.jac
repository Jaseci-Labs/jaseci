walker test_estimate { 
    can dpt.estimate;
    can file.load_to_b64;

    image = file.load_to_b64("jac_vision/jac_vision/dpt/tests/data/person_street_walking.webp");
    report dpt.estimate(image, true);
}

walker test_estimate_batch {
    can dpt.estimate_batch;

    images = ['jac_vision/jac_vision/dpt/tests/data/person_street_walking.webp', 'jac_vision/jac_vision/dpt/tests/data/small_image_person.jpg'];
    report dpt.estimate_batch(images);
}