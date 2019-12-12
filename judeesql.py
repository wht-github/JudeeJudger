# from peewee import *, IntegerField
from playhouse.pool import PooledPostgresqlExtDatabase
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict
import json
from playhouse.postgres_ext import *
import logging
# from peewee import BaseModelSelect

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


with open('./conf.d/database.json', 'r') as f:
    setting = json.load(f)

database_name = 'Judee_dev'
#database_name = 'postgres'

db = PooledPostgresqlExtDatabase(database_name, **setting)


class BaseModel(Model):
    class Meta:
        database = db


class submission(BaseModel):
    ID = IntegerField(primary_key=True)
    contest_id = IntegerField()
    problem_id = IntegerField()
    create_time = DateTimeField()
    username_id = CharField(max_length=50)
    code = TextField()
    result = IntegerField()
    info = JSONField()
    language = CharField(max_length=15)
    statistic_info = JSONField()
    ip = TextField()

    class Meta:
        db_table = 'submission'


# class judge(BaseModel):
#     judge_id = IntegerField(primary_key=True)
#     submit_id = IntegerField()
#     test_case_id = IntegerField()
#     whether_special_judge = BooleanField()
#     result = IntegerField()
#     return_infor = TextField()

#     class Meta:
#         db_table = 'judge'


class oi_contest_rank(BaseModel):
    id = IntegerField(primary_key=True)
    submission_number = IntegerField()
    total_score = IntegerField()
    submission_info = BinaryJSONField()
    contest_id = IntegerField()
    user_id = CharField(max_length=50)

    class Meta:
        db_table = 'oi_contest_rank'


class problem(BaseModel):
    ID = IntegerField(primary_key=True)
    is_public = BooleanField()
    title = TextField()
    description = TextField()
    input_description = TextField()
    output_description = TextField()
    samples = BinaryJSONField()
    test_case_score = JSONField()
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
        db_table = 'problem'


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
        db_table = 'contest'


def get_submission_by_id(id, dic=False):
    # try:
    with db.connection_context():
            #result = submission.get(submission.ID == id)
        result = submission.select().where(submission.ID == id).get()
        if dic:
            result = model_to_dict(result)
        # id
        return result
    # except :
        #print(f'submission with id {id} not exist')
        # return None


def update_submission_by_id(id, result, info=None, statistic_info=None):
    with db.connection_context():
        if info and statistic_info:
            a = (
                submission.update(
                    result=result, info=info, statistic_info=statistic_info
                )
                .where(submission.ID == id)
                .execute()
            )
        else:
            if info:
                a = (
                    submission.update(result=result, info=info)
                    .where(submission.ID == id)
                    .execute()
                )
            elif statistic_info:
                a = (
                    submission.update(
                        result=result, statistic_info=statistic_info)
                    .where(submission.ID == id)
                    .execute()
                )
            else:
                a = (
                    submission.update(result=result)
                    .where(submission.ID == id)
                    .execute()
                )
        # affect num
        return a


def update_ocrank_by_cid_uid(contest_id, user_id, submission_add, total_score_add):
    try:
        with db.connection_context():
            #a = oi_contest_rank.get(oi_contest_rank.contest_id == contest_id and oi_contest_rank.user_id == user_id)
            a = oi_contest_rank.select(oi_contest_rank.id, oi_contest_rank.submission_number, oi_contest_rank.total_score).where(
                oi_contest_rank.contest_id == contest_id and oi_contest_rank.user_id == user_id).get()
            a.submission_number += submission_add
            a.total_score += total_score_add
            b = a.save()
            # affect num
            return b
    except:
        return None


def get_problem_info(id, dic=False):
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
    # try:
    with db.connection_context():
        result = contest.select(contest.rule_type).where(
            contest.id == id).get()
        if dic:
            result = model_to_dict(result)
# id
        return result
    # except:
    #    return None


def update_problem_by_id(id, result):
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

#a = update_ocrank_by_cid_uid(1,1,2,100)
