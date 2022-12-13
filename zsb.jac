version : '3.5.9.3'

          //Object Declarations
 node botset
{
    has plan_type, user_type, payment_status, trial_status_display;
    has max_bot_count, max_transaction_count, max_ans_count, max_test_suite, max_test_cases, export_import, analytics, integration, text_ingest;
    has current_bot_count, current_transaction_count, last_reset_date;
    has customer, subscription;
    has onboarding_flag;
}
node log_chunk { has history, feedback, callback; }
node bot { has anchor name, answer_count = 0, description, created_time = std.time_now(), last_updated_time = std.time_now(), metadata, status, mail_config; }
node category { has anchor name, color; }
node integration { has anchor identifier, path, int_type, settingsobj; }
node testsuite { has anchor name, test_count, created_time, last_updated_time, last_result_summary, last_ran_time; }
node testcase {
    has anchor question, expected_answerid, last_test_status, last_actual_answerid, last_ran_time, created_time, last_updated_time;
    has private encoding;
}
node answer
{
    has anchor text, show_text, score, created_time = std.time_now(), last_updated_time = std.time_now();
    has private encoding;
    has qlinks, hitcount;
    has editor;
    has categoryid;
    has quick_reply, quick_reply_options;
    has callback;
    has ans_version ="final";
}
node default_answer { has anchor text, show_text, thresh_score, hitcount; }

// Init users graph access

walker init
{
    has plan_obj, plan_type, user_type, payment_status, trial_status_display, max_bot_count, max_transaction_count, text_ingest;
    has plan_obj_default;

    with entry
    {
        //default value to be used if global variable is missing
        plan_obj_default = {"max_bot_count" : 1, "max_ans_count" : 10, "max_txn_count" : 0, "max_test_suite" : 1, "max_test_cases" : 5, "export_import" : "false", "analytics" : "false", "integration" : "Preview", "text_ingest" : "false"};

        //Set Default Options : plan type (free, basic, advanced) , user type ( free, trial, paying), payment status ( paid, unpaid), trial status display ( true, false)
        plan_type = "free";
        user_type = "free";
        payment_status = "paid";
        trial_status_display = "false";
        plan_type_full_text = ("plan_type_" + plan_type).str::lower;
    }

    root
    {
        take(--> node::botset) else
        {
            plan_obj = std.get_global(plan_type_full_text);
            std.log('root plan_obj', plan_obj);
            if (not plan_obj):plan_obj=plan_obj_default;
            spawn here--> node::botset(plan_type = plan_type, user_type = user_type, payment_status = payment_status,
                                        trial_status_display = trial_status_display, current_bot_count = 0,
                                        last_reset_date = std.time_now(), onboarding_flag = []);
              std.log(plan_obj);
            take--> node::botset;
        }
    }
    botset
    {
        if (not here.plan_type):here.plan_type=plan_type;
        plan_type_full_text = ("plan_type_" + here.plan_type).str::lower;
        std.log('botset plan_obj ', plan_type_full_text);
        plan_obj = std.get_global(plan_type_full_text);
        std.log(plan_obj);
        if (not here.user_type):here.user_type=user_type;
        if (not here.max_bot_count):here.max_bot_count=plan_obj['max_bot_count'];
        if (not here.max_transaction_count):here.max_transaction_count=plan_obj['max_txn_count'];
        if (not here.max_ans_count):here.max_ans_count=plan_obj['max_ans_count'];
        if (not here.max_test_suite):here.max_test_suite=plan_obj['max_test_suite'];
        if (not here.max_test_suite):here.max_test_suite=plan_obj['max_test_suite'];
        if (not here.max_test_cases):here.max_test_cases=plan_obj['max_test_cases'];
        if (not here.last_reset_date):here.last_reset_date=std.time_now();
        if (not here.onboarding_flag): here.onboarding_flag=[];
        if (not here.analytics): here.analytics=plan_obj['analytics'];
        if (not here.export_import): here.export_import=plan_obj['export_import'];
        if (not here.text_ingest): here.text_ingest=plan_obj['text_ingest'];
        if (not here.integration): here.integration=plan_obj['integration'];
        if (not here.current_transaction_count): here.current_transaction_count='0';
        if (not here.subscription): here.subscription={};
        if (not here.customer): here.customer={};
        report here;
        disengage;
    }
}

//botset

walker get_botset
{

    root { report--> node::botset; }
}

walker change_botset
{
    has plan_obj, plan_type, user_type, payment_status, trial_status_display, customer, subscription;
    root { take--> node::botset; }
    botset
    {
        if (plan_type)
        {
            here.plan_type = plan_type;
            plan_type_full_text = 'plan_type_' + plan_type;

            std.log('change_botset ', plan_type_full_text);

            plan_obj = std.get_global(plan_type_full_text);
            if (plan_obj)
            {
                here.max_bot_count = plan_obj['max_bot_count'];
                here.max_transaction_count = plan_obj['max_txn_count'];
                here.max_ans_count = plan_obj['max_ans_count'];
                here.max_test_suite = plan_obj['max_test_suite'];
                here.max_test_suite = plan_obj['max_test_suite'];
                here.max_test_cases = plan_obj['max_test_cases'];
                here.analytics = plan_obj['analytics'];
                here.export_import = plan_obj['export_import'];
                here.integration = plan_obj['integration'];
                here.text_ingest = plan_obj['text_ingest'];
            }
        }

        if (user_type): here.user_type=user_type;
        if (payment_status):here.payment_status=payment_status;
        if (trial_status_display):here.trial_status_display=trial_status_display;
        if (not here.customer)
        {
            if (customer):here.customer=customer;
        }
        if (subscription):here.subscription=subscription;
        report here;
        disengage;
    }
}

walker change_botset_secret
{
    has max_ans_count;
 root { take--> node::botset; }
    botset
    {
        here.max_ans_count=max_ans_count;
        report here;
    }
}


walker reset_botset
{
    has plan_obj, plan_type, user_type, payment_status, trial_status_display, customer, subscription;
    root { take--> node::botset; }
    botset
    {

        here.plan_type = plan_type;
        plan_obj = std.get_global('plan_type_free');
        if (plan_obj)
        {
            here.max_bot_count = plan_obj['max_bot_count'];
            here.max_transaction_count = plan_obj['max_txn_count'];
            here.max_ans_count = plan_obj['max_ans_count'];
            here.max_test_suite = plan_obj['max_test_suite'];
            here.max_test_suite = plan_obj['max_test_suite'];
            here.max_test_cases = plan_obj['max_test_cases'];
            here.analytics = plan_obj['analytics'];
            here.export_import = plan_obj['export_import'];
            here.integration = plan_obj['integration'];
        }

        here.user_type = 'free';
        here.payment_status = 'unpaid';
        here.trial_status_display = 'false';
        here.subscription = {};
        take--> node::bot;
    }
    bot
    {
        here.status = 'inactive';
    }
}

walker reactivate_allbots
{
    root { take--> node::botset; }
    botset
    {
        take--> node::bot;
    }
    bot
    {
        here.status = 'active';
    }
}

walker set_onboarding_flag
{
    has flag;
    root { take--> node::botset; }
    botset
    {
        if (not here.onboarding_flag): here.onboarding_flag=[];
        here.onboarding_flag = here.onboarding_flag + [flag];
        report here.onboarding_flag;
    }
}

walker reset_onboarding_flag
{
    has flag;
    root { take--> node::botset; }
    botset
    {
        here.onboarding_flag = [];
        if (flag)
        {
            for
                i in here.onboarding_flag
                {
                    if (i != flag)
                    {
                        here.onboarding_flag = here.onboarding_flag + [i];
                    }
                }
        }
        report here.onboarding_flag;
    }
}

walker reset_botset_count
{
    root { take--> node::botset; }
    botset
    {
        here.current_transaction_count = 0;
    }
}

// Bot

walker get_bots
{
    has count, bots, bot_count;
    root { take--> node::botset; }
    botset
    {
        bot_count = 0;

        for
            i in--> node::bot
            {
                if (i.status != 'inactive')
                {
                    bot_count += 1;
                    if
                        not(i.answer_count)
                        {
                            count = spawn i walker::get_answer_count();
                            i.answer_count = count;
                        }

                    report i;
                }
            }
        here.current_bot_count = bot_count;
        disengage;
    }
}

walker get_bot
{
    bot {
        report here;
    }
}


