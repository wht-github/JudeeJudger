from peewee import (
    Model,
    IntegerField,
    TextField,
    CharField,
    DateTimeField,
    BooleanField,
    TimestampField,
    BigIntegerField,
    fn,
)
from playhouse.pool import PooledPostgresqlExtDatabase
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict
import json
from playhouse.postgres_ext import PostgresqlExtDatabase, BinaryJSONField
import logging

# from peewee import BaseModelSelect


# logger = logging.getLogger("peewee")
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())


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
# with open("./database.json", "r") as f:
    # setting = json.load(f)

database_name = "Judee_dev"
# database_name = "postgres"
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


class acm_contest_rank(BaseModel):
    id = IntegerField(primary_key=True)
    submission_number = IntegerField()
    accepted_number = IntegerField()
    total_time = IntegerField()
    submission_info = BinaryJSONField()
    contest_id = IntegerField()
    user_id = CharField(max_length=50)

    class Meta:
        db_table = "acm_contest_rank"


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


class contest_problem(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=5)
    problem_id = IntegerField()
    contest_id = IntegerField()
    first_ac_id = CharField(max_length=50)

    class Meta:
        db_table = "contest_problem"


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
    """
    get submission table infomation by submission id
    return model
    """
    try:
        with db.connection_context():
            result = submission.select().where(submission.ID == id).get()
            if dic:
                result = model_to_dict(result)
            return result
    except Exception as e:
        raise e


def get_problem_info(id, dic=False):
    """
    get time_limit, memory_limit and test_case_score of probem table by problem id
    return none if sth bad happen, else return number of affected rows 
    """
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
            return result
    except Exception as e:
        raise e


def get_contest_type(id, dic=False):
    """
    get rule_type of contest table by contest id
    return none if sth bad happen, else return number of affected rows 
    """
    try:
        with db.connection_context():
            result = contest.select(contest.rule_type).where(
                contest.id == id).get()
            if dic:
                result = model_to_dict(result)
            return result
    except Exception as e:
        raise e


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


def update_submission(id, result, compile_error_info=None, info=None):
    if compile_error_info:
        update_compile_error(id, result, compile_error_info)
    elif info:
        update_run_time(id, result, info)
    else:
        update_result(id, result)


def update_result(id, result):
    with db.connection_context():
        a = submission.update(result=result).where(
            submission.ID == id).execute()
        # affect num
        return a


def update_compile_error(id, result, compile_error_info):
    with db.connection_context():
        sub = (
            submission.select(submission.ID, submission.username_id)
            .where(submission.ID == id)
            .get()
        )
        a = (
            user_userdata.update(submit=user_userdata.submit + 1)
            .where(user_userdata.username_id == sub.username_id)
            # .get()
        )
        sub.result = result
        sub.compile_error_info = compile_error_info
        # affect num
        # return sub.save() + 
        return


def update_run_time(id, result, info):
    time_cost = 0
    memory_cost = 0
    score = 0

    with db.connection_context():
        temp = (
            submission.select(
                submission.username_id, submission.problem_id, problem.test_case_score
            )
            .join(problem, on=(submission.problem_id == problem.ID))
            .where(submission.ID == id)
            .get()
        )
        scores = temp.problem.test_case_score
        user_id = temp.username_id
        pro_id = temp.problem_id

    for a in range(len(info)):
        # time_cost += info[a].get("cpu_time", 0)
        time_cost = max(time_cost, info[a].get("cpu_time", 0))
        memory_cost = max(memory_cost, info[a].get("memory", 0))
        score += scores[a] if info[a].get("result", -1) == 0 else 0

    update_userdata(user_id, pro_id, result, score)

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
    """
    it will update submit, ac, ac_prob and score
    remember invoke this method before the submission with this score have been written in submission table
    """
    with db.connection_context():
        userdata = (
            user_userdata.select(
                user_userdata.ac,
                user_userdata.submit,
                user_userdata.score,
                user_userdata.ac_prob,
                # user_userdata.ranking,
                user_userdata.username_id,
            )
            .where(user_userdata.username_id == user_id)
            .get()
        )

        userdata.submit += 1

        if result == 0:
            ac_prob = list(map(int, userdata.ac_prob.strip().split("|")[:-1]))
            if problem_id not in ac_prob:
                userdata.ac_prob += "%d|" % problem_id
            userdata.ac += 1

        submissions = submission.select(submission.score).where(
            submission.problem_id == problem_id, submission.username_id == user_id
        )
        max_score = 0
        for a in submissions:
            max_score = max(max_score, a.score if a.score else 0)
        add_score = max(score - max_score, 0)
        userdata.score += add_score

        # return userdata.save(only=["ac", "submit", "score", "ac_prob"])
        return userdata.save()


