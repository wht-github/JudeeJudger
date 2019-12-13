from peewee import *
from playhouse.pool import PooledPostgresqlExtDatabase
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict
import json
from playhouse.postgres_ext import *
import logging

# from peewee import BaseModelSelect

logger = logging.getLogger("peewee")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


result_map = {
    -2: "COMPILE_ERROR",
    -1: "WRONG_ANSWER",
    0: "ACCEPTED",
    1: "CPU_TIME_LIMIT_EXCEEDED",
    2: "REAL_TIME_LIMIT_EXCEEDED",
    3: "MEMORY_LIMIT_EXCEEDED",
    4: "RUNTIME_ERROR",
    5: "SYSTEM_ERROR",
    6: "PENDING",
    7: "JUDGING",
    8: "PARTIALLY_ACCEPTED",
}


with open("./conf.d/database.json", "r") as f:
    setting = json.load(f)

database_name = "Judee_dev"
# database_name = 'postgres'

db = PooledPostgresqlExtDatabase(database_name, **setting)


class BaseModel(Model):
    class Meta:
        database = db


class submission(BaseModel):
    ID = IntegerField(primary_key=True)
    create_time = DateTimeField()
    code = TextField()
    result = IntegerField()
    info = BinaryJSONField()
    language = CharField(max_length=15)
    ip = TextField()
    contest_id = IntegerField()
    problem_id = IntegerField()
    username_id = CharField(max_length=50)
    memory_cost = IntegerField()
    score = IntegerField()
    time_cost = IntegerField()
    compile_error_info = TextField()

    class Meta:
        db_table = "submission"


class oi_contest_rank(BaseModel):
    id = IntegerField(primary_key=True)
    submission_number = IntegerField()
    total_score = IntegerField()
    submission_info = BinaryJSONField()
    contest_id = IntegerField()
    user_id = CharField(max_length=50)

    class Meta:
        db_table = "oi_contest_rank"


class problem(BaseModel):
    ID = IntegerField(primary_key=True)
    is_public = BooleanField()
    title = TextField()
    description = TextField()
    input_description = TextField()
    output_description = TextField()
    samples = BinaryJSONField()
    test_case_score = BinaryJSONField()
    hint = TextField()
    languages = BinaryJSONField()
    template = BinaryJSONField()
    create_time = TimestampField()
    last_update_time = TimestampField()
    time_limit = IntegerField()
    memory_limit = IntegerField()
    difficulty = IntegerField()
    source = TextField()
    total_score = IntegerField()
    submission_number = BigIntegerField()
    accepted_number = BigIntegerField()
    statistic_info = BinaryJSONField()
    created_by_id = CharField(max_length=50)

    class Meta:
        db_table = "problem"


class contest(BaseModel):
    id = IntegerField(primary_key=True)
    title = CharField(max_length=128)
    description = TextField()
    password = TextField()
    rule_type = TextField()
    start_time = TimestampField()
    end_time = TimestampField()
    create_time = TimestampField()
    last_update_time = TimestampField()
    visible = BooleanField()
    allowed_ip_ranges = BinaryJSONField()
    created_by_id = CharField(max_length=50)

    class Meta:
        db_table = "contest"


class user_userdata(BaseModel):
    ac = IntegerField()
    submit = IntegerField()
    score = IntegerField()
    ranking = IntegerField()
    ac_prob = TextField()
    username_id = CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = "user_userdata"


def get_submission_by_id(id, dic=False):
    '''
    get submission table infomation by submission id
    return model
    '''
    try:
        with db.connection_context():
            # result = submission.get(submission.ID == id)
            result = submission.select().where(submission.ID == id).get()
            if dic:
                result = model_to_dict(result)
            # id
            return result
    except:
        # print(f'submission with id {id} not exist')
        return None


def get_problem_info(id, dic=False):
    '''
    get time_limit, memory_limit and test_case_score of probem table by problem id
    return none if sth bad happen, else return number of affected rows 
    '''
    try:
        with db.connection_context():
            result = (
                problem.select(
                    problem.time_limit, problem.memory_limit, problem.test_case_score
                )
                .where(problem.ID == id)
                .get()
            )
            if dic:
                result = model_to_dict(result)
            # id
            return result
    except:
        return None


def get_contest_type(id, dic=False):
    '''
    get rule_type of contest table by contest id
    return none if sth bad happen, else return number of affected rows 
    '''
    try:
        with db.connection_context():
            result = contest.select(contest.rule_type).where(contest.id == id).get()
            if dic:
                result = model_to_dict(result)
            # id
            return result
    except:
        return None


def get_score(info, result, test_case_info=None):
    score = 0
    if test_case_info:
        scores = test_case_info
    else:
        with db.connection_context():
            scores = (
                submission.select(problem.test_case_score)
                .join(problem, on=(submission.problem_id == problem.ID))
                .where(submission.ID == id)
                .get()
                .problem.test_case_score
            )

    for a in range(len(info)):
        score += scores[a] if info[a].get(result, -1) == 0 else 0

    return score