walker add_bot
{
    has name, desc, created_time, default_answer;
    default_answer = "I do not have that information yet. Try another query ?";
    thresh_score = 0.07;
    metadata = {"greetings" : [], "defaultAnswer" : default_answer, "threshold" : thresh_score, "others" : {"language" : "English (U.S)"}};
    root
    {
        take--> node::botset;
    }
    botset
    {
        if (here.current_bot_count > here.max_bot_count)
        {
            disengage;
        }
        created_time = std.time_now();
        bot = spawn here--> node::bot(name = name, description = desc, metadata = metadata, created_time = created_time, last_updated_time = created_time);
        spawn bot walker::create_default_answer(text = default_answer, thresh_score = thresh_score);
        here.current_bot_count += 1;
        report bot;
        disengage;
    }
}

walker delete_bot {
    bot {
        take -->;
        destroy here;
        <--node::botset[0].current_bot_count -= 1;
    }

    log_chunk, category, answer, default_answer, integration, testsuite, testcase {
        take -->;
        destroy here;
    }
}

walker change_bot
{
    has name, desc, metadata, answer_count, thresh_score, no_response, mail_config;
    thresh_score = 0.07;
    default_answer = "I do not have that information yet. Try another query ?";

    bot
    {
        if (name):here.name=name;
        if (desc):here.description=desc;
        if (metadata)
        {
            if (metadata['defaultAnswer'] && metadata['threshold'])
            {
                spawn here walker::change_default_answer(text = metadata['defaultAnswer'],thresh_score = metadata['threshold'].float, no_report = true);

            }
            here.metadata = metadata;
        }
        if (answer_count):here.answer_count=answer_count;
        here.last_updated_time = std.time_now();
        if (mail_config): here.mail_config = mail_config;
        if (not no_response):report here;
        disengage;
    }
}

// Bot Summary


walker get_bot_summary
{

    with entry{
        integration_count=0;
        testsuite_count=0;
    }
    bot
    {
        for j in --> node::integration
        {
        integration_count=integration_count+1;
        }
        for i in --> node::testsuite
        {
        testsuite_count=testsuite_count+1;
        }
    }
      with exit{
        report {"integration_count":integration_count,"testsuite_count":testsuite_count};
    }
}

// Answer

walker get_answers
{
    bot
    {
        report--> node::answer;
        report--> node::default_answer;
        disengage;
    }
}

walker get_answer
{
    answer
    {
        report here;
        disengage;
    }
}

walker get_answers_filter
{
    has start_count, end_count;
    bot
    {
        for
            i in--> node::answer
            {
                start_count = start_count + 1;
                report i;
            if (start_count == end_count):disengage;
            }
       disengage;
    }
}

walker get_answer_array
{
    has anchor answer_array;
    with entry
    {
        answer_array = [];
    }
    bot
    {
        for
            i in--> node::answer
            {
                answer_array = answer_array + [i.text];
            }
    }
}

walker get_answer_count
{
    has anchor count;

    with entry
    {
        count = 0;
    }
    bot
    {
        for
            i in--> node::answer
            {
                count += 1;
            }
    }
}

walker create_answer
{
    has text, show_text, categoryid;
    has ans_version = "final", qlinks = [], quick_reply = "false", quick_reply_options = [], callback = "false", editor = "rte", variants = [];

    can use.enc_answer;

    bot
    {
        ans = spawn here--> node::answer(
            encoding = use.enc_answer("".str::join(qlinks) + text),
            text = text,
            show_text = visitor.context.dict::get("show_text", text),
            qlinks = qlinks,
            categoryid = categoryid,
            quick_reply = quick_reply,
            quick_reply_options = quick_reply_options,
            callback = callback,
            editor = editor,
            ans_version = ans_version
        );

        here.answer_count += 1;
        here.last_updated_time = std.time_now();

        report ans;
    }
}

walker create_many_answers
{
    has textlist;

    bot, category
    {
       for
           i in textlist : spawn here walker::create_answer(text = i, show_text = i);
    }
}

walker delete_answer
{

    with entry
    {
        thisbot = <--node::bot[0];
        answer_count = spawn thisbot walker::get_answer_count();
    }
    answer
    {
        destroy here;
    }
    with exit
    {
        if (answer_count != 1): answer_count=answer_count-1;
        else: answer_count="0";
        spawn thisbot walker::change_bot(answer_count = answer_count, no_response = 'true');
        report answer_count;
    }
}

walker change_answer
{
    has text, show_text, editor, categoryid, quick_reply, quick_reply_options, callback, qlinks, encoding;
    has thisbot;
    has ans_version;
    can use.enc_answer;

    with entry
    {
        thisbot = <--node::bot[0];
    }

    answer
    {
        if (text)
        {
            pretext = "";
            here.text = text;
            if (here.qlinks)
            {for
                    i in here.qlinks : pretext += i;
            }
            here.encoding = use.enc_answer(pretext + text);
        }
        if (show_text): here.show_text = show_text;
        if (editor): here.editor = editor;
        here.categoryid = categoryid;
        if (quick_reply): here.quick_reply = quick_reply;
        if (callback): here.callback = callback;
        if (ans_version): here.ans_version = ans_version;
        if (quick_reply_options): here.quick_reply_options = quick_reply_options;
        here.last_updated_time = std.time_now();
        report here;
        disengage;
    }

    with exit
    {
        thisbot.last_updated_time = std.time_now();
    }
}

// Default Answer

walker get_default_answer
{
    bot
    {
        report--> node::default_answer;
        disengage;
    }
}

walker get_default_answerid
{
    has anchor default_answerid;
    bot
    {
        default_answerid = --> node::default_answer[0];
        disengage;
    }
}

walker create_default_answer
{
    has text, show_text, thresh_score;

    bot
    {
        if (not thresh_score):thresh_score=0.07;
        take(--> node::default_answer) else
        {
            default = spawn here--> node::default_answer(text = text, show_text = text, thresh_score = thresh_score);
        }
        disengage;
    }
}

walker change_default_answer
{
    has text, show_text, thresh_score, no_report;
    bot
    {
        take--> node::default_answer[0];
    }
    default_answer
    {

        if (text)
        {
            here.text = text;
            here.show_text = text;
        }
        if (thresh_score)
        {
            here.thresh_score = thresh_score;
        }
        disengage;
    }
}

walker delete_default_answer
{

    default_answer
    {
        destroy here;
    }
}

//Category
walker create_category
{
    has name, color;

    bot
    {
        cat = spawn here--> node::category(name = name, color = color);
        report cat;
        disengage;
    }
}

walker get_categories
{
    bot
    {
        report--> node::category;
    }
}

walker get_category_array
{
    has anchor category_array;

    with entry
    {
        category_array = [];
    }

    bot
    {
        for
            i in--> node::category
            {
                category_array += [ {"category" : i.name, "id" : &i} ];
            }
    }
}

walker get_category_name
{
    has anchor category_obj;

      category
    {
        category_obj = {"name" : here.name, "color" : here.color};
    }
}

walker change_category
{
    has name, color;
    category
    {
        if (name):here.name=name;
        if (color):here.color=color;
        report here;
        disengage;
    }
}

walker delete_category
{
    has thisbot, categoryid, deleteanswers;
    with entry
    {
        thisbot = <--node::bot[0];
        categoryid = &here;
    }
    category
    {
        destroy here;
    }
    with exit
    {
        if (not deleteanswers):deleteanswers="";
        spawn thisbot walker::reset_category(categoryid = categoryid, deleteanswers = deleteanswers);
    }
}

walker reset_category
{
    has categoryid, deleteanswers;
    bot
    {
        for
            i in node::answer
            {
                if (i.categoryid == categoryid)
                {
                    if (deleteanswers == "Yes")
                    {
                        destroy i;
                    }
                    else
                    {
                        i.categoryid = "";
                    }
                    report i;
                }
            }
    }
}

// Integration

walker create_integration
{
    has identifier, int_type, path, settingsobj;

    bot
    {
        intg = spawn here--> node::integration(identifier = identifier, int_type = int_type, path = path, settingsobj = settingsobj);
        report intg;
        disengage;
    }
}

walker get_integrations
{
    bot
    {
        report--> node::integration;
    }
}

walker change_integration
{
    has identifier, int_type, path, settingsobj;
    integration
    {
        if (identifier):here.identifier=identifier;
        if (int_type):here.int_type=int_type;
        if (path):here.path=path;
        if (settingsobj): here.settingsobj=settingsobj;
        report here;
        disengage;
    }
}