# discarded
# def update_submission_by_id(id, result, compile_error_info=None):
    # """
    # if no compile_error_info, it only update result by id
    # else it update result and compile_error_info by id
    # """
    # with db.connection_context():
    #     if compile_error_info:
    #         a = (
    #             submission.update(
    #                 result=result, compile_error_info=compile_error_info)
    #             .where(submission.ID == id)
    #             .execute()
    #         )
    #     else:
    #         a = submission.update(result=result).where(
    #             submission.ID == id).execute()
    #     # affect num
    #     return a


# discarded
# def update_submission_userdata(
#     id, result, info, username_id=None, problem_id=None, test_case_info=None
# ):
#     """
#     it will update result, info, time_cost, memory_cost, score in submission by id
#     and it will invoke update_userdata() to update userdata table
#     you'd better give me username_id and problem_id and test_case_info, but it not must
#     """
#     time_cost = 0
#     memory_cost = 0
#     score = 0

#     if test_case_info:
#         scores = test_case_info
#     else:
#         with db.connection_context():
#             scores = (
#                 submission.select(problem.test_case_score)
#                 .join(problem, on=(submission.problem_id == problem.ID))
#                 .where(submission.ID == id)
#                 .get()
#                 .problem.test_case_score
#             )

#     for a in range(len(info)):
#         time_cost += info[a].get("cpu_time", 0)
#         memory_cost = max(memory_cost, info[a].get("memory", 0))
#         score += scores[a] if info[a].get("result", -1) == 0 else 0

#     if username_id and problem_id:
#         user_id = username_id
#         pro_id = problem_id
#     else:
#         with db.connection_context():
#             temp = (
#                 submission.select(submission.username_id,
#                                   submission.problem_id)
#                 .where(submission.ID == id)
#                 .get()
#             )
#             user_id = temp.problem_id
#             pro_id = temp.problem_id

#     update_userdata(user_id, pro_id, result, score)

#     with db.connection_context():
#         return (
#             submission.update(
#                 result=result,
#                 info=info,
#                 time_cost=time_cost,
#                 memory_cost=memory_cost,
#                 score=score,
#             )
#             .where(submission.ID == id)
#             .execute()
#         )


def update_oi_rank(contest_id, user_id, problem_id, problem_score):
    with db.connection_context():
        record = oi_contest_rank.get_or_none(
            oi_contest_rank.contest_id == contest_id,
            oi_contest_rank.user_id == user_id
        )

    if record is None:
        with db.connection_context():
            max_id = (
                oi_contest_rank.select(fn.MAX(oi_contest_rank.id).alias("max"))
                .get()
                .max
            )
        record = oi_contest_rank(
            id=max_id + 1,
            user_id=user_id,
            contest_id=contest_id,
            submission_number=0,
            total_score=0,
            submission_info={},
        )

    record.submission_number += 1

    add_score = max(
        problem_score - record.submission_info.get(problem_id, 0), 0)
    record.total_score += add_score

    record.submission_info[problem_id] = max(
        record.submission_info.get(problem_id, 0), problem_score
    )

    with db.connection_context():
        return record.save()