def update_submission_by_id(id, result, compile_error_info=None):
    '''
    if no compile_error_info, it only update result by id
    else it update result and compile_error_info by id
    '''
    with db.connection_context():
        if compile_error_info:
            a = (
                submission.update(result=result, compile_error_info=compile_error_info)
                .where(submission.ID == id)
                .execute()
            )
        else:
            a = submission.update(result=result).where(submission.ID == id).execute()
        # affect num
        return a


def update_submission_userdata(
    id, result, info, username_id=None, problem_id=None, test_case_info=None
):
    '''
    it will update result, info, time_cost, memory_cost, score in submission by id
    and it will invoke update_userdata() to update userdata table
    you'd better give me username_id and problem_id and test_case_info, but it not must
    '''
    time_cost = 0
    memory_cost = 0
    score = 0

    if test_case_info:
        scores = test_case_info
    else:
        with db.connection_context():
            scores = (
                submission.select(problem.test_case_score)
                .join(problem, on=(submission.problem_id == problem.ID))
                .where(submission.ID == id)
                .get()
                .problem.test_case_score
            )

    for a in range(len(info)):
        time_cost += info[a].get("cpu_time", 0)
        memory_cost = max(memory_cost, info[a].get("memory", 0))
        score += scores[a] if info[a].get('result', -1) == 0 else 0

    if username_id and problem_id:
        user_id = username_id
        pro_id = problem_id
    else:
        with db.connection_context():
            temp = (
                submission.select(submission.username_id, submission.problem_id)
                .where(submission.ID == id)
                .get()
            )
            user_id = temp.problem_id
            pro_id = temp.problem_id

    update_userdata(user_id, pro_id, result, score)
    # result_info = {'time_cost' : time_cost, 'memory_cost' : memory_cost, 'score' : score, 'result' : info}

    with db.connection_context():
        return (
            submission.update(
                result=result,
                info=info,
                time_cost=time_cost,
                memory_cost=memory_cost,
                score=score,
            )
            .where(submission.ID == id)
            .execute()
        )


def update_userdata(user_id, problem_id, result, score):
    '''
    it will update submit, ac, ac_prob and score
    remember invoke this method before the submission with this score have been written in submission table
    '''
    with db.connection_context():
        userdata = (
            user_userdata.select(
                user_userdata.ac,
                user_userdata.submit,
                user_userdata.score,
                user_userdata.ac_prob,
            )
            .where(user_userdata.username_id == user_id)
            .get()
        )

        userdata.submit += 1

        ac_prob = list(map(lambda x: int(x.strip()), userdata.ac_prob.split()))
        if problem_id not in ac_prob:
            userdata.ac += 1
            userdata.ac_prob += "|%d" % problem_id

        submissions = submission.select(submission.score).where(
            submission.problem_id == problem_id,
            submission.username_id == user_id
        )
        max_score = 0
        for a in submissions:
            max_score = max(max_score, 0 if not a.score else a.score)
        add_score = max(score - max_score, 0)
        userdata.score += add_score

        return userdata.save()


def update_ocrank_by_cid_uid(contest_id, user_id, submission_add, total_score_add):
    '''
    update oi_contest_rank
    '''
    try:
        with db.connection_context():
            # a = oi_contest_rank.get(oi_contest_rank.contest_id == contest_id and oi_contest_rank.user_id == user_id)
            a = (
                oi_contest_rank.select(
                    oi_contest_rank.id,
                    oi_contest_rank.submission_number,
                    oi_contest_rank.total_score,
                )
                .where(
                    oi_contest_rank.contest_id == contest_id
                    and oi_contest_rank.user_id == user_id
                )
                .get()
            )
            a.submission_number += submission_add
            a.total_score += total_score_add
            b = a.save()
            # affect num
            return b
    except Exception as e:
        raise e
        return None


def update_problem_by_id(id, result):
    '''
    update problem
    '''
    with db.connection_context():
        a = (
            problem.select(
                problem.ID,
                problem.submission_number,
                problem.accepted_number,
                problem.statistic_info,
            )
            .where(problem.ID == id)
            .get()
        )
        a.submission_number += 1
        if result == 0:
            a.accepted_number += 1
        name = result_map[result]
        num = a.statistic_info.get(name, 0)
        a.statistic_info[name] = num + 1
        b = a.save()
        # affect num
        return b


# with db.connection_context():
#     scores = submission.select(problem.test_case_score).join(problem, on=(submission.problem_id == problem.ID)).where(submission.ID == 1).get()
# scores = scores.problem.test_case_score
# print(scores)


# update_problem_by_id(28, 0)


# use example

# a = get_submission_by_id(4)
# if a is not None:
#     print(a.problem_id)

# a = get_submission_by_id(4,dic=True)
# if a is not None:
#     print(a['code'])

# info = {'a':2,'b':3}
# info2 = {'a':3,'b':2}
# a = update_submission_by_id(6,1,info,info2)

# a = update_ocrank_by_cid_uid(1,1,2,100)