walker delete_integration
{
    integration
    {
        destroy here;
    }
}

// Test Suite

walker create_testsuite
{
    has name, time;

    bot
    {
        time = std.time_now();
        suite = spawn here--> node::testsuite(name = name, created_time = time, last_updated_time = time,last_result_summary = "", test_count = 0);
        report suite;
        disengage;
    }
}

walker change_testsuite
{
    has name;

    testsuite
    {
        if (name): here.name=name;
        here.last_updated_time = std.time_now();
        report here;
        disengage;
    }
}

walker get_testsuites
{
    has count;
    take--> node::testsuite;
    testsuite
    {
        count = spawn here walker::get_testcase_count();
        here.test_count = count;
        report here;
    }
}

walker delete_testsuite
{
    testsuite
    {
        destroy here;
    }
}

walker run_testsuite
{
    has name;
    has response;
    has pass_count, fail_count, actual_answer, thisbot;
    has questionarray;
    can use.enc_question;

    with entry
    {
        if (not response):response=true;
        thisbot = <--node::bot[0];
        questionarray = [];
        actual_answer = "";
        //take -->node::testsuite;
        pass_count = 0;
        fail_count = 0;
    }

    testsuite
    {

                  for
                      i in--> node::testcase
                      {
                          if (not i.encoding)
                          {
                              std.log('There is no encoding');
                              i.encoding =  use.enc_question(i.question);
                          }
                          actual_answer = spawn thisbot walker::ask_question_testcase(text = i.question, enc=i.encoding);
                          a=&actual_answer;
                          b=i.expected_answerid;
                          if (a == b)
                          {
                              pass_count += 1;
                              i.last_test_status = 1;
                          }
                          else
                          {

                              fail_count += 1;
                              i.last_test_status = 0;
                          }
                          i.last_actual_answerid = &actual_answer;
                          i.last_ran_time = std.time_now();
                      }

                  if (response == true): report -->node::testcase;

                  here.last_result_summary = {"success" : pass_count, "fail" : fail_count};
                  here.last_ran_time = std.time_now();
                  disengage;
    }
}

// Test Case

walker create_testcase
{
    has question, answerid, time;
    can use.enc_question;

    with entry
    {
         enc = use.enc_question(question);
    }

    testsuite
    {
        time = std.time_now();
        test_case = spawn here--> node::testcase(question = question, expected_answerid = answerid, created_time = time, last_updated_time = time);
        test_case.encoding = enc;
        here.last_updated_time = std.time_now();
        here.test_count += 1;
        report test_case;
        disengage;
    }
}

walker create_many_testcases
{
    has question_array, answerid, time;
    has current_question_array;
    has answer, default_answerid;
    can use.enc_question;

    with entry
    {
        thisbot = <--node::bot[0];
        current_question_array = [];
    }

    testsuite
    {
        time = std.time_now();
        current_question_array = spawn here walker::get_testcase_array();

        for
            i in question_array
            {
              enc = use.enc_question(i);

                if (not i in current_question_array)
                {
                    current_question_array = current_question_array + [i];
                    if (answer == "default")
                    {
                        default_answerid = spawn thisbot walker::get_default_answerid();
                        test_case = spawn here--> node::testcase(question = i, expected_answerid = default_answerid, created_time = time, last_updated_time = time);
                        test_case.encoding = enc;
                        report test_case;
                    }
                    else
                    {
                        answerid = spawn thisbot walker::ask_question_nolog_noreport(text = i);
                        test_case = spawn here--> node::testcase(question = i, expected_answerid = answerid, created_time = time, last_updated_time = time);
                        test_case.encoding = enc;
                        report test_case;
                    }
                }
            }
        // report here;
        disengage;
    }
}

walker change_testcase
{
    has question, answerid;
    with entry
    {
        thissuite = <--node::testsuite[0];
    }
    testcase
    {
        if (question): here.question=question;
        if (answerid): here.expected_answerid=answerid;
        here.last_updated_time = std.time_now();
        report here;
        disengage;
    }
    with exit
    {
        thissuite.last_updated_time = std.time_now();
    }
}

walker get_testcases
{
    testsuite
    {
        report--> node::testcase;
    }
}

walker get_testcase_array
{
    has anchor testcase_array;
    with entry
    {
        testcase_array = [];
    }
    testsuite
    {
        for
            i in--> node::testcase
            {
                testcase_array = testcase_array + [i.question];
            }
    }
}

walker get_testcase_count
{
    has anchor count;

    with entry
    {
        count = 0;
    }
    testsuite
    {
        for
            i in--> node::testcase
            {
                count += 1;
            }
    }
}

walker delete_testcase
{
    testcase
    {
        destroy here;
    }
}

walker run_all_tests
{
    has name;
    has pass_count, fail_count, actual_answer, thisbot;
    has questionarray;
    has thissuite;
    take--> node::testsuite;
    testsuite
    {
        spawn here walker::run_testsuite(response = 'false');
        report here;
    }
}

// Import Export

walker import_answerbank
{
    has answerbank;

    bot {
        for ans in answerbank {
            // check if ans's text is existing
            if not --> node::answer(text == ans["text"]) {
                category_id = "";
                if ans["category"] {
                    category_nodes = --> node::category(name == ans["category"]);

                    if category_nodes: category_id = &category_nodes[0];
                    else: category_id = &(spawn here --> node::category(name = ans["category"], color = ans["category_color"]));
                }

                spawn here walker::create_answer(
                    text = ans["text"],
                    show_text = ans["show_text"],
                    qlinks = ans["qlinks"],
                    categoryid = category_id,
                    quick_reply = ans.dict::get("quick_reply"),
                    quick_reply_options = ans.dict::get("quick_reply_options"),
                    callback = ans.dict::get("callback"),
                    editor = ans.dict::get("editor")
                );
            }
        }
    }
}

walker export_bot
{
    has name, desc, metadata;
    has botobj, ansobj, quickreplyobj;
    has category_obj;

    with entry
    {
        botobj = "";
        name = here.name;
        desc = here.description;
        metadata = here.metadata;
    }

    bot
    {
        ansobj = [];
        quickreplyobj = [];
   for i in--> node::answer
       {
           categoryid = i.categoryid;
           if (categoryid){
               category_obj = spawn *categoryid walker::get_category_name();
           }
           else: category_obj={"name":"", "color":""};
           ansobj += [ {"text" : i.text,
                        "show_text" : i.show_text,
                        "qlinks" : i.qlinks,
                        "category" : category_obj['name'],
                        "category_color" : category_obj['color'],
                        "quick_reply" : i.quick_reply,
                        "quick_reply_options" : i.quick_reply_options,
                        "callback" : i.callback,
                        "editor" : i.editor} ];
       }
    }

    with exit
    {
        botobj = {"name" : here.name, "desc" : here.description, "metadata" : here.metadata, "answerbank" : ansobj};
        report botobj;
    }
}

walker import_bot
{
    has name, desc, answerbank;
    has metadata = {};

    can use.enc_answer;

    root { take--> node::botset; }
    botset {
        current_bot = spawn here--> node::bot(name = name, description = desc, metadata = metadata);
        report current_bot;

        spawn current_bot walker::create_default_answer(
            text = metadata.dict::get("defaultAnswer", "I do not have that information yet. Try another query ?"),
            thresh_score = metadata.dict::get("threshold", 0.07)
        );

        spawn current_bot walker::import_answerbank(answerbank = answerbank);
    }
}

// Category Templates

