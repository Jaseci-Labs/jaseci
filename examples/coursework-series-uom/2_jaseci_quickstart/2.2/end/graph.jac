// Edges
edge married;
edge child;
edge member;

// Nodes
node person {
    has id;
    has family_id;
    has name;
    has date_of_birth;
    has profession;
    has gender;
    has deceased;
    has parents;
    has children;
    has spouse;

    has age;
    has days_to_birthday;

    can get_age {
        today_date = date.date_now();
        difference = date.date_day_diff(start_date=date_of_birth, end_date=today_date);
        age = difference / 365;
    }

    can get_days_to_birthday {
        today_date = date.date_now();
        today_year = today_date.str::split('-')[0];
        birthdate_split = date_of_birth.str::split('-');
        birth_month = birthdate_split[1];
        birth_day = birthdate_split[2];
        birthday = '-'.str::join([today_year, birth_month, birth_day]);
        difference = date.date_day_diff(start_date=today_date, end_date=birthday);
        if (difference < 0) : difference = difference + 365;
        days_to_birthday = difference;
    }
}
node family_root {
    has id;
    has family_name;
}

// Graphs
graph family_tree {
    has anchor family_root;
    spawn {
        family_root = spawn node::family_root;
    }
}