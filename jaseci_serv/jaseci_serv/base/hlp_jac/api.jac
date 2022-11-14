walker api {
    has user_id;
    has body;

    has url = 'https://dev-api.homelendingpal.com/api';
    has endpoint = 'kevBorrower';
    has token;
    has header = {'Authorization': 'Bearer ' + token};

    has anchor response;

    if(endpoint == 'kevBorrower'){
        response = request.get(url + '/kev/kevBorrower', {}, header);
    } elif(endpoint == 'borrowerFinancial'){
        response = request.get(url + '/kev/borrowerFinancial', {}, header);
    } elif(endpoint == 'borrowerCredit'){
        response = request.get(url + '/kev/borrowerCredit', {}, header);
    } elif(endpoint == 'homeSearch'){
        response = request.post(url + '/listHub/homes-search', body, header);
    }

    if(response["status_code"] == 200) {
        response['response']['user_id'] = user_id;
        report response['response'];
    } else{
        report response;
    }
}

walker getToken {
    has token;

    user_id=1;

    root {
        take --> node::cai_root;
    }
    cai_root {
        take --> node::user_dir;
    }
    user_dir {
        take -[user_link(user_id==user_id)]-> node::user;
    }
    user {
        here.token = token;
    }
}