walker get_category_templates
{

    has template_array;

    with entry
    {
        template_array =
            [
                {
                    "template_category" : "Greetings",
                    "template_category_color" : "#333333",
                    "answers" : [
                        {
                            "text" : "You're welcome! Thanks for chatting with me today.",
                            "show_text" : "You're welcome! Thanks for chatting with me today.",
                            "qlinks" : []
                        },
                        {
                            "text" : "Thanks for chatting with me today. Goodbye!",
                            "show_text" : "Thanks for chatting with me today. Goodbye!",
                            "qlinks" : []
                        },
                        {
                            "text" : "I am right where you left me.",
                            "show_text" : "<p>I am right where you left me.</p>",
                            "qlinks" : []
                        },
                        {
                            "text" : "You're so polite!",
                            "show_text" : "You're so polite!",
                            "qlinks" : []
                        },
                        {
                            "text" : "Good evening!",
                            "show_text" : "<p>Good evening! How's your day been?</p>",
                            "qlinks" : []
                        },
                        {
                            "text" : "Good morning!",
                            "show_text" : "<p>Good morning! How are you today?</p>",
                            "qlinks" : []
                        },
                        {
                            "text" : "Good night. Sleep tight!",
                            "show_text" : "<p>Sleep tight!</p>",
                            "qlinks" : []
                        },
                        {
                            "text" : "Whats up ?  I am just here, waiting to help someone.",
                            "show_text" : "<p>I am just here, keen to share my knowledge</p>",
                            "qlinks" : ["hey what's up"]
                        },
                        {
                            "text" : "I'm doing very well. Thanks!",
                            "show_text" : "I'm doing very well. Thanks!",
                            "qlinks" : []
                        }
                    ]
                },
                {
                    "template_category" : "Emotions",
                    "template_category_color" : "#599999",
                    "answers" : [
                        {
                            "text" : "Glad you think I'm funny.",
                            "show_text" : "Glad you think I'm funny.",
                            "qlinks" : []
                        },
                        {
                            "text" : "Wow indeed!",
                            "show_text" : "Wow indeed!",
                            "qlinks" : []
                        },
                        {
                            "text" : "No big deal. I don't hold a grudge.",
                            "show_text" : "No big deal. I don't hold a grudge.",
                            "qlinks" : []
                        },
                        {
                            "text" : "Hugs are the best!",
                            "show_text" : "Hugs are the best!",
                            "qlinks" : []
                        }
                    ]
                }
            ];
    }

    with exit
    {
        report template_array;
    }
}

walker import_category_template
{
    has category_object_array, category_object;
    has category_array, categoryid, count;

    with entry
    {
        category_array = spawn here walker::get_category_array();
        count = 0;
    }

    bot
    {

        for
            a in category_object_array
            {
                category_object = category_object_array[count];
                category_name = category_object['template_category'];
                category_color = category_object['template_category_color'];
                count += 1;
            for
                i in category_object['answers']
                {
                    categoryid = "";

                        for
                            j in category_array
                            {
                                if (category_name == j['category'])
                                {
                                    categoryid = j['id'];
                                }
                            }

                        if (not categoryid)
                        {
                            category_node = spawn here--> node::category(name = category_name, color = category_color);
                            categoryid = &category_node;
                            category_array += [ {"category" : category_name, "id" : categoryid} ];
                        }
                        spawn here walker::create_answer(text = i['text'], show_text = i['show_text'], qlinks = i['qlinks'], categoryid = categoryid, quick_reply = i['quick_reply'], quick_reply_options = i['quick_reply_options'], callback = i['callback'], editor = i['editor']);
                }
            }
    }
}

// Ask Question

walker ask_question
{
    has anchor answer;
    has text, selected, no_report = false;
    has max_score, thisbot, botset, dont_log, metadata, default, thresh_score;
    has use_draft = false;
    can use.enc_question, use.qa_score;

    with entry
    {
        enc = use.enc_question(text);
        selected = false;
        max_score = 0;
        thresh_score = 0;
        thisbot = here;
        botset = <--node::botset[0];
    }
    bot, default_answer
    {
        for
            j in--> node::default_answer : default = j;
        if (default): thresh_score=default.thresh_score;

        for
            i in--> node::answer
            {
                if (i.context.dict::get("ans_version", "final") != "draft" || use_draft==true )
                {
                    score = use.qa_score(enc, i.encoding);
                    if (score[0][0] > max_score)
                    {
                        selected = i;
                        max_score = score[0][0];
                    }
                }
            }
        std.log(score);
        if(max_score!=0):selected.score = max_score;
    }

    with exit
    {
        if (max_score > thresh_score)
        {

            if (not dont_log):
                    spawn thisbot walker::log_question(text=text, selected=selected, resp_type="answer", metadata=metadata);
            if (selected.hitcount): selected.hitcount+=1;
            else: selected.hitcount=1;
            if (metadata != {"channel" : "ZSB Platform"})
            {
                if (botset.current_transaction_count == "0"):botset.current_transaction_count=1;
                else:botset.current_transaction_count+=1;
            }

            answer = selected;
            if not(no_report): report selected;

        }
        else
        {
            if (default)
            {
                if (not dont_log):
                    spawn thisbot walker::log_question(text=text, selected=default, resp_type="default", metadata=metadata);
                if (default.hitcount): default.hitcount+=1;
                else: default.hitcount=1;
                answer = default;
                if not(no_report): report default;
            }
            else {
                answer = ret = {"context":{"text":"I do not have that information yet. Try another query ?","show_text":"I do not have that information yet. Try another query ?"}};
                if not(no_report): report ret;
            }
        }
    }
}

walker pub_ask_question : anyone
{
    has anchor answer;
    has text, selected, no_report = false;
    has max_score, thisbot, botset, dont_log, metadata, default, thresh_score;
    can use.enc_question, use.qa_score;

    with entry
    {
        enc = use.enc_question(text);
        selected = false;
        max_score = 0;
        thresh_score = 0;
        thisbot = here;
        botset = <--node::botset[0];
    }
    bot, default_answer
    {
        for
            j in--> node::default_answer : default = j;
        if (default): thresh_score=default.thresh_score;

        for
            i in--> node::answer
            {
                score = use.qa_score(enc, i.encoding);
                if (score[0][0] > max_score)
                {
                    selected = i;
                    max_score = score[0][0];
                }
            }
        std.log(score);
        if(max_score!=0):selected.score = max_score;
    }

    with exit
    {
        if (max_score > thresh_score)
        {

            if (not dont_log):
                    spawn thisbot walker::log_question(text=text, selected=selected, resp_type="answer", metadata=metadata);
            if (selected.hitcount): selected.hitcount+=1;
            else: selected.hitcount=1;
            if (metadata != {"channel" : "ZSB Platform"})
            {
                if (botset.current_transaction_count == "0"):botset.current_transaction_count=1;
                else:botset.current_transaction_count+=1;
            }

            answer = selected;
            if not(no_report): report selected;

        }
        else
        {
            if (default)
            {
                if (not dont_log):
                    spawn thisbot walker::log_question(text=text, selected=default, resp_type="default", metadata=metadata);
                if (default.hitcount): default.hitcount+=1;
                else: default.hitcount=1;
                answer = default;
                if not(no_report): report default;
            }
            else {
                answer = ret = {"context":{"text":"I do not have that information yet. Try another query ?","show_text":"I do not have that information yet. Try another query ?"}};
                if not(no_report): report ret;
            }
        }
    }
}

walker zsb_public_api : anyone
{
    has api_name;
    has text;
    has feedback, metadata;
    has customer_info, session_id, interaction_id;
    has url, send_email = true;

    bot
    {
        if (api_name == "ask_question")
        {
            spawn here walker::ask_question(text = text, metadata = metadata);
        }
        if (api_name == "log_feedback")
        {
            spawn here walker::log_feedback(feedback = feedback, metadata = metadata);
        }
        if (api_name == "log_callback")
        {
            spawn here walker::log_callback(customer_info = customer_info, session_id = session_id, interaction_id = interaction_id, url = url, send_email = send_email);
        }
    }
}


walker ask_question_nolog_noreport
{
    has text;
    has anchor selected;
    can use.enc_question, use.qa_score;

    with entry
    {
        enc = use.enc_question(text);
        selected = false;
        thresh_score = 0;
    }
    bot, default_answer
    {
        for
            j in--> node::default_answer : default = j;
        if (default): thresh_score=default.thresh_score;

        max_score = 0;
        for
            i in--> node::answer
            {
                score = use.qa_score(enc, i.encoding);
                if (score[0][0] > max_score)
                {
                    selected = i;
                    max_score = score[0][0];
                }
            }

        if (max_score < thresh_score)
        {
            if (default)
            {
                selected = default;
            }
        }
    }
}

walker ask_question_testcase
{
    has text;
    has enc;
    has anchor selected;
    can use.enc_question, use.qa_score;

    with entry
    {
        selected = false;
        thresh_score = 0;
    }
    bot, default_answer
    {
        for
            j in--> node::default_answer : default = j;
        if (default): thresh_score=default.thresh_score;

        max_score = 0;
        for
            i in--> node::answer
            {
                score = use.qa_score(enc, i.encoding);
                std.log(score);
                if (score[0][0] > max_score)
                {
                    selected = i;
                    max_score = score[0][0];
                }
            }

        if (max_score < thresh_score)
        {
            if (default)
            {
                selected = default;
            }
        }
    }
}

