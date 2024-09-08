walker test_activity {
    has a, b, c;

    can elastic.doc_activity, elastic.refresh_activity, elastic.search_activity, elastic.mapping_activity;

    with entry {
        # with standard structure but can be overriden
        report std.log_activity({"other_field": 1}, action = "CUSTOM_ACTION_NAME");
        # with suffix on index
        report std.log_activity({"other_field": 2}, action = "CUSTOM_ACTION_NAME", suffix="-sample-id");

        # developer's custom structure
        report elastic.doc_activity({"testing": "doc_activity"});

        # since it's a fast testing we should call refresh manually
        elastic.refresh_activity();
        elastic.refresh_activity(suffix="-sample-id");

        report elastic.search_activity({});
        report elastic.search_activity({}, suffix="-sample-id");

        report elastic.mapping_activity();
        report elastic.mapping_activity(suffix="-sample-id");
    }
}

walker test_common {
    has d, e, f;

    can elastic.doc, elastic.refresh, elastic.search, elastic.mapping;

    with entry {
        report elastic.doc({"testing": "doc"});
        report elastic.doc({"testing": "doc-other-index"}, index="other-index");
        report elastic.doc({"testing": "doc-other-index-suffix"}, index="other-index", suffix="-user-id");

        # since it's a fast testing we should call refresh manually
        elastic.refresh();
        elastic.refresh(index="other-index");
        elastic.refresh(index="other-index", suffix="-user-id");

        report elastic.search({});
        report elastic.search({}, index="other-index");
        report elastic.search({}, index="other-index", suffix="-user-id");

        report elastic.mapping();
        report elastic.mapping(index="other-index");
        report elastic.mapping(index="other-index", suffix="-user-id");
    }
}

walker test_other {

    can elastic.aliases, elastic.reindex;

    with entry {
        # migrate index
        report elastic.reindex({
            "source": {
                "index": "other-index-user-id",
                "size": 10
            },
            "dest": {
                "index": "new-index"
            }
        });

        report elastic.aliases();

        # since it's a fast testing we should call refresh manually
        elastic.refresh(index="new-index");
        report elastic.search({}, index="new-index");
    }
}