def update_acm_rank(contest_id, user_id, problem_id, sub_create_time, result):
    with db.connection_context():
        record = acm_contest_rank.get_or_none(
            acm_contest_rank.contest_id == contest_id,
            acm_contest_rank.user_id == user_id
        )

    if record is None:
        with db.connection_context():
            max_id = (
                acm_contest_rank.select(
                    fn.MAX(acm_contest_rank.id).alias("max"))
                .get()
                .max
            )
            # print(max_id)
            # assert False
        record = acm_contest_rank(
            # id=(max_id + 1 if  max_id else 1),
            user_id=user_id,
            contest_id=contest_id,
            submission_number=0,
            accepted_number=0,
            total_time=0,
            submission_info={},
        )
    #print(record.submission_info.get(problem_id, {}))
    #print(record.submission_info.get(problem_id, {}).get("is_ac", False))
    if record.submission_info.get(str(problem_id), {}).get("is_ac", False):
        # logging.debug('dsalkjf')
        print('adsfsad')
        return

    record.submission_number += 1

    record.submission_info[str(problem_id)] = record.submission_info.get(
        str(problem_id), {})
    if result == 0:
        # print(0)
        print('---------------------------------')
        print(sub_create_time)
        time = contest.select(contest.create_time).where(
            contest.id == contest_id).get().create_time
        print(time)
        print(sub_create_time - time)
        time = (sub_create_time - time).seconds + \
            (sub_create_time - time).days * 24 * 60 * 60
        print(time)
        record.total_time += time
        record.accepted_number += 1
        record.submission_info[str(problem_id)] = record.submission_info.get(
            str(problem_id), 0)
        record.submission_info[str(problem_id)]["is_ac"] = True
        record.submission_info[str(problem_id)]["ac_time"] = time
        with db.connection_context():
            # print('cp')
            cp = (
                contest_problem.select()
                .where(
                    contest_problem.contest_id == contest_id,
                    contest_problem.problem_id == problem_id,
                )
                .get()
            )
            # print(cp.first_ac_id)
            if cp.first_ac_id is None:
                # print('-------------------------none')
                record.submission_info[str(problem_id)]["is_first_ac"] = True
                cp.first_ac_id = user_id
                cp.save()
    else:
        record.total_time += 1200
        record.submission_info[str(problem_id)] = record.submission_info.get(
            str(problem_id), 0)
        record.submission_info[str(problem_id)]["is_ac"] = False
        #print(record.submission_info[str(problem_id)].get("error_number", 0))
        record.submission_info[str(problem_id)]["error_number"] = (
            record.submission_info[str(problem_id)].get("error_number", 0) + 1
        )

    with db.connection_context():
        # print('save')
        return record.save()


# may discarded
# def update_ocrank_by_cid_uid(contest_id, user_id, submission_add, total_score_add):
#     """
#     update oi_contest_rank
#     """
#     try:
#         with db.connection_context():
#             a = (
#                 oi_contest_rank.select(
#                     oi_contest_rank.id,
#                     oi_contest_rank.submission_number,
#                     oi_contest_rank.total_score,
#                 )
#                 .where(
#                     oi_contest_rank.contest_id == contest_id
#                     and oi_contest_rank.user_id == user_id
#                 )
#                 .get()
#             )
#             a.submission_number += submission_add
#             a.total_score += total_score_add
#             # affect num
#             return a.save()
#     except Exception as e:
#         raise e


def update_problem(problem_id, user_id, result):
    """
    update problem
    """
    with db.connection_context():
        pro = (
            problem.select(
                problem.ID,
                problem.submission_number,
                problem.accepted_number,
                problem.statistic_info,
            )
            .where(problem.ID == problem_id)
            .get()
        )

        print(problem_id)
        print(user_id)

        sub_count = (
            submission.select(fn.COUNT(submission.ID).alias("count"))
            .where(
                submission.problem_id == problem_id,
                submission.username_id == user_id
            )
            .get()
            .count
        )
        print('###########################')
        print(sub_count)
        if sub_count < 2:
            print('sub')
            pro.submission_number += 1

        if result == 0:
            print('ac')
            ac_count = (
                submission.select(fn.COUNT(submission.ID).alias("count"))
                .where(
                    submission.problem_id == problem_id, submission.username_id == user_id, submission.result == result
                )
                .get()
                .count
            )
            print(ac_count)
            if ac_count == 0:
                pro.accepted_number += 1

        name = result_map[result]
        num = pro.statistic_info.get(name, 0)
        pro.statistic_info[name] = num + 1
        # affect num
        return pro.save()


# try:
#     with db.connection_context():
#         a = oi_contest_rank.select(oi_contest_rank.id, oi_contest_rank.submission_info).where(oi_contest_rank.id == 2).get()
#         #a.submission_info = 'b'
#     # a.save()
#         # a.submission_number = 1
#         # a.save()
# except Exception as e:
#     with db.connection_context():
#         a = oi_contest_rank.select(oi_contest_rank.id, oi_contest_rank.submission_info).where(oi_contest_rank.id == 1).get()
# .group_by(oi_contest_rank.contest_id, oi_contest_rank.user_id)
# with db.connection_context():
#     a = oi_contest_rank.select(fn.COUNT(oi_contest_rank.id).alias('count')).where(oi_contest_rank.contest_id == 1 and oi_contest_rank.user_id == 2).get()
#     print(a.count)