walker get_question_matches
{
    has text, num_matches, matches, thresh_score;
    can use.enc_question, use.qa_score;

    with entry
    {
        matches = [];
        thresh_score = 0;
    }

    bot, default_answer
    {
       for
           j in--> node::default_answer : default = j;
       if (default): thresh_score=default.thresh_score;

        enc = use.enc_question(text);
        for
            i in--> node::answer
            {
                score = use.qa_score(enc, i.encoding);
                matches += [[score [0] [0], &i]];

            }
             std.log(matches);

    }

    with exit
    {
        if (num_matches > matches.length):
            num_matches=matches.length;
        matches = std.sort_by_col(matches, 0, true);
        if (matches[0][0] < thresh_score): report [thresh_score,&default];
        for
            i = 0 to i < num_matches by i += 1 : report matches[i];
    }
}

//Logging

walker log_question
{
    has text, selected, metadata, botid, log,log_db, default;
    bot
    {
        take--> node::log_chunk else
        {
            spawn here--> node::log_chunk;
            take--> node::log_chunk;
        }
        botid = &here;
    }

    log_chunk
    {
        now = std.time_now();
        log_db = {"datetime" : now, "log_type" : "question", "question" : text, "answerid" : &selected, "answertext" : null, "answer_showtext" : null, "metadata" : metadata, "answertype" : resp_type, "feedback" : null};
        log = {"datetime" : now, "log_type" : "question", "question" : text, "answerid" : &selected, "answertext" : selected.text, "answer_showtext" : selected.show_text, "metadata" : metadata, "answertype" : resp_type, "feedback" : null};

        spawn here walker::prepare_history();

        here.history["date_map"][
            here.history["latest"]
        ].list::insert(0, log_db);

        spawn here walker::create_log_elastic(myobj = log, id = botid);
    }
}

walker log_feedback
{
    has feedback, metadata, botid;
    bot
    {
        take--> node::log_chunk else
        {
            spawn here--> node::log_chunk;
            take--> node::log_chunk;
        }
        botid = &here;
    }

    log_chunk
    {
        if (not here.feedback): here.feedback=[];
        //here.feedback = [ {"datetime" : std.time_now(), "log_type" : "feedback", "feedback" : feedback, "metadata" : metadata} ] + here.feedback;
    }
    with exit
    {
        spawn here walker::update_log_elastic(id = botid, feedback = feedback, metadata = metadata);
    }
}

walker log_callback
{
    has customer_info, session_id, interaction_id;
    has url, send_email = true;
    bot
    {

        take--> node::log_chunk else
        {
            spawn here--> node::log_chunk;
            take--> node::log_chunk;
        }

        if send_email {
            spawn here walker::send_email_for_callback(customer_info = customer_info.dict::copy, session_id = session_id, interaction_id = interaction_id, url = url);
        }

    }

    log_chunk
    {
        _s = session_id.str;

        spawn here walker::prepare_callback();

        if _s not in here.callback["session_map"] {
            here.callback["date_map"][
                here.callback["latest"]
            ].list::insert(0, _s);

            here.callback["session_map"].dict::update({
                _s: {
                    "datetime": date.datetime_now(),
                    "log_type": "callback",
                    "customer_info": customer_info,
                    "session_id": _s,
                    "interaction_id": [interaction_id]
                }
            });
            // current workaround for the issue on not saving using built in
            here.callback["latest"] = here.callback["latest"];
        } else {
            here.callback["session_map"][_s]["interaction_id"].list::append(interaction_id);
            here.callback["session_map"][_s]["customer_info"] = customer_info;
        }
    }
}

walker get_log
{
    has target_answer, for_question=false, from_elastic=true;
    has start_date, end_date, size= 1000, channels;
    can date.date_day_diff;

    bot
    {
        if from_elastic {
            id = &here;
            uuid = id.str::replace('urn:uuid:', '');
            url = std.get_global('elastic_url').str + '/' + std.get_global('elastic_index').str + '-' + uuid + '/_search';
            auth = std.get_global('elastic_auth');

            date_filter = {};

            if (start_date): date_filter["gte"] = start_date;
            if (end_date): date_filter["lte"] = end_date;

            filter = [{ "range": { "datetime": date_filter } }];

            if (channels && channels.length > 0) {
                filter = filter + [{ "terms": { "metadata.channel.keyword": channels } }];
            }

            if target_answer {
                filter = filter + [{ "wildcard": {"answerid": "*" + target_answer.str + "*"} }];
            }

            myobj = {
                "size": size,
                "query": { "bool": { "filter": filter } }
            };
            report request.get(url, myobj, {"Authorization" : auth, "Content-Type" : "application/json"});
        } else: take--> node::log_chunk;

    }

    log_chunk
    {
        spawn here walker::prepare_history();

        history = [];
        limit = 0;

        for dt in here.history["dates"] {
            if date.date_day_diff(dt) <= 60 {
                if target_answer {
                    for i in here.history["date_map"][dt] {
                        if for_question {
                            if "answerid" in i && target_answer in i["answerid"]:
                                report[i["question"], i["datetime"]];
                        } else:
                            if  (
                                    "answerid" in i &&
                                    target_answer in i["answerid"]
                                ) || (
                                    "context" in i &&
                                    "answerid" in i["context"] &&
                                    target_answer in i["context"]["answerid"]
                                ):
                                report i;
                                limit += 1;
                                if limit >= size.int: disengage;
                    }
                } else {
                    history.list::extend(here.history["date_map"][dt]);
                }
            }
            else: break;
        }
        if not(target_answer): report history[0:size.int];
    }
}

walker drain_log
{
    bot
    {
        take--> node::log_chunk;
    }
    log_chunk
    {
        spawn here walker::prepare_history();

        report here.history["date_map"];

        here.history = {
            "dates": [],
            "date_map": {},
            "latest": ""
        };
    }
}

// APi for date filter of log history
walker get_log_date_filter
{
    has start_date, end_date;
    bot
    {
        take--> node::log_chunk;
    }
    log_chunk
    {
        spawn here walker::prepare_history();

        history = [];

        for dt in here.history["dates"]:
            if date.date_day_diff(dt) <= 60:
                if start_date {
                    if start_date.str::split("T")[0] > dt: continue;
                    elif end_date:
                        if end_date < dt: continue;
                        else {
                            for hist in here.history["date_map"][dt]:
                                if hist["datetime"] >= start_date && hist["datetime"] <= end_date:
                                    history.list::append(hist);
                        }
                    else:
                        for hist in here.history["date_map"][dt]:
                            if hist["datetime"] >= start_date:
                                history.list::append(hist);
                } else {
                    if end_date:
                        if end_date < dt: continue;
                        else {
                            for hist in here.history["date_map"][dt]:
                                if hist["datetime"] <= end_date:
                                    history.list::append(hist);
                        }
                    else: history.list::extend(here.history["date_map"][dt]);
                }
            else: break;

        report history;
    }
}

walker get_log_date_filter_elastic
{
    has start_date, end_date, id, size, channels;
    can request.get;
    with entry
    {
        if not(start_date) : start_date = std.time_now();
        if not(end_date) : end_date = start_date;
        if not(size) : size = 1000;
        auth = std.get_global('elastic_auth');
    }
    bot
    {
        id = &here;
    }

    with exit
    {
        uuid = id.str::replace('urn:uuid:', '');
        url = std.get_global('elastic_url').str + '/' + std.get_global('elastic_index').str + '-' + uuid + '/_search';
        filter = [{ "range": { "datetime": { "gte": start_date, "lte": end_date } } }];

        if (channels && channels.length > 0) {
            filter = filter + [{ "terms": { "metadata.channel.keyword": channels } }];
        }

        myobj = {
            "size": size,
            "query": { "bool": { "filter": filter } },
            "aggs": { "unique_answers": { "cardinality": { "field": "answerid" } }, "answer_count": { "terms": { "field": "answerid" } }, "question_count": { "categorize_text": { "field": "question" } }, "default_count": { "terms": { "field": "answertype" } }, "feedback_count": { "terms": { "field": "feedback" } }, "session_count": { "cardinality": { "field": "metadata.sessionID.keyword" } }, "visitor_count": { "cardinality": { "field": "metadata.visitorID" } } }
        };
        std.log(myobj);
        report request.get(url, myobj, {"Authorization" : auth, "Content-Type" : "application/json"});
    }
}


walker get_log_date_filter_graph_elastic
{
    has start_date, end_date,start_range,end_range,interval, format, id, channels;
    can request.get;
    with entry
    {
        if
            not(start_date) : start_date = std.time_now();
        if
            not(end_date) : end_date = start_date;
        if not(format) : format = "date_time";
        auth = std.get_global('elastic_auth');
    }
    bot
    {
        id = &here;
    }

    with exit
    {
        uuid = id.str::replace('urn:uuid:', '');
        url = std.get_global('elastic_url').str + '/' + std.get_global('elastic_index').str + '-' + uuid + '/_search';

        filter = [{ "range": { "datetime": { "gte": start_date, "lte": end_date } } }];
        if (channels && channels.length > 0) {
            filter = filter + [{ "terms": { "metadata.channel.keyword": channels } }];
        }

        myobj = {
            "size": 10000,
            "query": { "bool": { "filter": filter } },
            "aggs": { "question_count": { "date_histogram": { "field": "datetime", "fixed_interval": interval, "extended_bounds": { "min": start_range, "max": end_range } } } }
        };

        std.log(myobj);
        report request.get(url, myobj, {"Authorization" : auth, "Content-Type" : "application/json"});
    }
}

walker get_log_filter_elastic
{
    has filter_key, filter_value, id, filter_obj;
    can request.get;
    with entry
    {
        auth = std.get_global('elastic_auth');
        filter_obj = {};
        if (filter_key == "interactionID"):filter_obj={"metadata.interactionID":filter_value};
        elif (filter_key == "sessionID") : filter_obj = {"metadata.sessionID" : filter_value};
        //if (filter_value):filter_obj.filter_value=filter_value;
        //report filter_obj;
    }
    bot
    {
        id = &here;
    }

    with exit
    {
        uuid = id.str::replace('urn:uuid:', '');
        url = std.get_global('elastic_url') + '/' + std.get_global('elastic_index') + '-' + uuid + '/_search';
        aggs = std.get_global('elastic_aggs');
        myobj = {"size" : 10000, "query" : {"match" : filter_obj}, "aggs" : aggs};
        std.log(myobj);
        report request.get(url, myobj, {"Authorization" : auth, "Content-Type" : "application/json"});
    }
}

walker get_feedback_date_filter
{
    has start_date, end_date;
    with entry
    {
        if
            not(start_date) : start_date = std.time_now();
        if
            not(end_date) : end_date = start_date;
    }
    bot
    {
        take--> node::log_chunk;
    }
    log_chunk
    {
        if (not here.feedback): disengage;
            for
                i in here.feedback
                {
                    if ((&i['datetime']) >= start_date && (&i['datetime']) <= end_date)
                    {
                        report i;
                    }
                    else
                    {
                        if ((&i['datetime']) < start_date)
                        {
                            disengage;
                        }
                    }
                }
    }
}

walker get_callback_date_filter
{
    has start_date, end_date;

    bot {
        take--> node::log_chunk;
    }

    log_chunk {
        spawn here walker::prepare_callback();
        for dt in here.callback["dates"] {
            if date.date_day_diff(dt) <= 60 {
                if start_date {
                    if start_date.str::split("T")[0] > dt: continue;
                    elif end_date:
                        if end_date < dt: continue;
                        else {
                            for ss in here.callback["date_map"][dt] {
                                cb = here.callback["session_map"][ss];
                                if cb["datetime"] >= start_date && cb["datetime"] <= end_date:
                                    report cb;
                            }
                        }
                    else:
                        for ss in here.callback["date_map"][dt] {
                            cb = here.callback["session_map"][ss];
                            if cb["datetime"] >= start_date:
                                report cb;
                        }
                } else {
                    if end_date:
                        if end_date < dt: continue;
                        else {
                            for ss in here.callback["date_map"][dt] {
                                cb = here.callback["session_map"][ss];
                                if cb["datetime"] <= end_date:
                                    report cb;
                            }
                        }
                    else:
                        for ss in here.callback["date_map"][dt]:
                            report here.callback["session_map"][ss];
                }
            }
        }
    }
}

walker get_question_log
{
    has target_answer, from_elastic=true;
    has start_date, end_date, size = 1000, channels;
    bot {
        spawn here walker::get_log(
            target_answer=target_answer, for_question=true, from_elastic=from_elastic,
            start_date=start_date, end_date=end_date, size=size, channels=channels
        );
    }
}

// External API Integration

walker create_log_elastic
{
    has url, myobj, id, uuid, auth;
    can request.post;

    log_chunk
    {
        uuid = id.str::replace('urn:uuid:', '');
        auth = std.get_global('elastic_auth');
        url = std.get_global('elastic_url').str + '/' + std.get_global('elastic_index').str + '-' + uuid + '/_doc';
        try {
            request.post(url, myobj, {"Authorization" : auth.str, "Content-Type" : "application/json"});
        } else with err {
            log_db = {"datetime" : std.time_now(), "log_type" : "elastic_log", "id" : id, "context" : myobj, "error" : err};

            here.history["date_map"][
                here.history["latest"]
            ].list::insert(0, log_db);
            // current workaround for the issue on not saving using built in
            here.history["latest"] = here.history["latest"];
            report:error = err;
        }
    }
}

walker update_log_elastic
{
    has url, myobj, id, uuid, metadata, feedback;
    can request.post;
    with entry
    {
        uuid = id.str::replace('urn:uuid:', '');
        url = std.get_global('elastic_url') + '/' + std.get_global('elastic_index') + '-' + uuid + '/_update_by_query';
        auth = std.get_global('elastic_auth');
        if (metadata)
        {
            interactionID = metadata['interactionID'];
            feedback_str = std.log(feedback);
            myobj = {"script" : {"source" : "ctx._source.feedback=" + feedback_str}, "query" : {"match" : {"metadata.interactionID" : interactionID}}};
            report request.post(url, myobj, {"Authorization" : auth, "Content-Type" : "application/json"});
        }
    }
}

// Linking of a question to an answer

walker link_question
{
    has text, answerid;
    has thisbot, actual_answer, actual_link_array;
    can use.enc_answer, use.dist_score;
    with entry
    {
        thisbot = <--node::bot[0];
    }

    answer
    {
        answerid = &here;
        actual_link_array = here.qlinks;
        if (here.qlinks)
        {
            if (not text in here.qlinks): here.qlinks += [text];
        }
        else: here.qlinks = [text];
        pretext = "";
        if (here.qlinks)
        {for
                i in here.qlinks : pretext += i;
        }
        old_enc = here.encoding;
        here.encoding = use.enc_answer(pretext + text);
        actual_answer = spawn thisbot walker::ask_question_nolog_noreport(text = text);
        if ((&actual_answer) != answerid)
        {
            here.encoding = old_enc;
            here.qlinks = actual_link_array;
            report[[0]];
            disengage;
        }
        else: report use.dist_score(old_enc, here.encoding);
    }
}

walker unlink_question
{
    has idx;
    can use.enc_answer, use.dist_score;

    answer
    {
        if (not here.qlinks or here.qlinks.length < idx):
            report "Index out of range!";
        else
        {
            destroy here.qlinks[idx];
            pretext = "";
            for
                i in here.qlinks : pretext += i;
            old_enc = here.encoding;
            here.encoding = use.enc_answer(pretext + here.text);
            report use.dist_score(old_enc, here.encoding);
        }
    }
}

// Global Setter only works for Admin
walker global_var_setter
{
    has plan_obj, plan_var_name;
    std.set_global(plan_var_name, plan_obj);
    report plan_obj;
}

// Global Multi Setter only works for Admin
walker multi_global_var_setter
{
    has plan_arr;
    with entry
    {
        for
            i in plan_arr
            {
                spawn here walker::global_var_setter(plan_var_name = i['plan_var_name'], plan_obj = i['plan_obj']);
            }
    }
}

// Global Setter works for all users
walker global_var_getter
{
    has plan_var_name;
    global_obj = std.get_global(plan_var_name);
    report global_obj;
}

node data_nugget { has anchor name, data; }
walker create_nugget
{
    has name, data;

    spawn here--> node::data_nugget(name = name, data = data);
}

walker get_nugget
{
    has name;
    report--> node::data_nugget == name;
}
walker delete_nugget
{
    has name;
    destroy--> node::data_nugget == name;
}
walker update_nugget
{
    has name, data;
    n = --> node::data_nugget == name;
    if (n): n.data=data;
}

walker admin_data
{

    root
    {
        report-->;

    }

}

//Jira walkers

walker jira_create_issue {
    has projectKey, title, body, labels, issueType, files;
    can request.get;

    with entry {
        jira_auth = std.get_global('jira_auth');
        jira_host = std.get_global('jira_host');
        jira_env = std.get_global('jira_env');

        headers = {
            "Authorization": "Basic " + jira_auth,
            "Content-Type": "application/json"
        };
        url = jira_host + "/rest/api/2/issue";
        error = [];
        if (!projectKey): error = error + ["projectKey is required!"];
        if (!title): error = error + ["title is required!"];
        if (!body): error = error + ["body is required!"];
        if (!labels): error = error + ["labels is required!"];
        if (!issueType): error = error + ["issueType is required!"];
    }

    with exit {
        if (error.length > 0) {
            report {
                "errors": error
            };
        } else {
            getRes = request.post(url, {
                "fields": {
                    "project": {
                        "id": projectKey
                    },
                    "issuetype": {
                        "id": issueType
                    },
                    "customfield_10010": "zsbs/systemproblem",
                    "summary": title,
                    "description": body,
                    "labels": labels + [jira_env]
                }
            }, headers);
            report getRes;

            if (getRes.status_code == 201) {
                issueIdOrKey = getRes.response.key;
                if(issueIdOrKey && files && files.length > 0) : spawn here walker::jira_upload_attachment(issueIdOrKey = issueIdOrKey, files = files);
            }
        }
    }
}

walker jira_update_issue {
    has issueIdOrKey, title, body, files;
    can request.get;

    with entry {
        jira_auth = std.get_global('jira_auth');
        jira_host = std.get_global('jira_host');

        headers = {
            "Authorization": "Basic " + jira_auth,
            "Content-Type": "application/json"
        };

        error = [];
        if (!issueIdOrKey): error = error + ["issueIdOrKey is required!"];
        if (!title && !body): error = error + ["Please specify field to update!"];
        else : url = jira_host + "/rest/api/2/issue/" + issueIdOrKey.str;
    }

    with exit {
        if (error.length > 0) {
            report {
                "errors": error
            };
        } else {
            req = {
                "fields": {}
            };
            if (title): req.fields["summary"] = title.str;
            if (body): req.fields["description"] = body.str;
            report request.put(url, params = req, headers);

            if (issueIdOrKey && files && files.length > 0) : spawn here walker::jira_upload_attachment(issueIdOrKey = issueIdOrKey, files = files);
        }
    }
}

walker jira_get_issue {
    has issueIdOrKey, jql, startAt, maxResults;
    can request.get;

    with entry {
        jira_auth = std.get_global('jira_auth');
        jira_host = std.get_global('jira_host');
        headers = {
            "Authorization": "Basic " + jira_auth,
            "Content-Type": "application/json"
        };
        url = jira_host + "/rest/api/2";

        if (!issueIdOrKey) {
            if (!startAt): startAt = 0;
            if (!maxResults): maxResults = 5;
            if (!jql): jql = "";
            url += "/search?jql=" + jql + "&startAt=" + startAt.str + "&maxResults=" + maxResults.str;
        } else :url += "/issue/" + issueIdOrKey.str;
    }

    with exit {
        report request.get(url, {}, headers);
    }
}

walker jira_add_comment {
    has issueIdOrKey, body;
    can request.get;

    with entry {
        jira_auth = std.get_global('jira_auth');
        jira_host = std.get_global('jira_host');

        headers = {
            "Authorization": "Basic " + jira_auth,
            "Content-Type": "application/json"
        };

        error = [];
        if (!issueIdOrKey): error = error + ["issueIdOrKey is required!"];
        if (!body): error  = error + ["body is required!"];
        else : url = jira_host + "/rest/api/2/issue/" + issueIdOrKey.str + "/comment";
    }

    with exit {
        if (error.length > 0) {
            report {
                "errors": error
            };
        } else {
            report request.post(url, params = {"body": body}, headers);
        }
    }
}

walker jira_get_comment {
    has issueIdOrKey;
    can request.get;

    with entry {
        jira_auth = std.get_global('jira_auth');
        jira_host = std.get_global('jira_host');

        headers = {
            "Authorization": "Basic " + jira_auth,
            "Content-Type": "application/json"
        };

        error = [];
        if (!issueIdOrKey): error = error + ["issueIdOrKey is required!"];
        else : url = jira_host + "/rest/api/2/issue/" + issueIdOrKey.str + "/comment";
    }

    with exit {
        if (error.length > 0) {
            report {
                "errors": error
            };
        } else {
            report request.get(url, {}, headers);
        }
    }
}

walker jira_upload_attachment {
    has issueIdOrKey, files;
    can request.multipart_base64;

    with entry {
        jira_auth = std.get_global('jira_auth');
        jira_host = std.get_global('jira_host');

        headers = {
            "Authorization": "Basic " + jira_auth,
            "X-Atlassian-Token": "no-check"
        };

        error = [];
        if (!issueIdOrKey): error = error + ["issueIdOrKey is required!"];
        if (!files || files.length == 0): error = error + ["files is required!"];

        url = jira_host + "/rest/api/2/issue/" + issueIdOrKey.str + "/attachments";
    }

    with exit {
        if (error.length > 0) {
            report {
                "errors": error
            };
        } else {
            report request.multipart_base64(url, files = files, header = headers);
        }
    }
}


walker jira_delete_attachment {
    has attachmentId;
    can request.delete;

    with entry {
        jira_auth = std.get_global('jira_auth');
        jira_host = std.get_global('jira_host');

        headers = {
            "Authorization": "Basic " + jira_auth,
            "Content-Type": "application/json"
        };

        error = [];
        if (!attachmentId): error = error + ["attachmentId is required!"];

        url = jira_host + "/rest/api/2/attachment/" + attachmentId.str;
    }

    with exit {
        if (error.length > 0) {
            report {
                "errors": error
            };
        } else {
            report request.delete(url, {}, header = headers);
        }
    }
}

walker jira_download_attachment {
    has attachmentId;
    can request.get, request.file_download_base64;

    with entry {
        jira_auth = std.get_global('jira_auth');
        jira_host = std.get_global('jira_host');

        headers = {
            "Authorization": "Basic " + jira_auth,
            "Content-Type": "application/json"
        };

        error = [];
        if (!attachmentId): error = error + ["attachmentId is required!"];

        url = jira_host + "/rest/api/2/attachment/" + attachmentId.str;
        url_download = jira_host + "/rest/api/2/attachment/content/" + attachmentId.str;
    }

    with exit {
        if (error.length > 0) {
            report {
                "errors": error
            };
        } else {
            getRes = request.get(url, {}, header = headers);
            if (getRes["status_code"] == 200){
                getRes.content = request.file_download_base64(url_download, header = headers);
            }
            report getRes;
        }
    }
}




walker text_summarization {
    can cl_summer.summarize;

    has path = null;
    has text = null;
    has sentence_count = 10;
    has doc_type="text";  // url or text
    has url = null;
    has content_type="default";

    if (doc_type == "technical") {
        sum_type = "LuhnSummarizer";
    } else {
        sum_type = "LsaSummarizer";
    }

    if (doc_type=="url")
    {
        summarized_data = cl_summer.summarize(text="none", url=url, sent_count=sentence_count, summarizer_type=sum_type);

    }
    else
    {
            summarized_data = cl_summer.summarize(text=text, url="none", sent_count=sentence_count, summarizer_type=sum_type);
    }

    report summarized_data;

}


walker messenger_callback: anyone {
    can request.post;

    integration {
        report:status = 403;
        report:custom = {"err_msg": "Forbidden Request!"};

        req_ctx = global.info["request_context"];

        method = req_ctx.method;
        msg_conf = std.get_global("messenger_config");

        if ( method == "GET" ) {

            mode = req_ctx.query["hub.mode"];
            token = req_ctx.query["hub.verify_token"];
            challenge = req_ctx.query["hub.challenge"];

            if (mode == "subscribe" && token.str == msg_conf["verify_token"]) {
                report:status = 200;
                report:custom = challenge.int;
            }

        } elif ( method == "POST" ) {

            body = req_ctx.body;

            if ( "object" in body && body["object"] == "page" ) {

                _bot = <-- node::bot[0];
                for ent in body["entry"] {
                    for msg in ent["messaging"] {
                        answer = spawn _bot walker::ask_question(text = msg["message"]["text"], metadata = {
                            "visitorID": msg["sender"]["id"],
                            "sessionID": msg["sender"]["id"],
                            "interactionID": msg["message"]["mid"],
                            "channel": "facebook_messenger"
                        }, no_report = true);

                        request.post(msg_conf["url"] + here.settingsobj.fbMessengerToken,
                        {
                            "messaging_type": "RESPONSE",
                            "recipient": {
                                "id": msg["sender"]["id"]
                            },
                            "message": {
                                "text": answer.show_text
                            }
                        }, null);
                    }

                }
                report:status = 200;
                report:custom = {};
            }
        }
    }
}

walker prepare_history {
    can date.date_day_diff, date.date_now;
    log_chunk {
        _date = date.date_now();
        if not here.history {
            here.history = {
                "dates": [_date],
                "date_map": {
                    _date: []
                },
                "latest": _date
            };
        } else {
            if here.history.type != dict {
                _temp = {
                    "dates": [_date],
                    "date_map": {
                        _date: []
                    },
                    "latest": _date
                };

                if (here.history && (len = here.history.length) > 0) {
                    _temp["latest"] = here.history[0]["datetime"].str::split("T")[0];
                    _temp["dates"] = [_temp["latest"]];
                    _temp["date_map"] = {
                        _temp["latest"]: here.history
                    };
                }
                here.history = _temp;
            } else {
                while date.date_day_diff(
                    here.history["dates"][-1]
                ) > 120 {
                    here.history["date_map"].dict::pop(
                        here.history["dates"].list::pop
                    );
                }
            }

            if here.history["latest"] != _date {
                here.history["dates"].list::insert(0, _date);
                here.history["date_map"][_date] = [];
                here.history["latest"] = _date;
            }
        }
    }
}
walker send_email_for_callback {
    has customer_info, session_id, interaction_id, url;
    can mail.send;

    bot {
        mc = here.mail_config;
        if mc && mc.dict::get("enabled", false) {
            subject = "ZSB Notification: Callback Request for " + session_id.str;
            recipients = mc.dict::get("recipients", []);

            if not url {
                url = "about:blank";
            }

            name = customer_info.dict::pop("name", "N/A");
            email = customer_info.dict::pop("email", "N/A");
            phoneNumber = customer_info.dict::pop("phoneNumber", "N/A");

            otherDetails_text = "";
            otherDetails_html = "";

            for k, v in customer_info {
                otherDetails_text += "\n  " + k.str + ": " + v.str;
                otherDetails_html += "<br>&nbsp;&nbsp;<b>" + k.str + "</b>: " + v.str;
            }

            if otherDetails_text {
                otherDetails_text = "Other Details:" + otherDetails_text.str;
                otherDetails_html = "<p><b>Other Details</b>:" + otherDetails_html.str + "</p>";
            }

            text = "\n".str::join([
                "Hello,",
                "A callback has been requested on your bot. Please see customer details below.",
                "Customer Name: " + name.str,
                "Customer Email: " + email.str,
                "Customer Phone Number: " + phoneNumber.str,
                otherDetails_text + "This request can be viewed on this link " + url.str
            ]);

            html = "<br>".str::join([
                "Hello,",
                "A callback has been requested on your bot. Please see customer details below.",
                "<b>Customer Name</b>: " + name.str,
                "<b>Customer Email</b>: " + email.str,
                "<b>Customer Phone Number</b>: " + phoneNumber.str,
                otherDetails_html + 'This request can be viewed on this session <a href="' + url.str +'" target="_blank">' + session_id.str + "</a>"
            ]);

            if recipients {
                mail.send(null, recipients, subject, text, html);
                disengage;
            }
        }
        report:error = "mail_config is not yet configured!";
    }
}

walker prepare_callback {
    can date.date_day_diff, date.date_now;
    log_chunk {
        _date = date.date_now();
        if not here.callback {
            here.callback = {
                "dates": [_date],
                "date_map": {
                    _date: []
                },
                "session_map": {},
                "latest": _date
            };
        } else {
            if here.callback.type != dict {
                _temp = {
                    "dates": [_date],
                    "date_map": {
                        _date: []
                    },
                    "session_map": {},
                    "latest": _date
                };

                if (here.callback && (len = here.callback.length) > 0) {
                    for cb in here.callback {

                        cb["migrated"] = true;

                        _s = cb["session_id"].str;
                        _d = cb["datetime"].str::split("T")[0];
                        if _d in _temp["date_map"] {
                            _temp["date_map"][_d].list::append(_s);
                        } else {
                            _temp["dates"].list::append(_d);
                            _temp["date_map"][_d] = [_s];
                        }

                        // since callback is descending only first will be saved (latest)
                        if not (_s in _temp["session_map"]) {
                            _temp["session_map"][_s] = cb;
                        }
                    }
                }
                here.callback = _temp;
            } else {
                while date.date_day_diff(
                    here.callback["dates"][-1]
                ) > 120 {
                    _ss = here.callback["date_map"].dict::pop(
                        here.callback["dates"].list::pop
                    );
                    for _s in _ss {
                        here.callback["session_map"].dict::pop(_s);
                    }
                }
            }

            if here.callback["latest"] != _date {
                here.callback["dates"].list::insert(0, _date);
                here.callback["date_map"][_date] = [];
                here.callback["latest"] = _date;
            }
        }
    }
}

/////////////////////////////////////// STRIPE WALKERS ///////////////////////////////////////

walker zsb_stripe_webhook: anyone {
    root {
        req_ctx = global.info['request_context'];
        req_data = req_ctx['body']['data']['object'];
        event_type = req_ctx['body']['type'];
    }
}

// ////////////////////////////// CUSTOMER WALKER ////////////////

walker create_customer {
  has email,
      name,
      metadata,
      payment_method,
      address,
      metadata;

  can stripe.create_customer;

  root {
    try {
      report:status = 201;
      report stripe.create_customer(email=email, name=name, metadata=metadata, address=address, payment_method_id=payment_method);
    } else with error {
      report error;
      report:error = error;
    }
  }
}

walker get_customer {
  has customer_id;
  can stripe.get_customer;

  with entry {
    if( !customer_id ) {
        report:status = 400;
        report:custom = { "message": "No customer id provided", "success": false};
        disengage;
    }
  }

  try {
    report stripe.get_customer(customer_id=customer_id);
  } else with error {
    report error;
    report:error = error;
  }
}

walker get_customer_payment_methods {
  has customer_id;
  can stripe.get_payment_methods;

  try {
    report stripe.get_payment_methods(customer_id=customer_id);
  } else with error {
    report error;
    report:error = error;
  }
}

walker add_payment_method {
  has payment_method_id, customer_id;
  can stripe.attach_payment_method;

  try {
    report stripe.attach_payment_method(payment_method_id=payment_method_id, customer_id=customer_id);
  } else with error {
    report error;
    report:error = error;
  }
}

walker update_payment_method {
  has payment_method_id, customer_id;
  can stripe.update_default_payment_method;

  try {
    report stripe.update_default_payment_method(customer_id=customer_id, payment_method_id=payment_method_id);
  } else with error {
    report error;
    report:error = error;
  }
}

///////////////////////////////// SUBSCRIPTION //////////////////////////////////
walker create_trial_subscription {
  has customer_id, payment_method_id = "", items = [], trial_period_days = 14, expand = ['latest_invoice.payment_intent'];
  can stripe.create_trial_subscription;

  with entry {
    if( !customer_id ) {
        report:status = 400;
        report:custom = { "message": "No customer id provided", "success": false};
        disengage;
    }

    if( items.length < 1 ) {
        report:status = 400;
        report:custom = { "message": "No item is provided", "success": false};
        disengage;
    }
  }


  try {
    report:status = 201;
    report stripe.create_trial_subscription(payment_method_id, customer_id, items, trial_period_days, expand);
  } else with error {
    report error;
    report:error = error;
  }
}

walker get_subscription {
  has subscription_id;
  can stripe.get_subscription;

  with entry {
    if( !subscription_id ) {
        report:status = 400;
        report:custom = { "message": "No subscription id provided", "success": false};
        disengage;
    }
  }

  try {
    report stripe.get_subscription(subscription_id);
  } else with error {
    report error;
    report:error = error;
  }
}